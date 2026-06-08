
COPR_NAME ?= cqi/hermes-agent
REPO_URL ?= https://github.com/tkdchen/packaging-hermes-agent
ROOT_CFG ?= fedora-rawhide-x86_64

PACKAGES_DIR = packages
RESULTS_DIR = results

name ?=
version ?=
skip_build_srpm ?=

pkg_dir = ./$(PACKAGES_DIR)/$(name)/
ifeq ($(name),hermes-agent)
spec = $(pkg_dir)/$(name).spec
else
spec = $(pkg_dir)/python-$(name).spec
endif
result_dir = ./$(RESULTS_DIR)/$(name)

.PHONY: require/arg/name
require/arg/name:
	@if [[ -z "$(name)" ]]; then \
		printf "Missing package name. Use argument name.\n" >&2; \
		exit 1; \
	fi

.PHONY: require/arg/version
require/arg/version:
	@if [[ -z "$(version)" ]]; then \
		printf "Missing package version. Use argument version.\n" >&2; \
		exit 1; \
	fi

.PHONY: dirs/packages
dirs/packages:
	if [[ ! -e ./$(PACKAGES_DIR) ]]; then mkdir ./$(PACKAGES_DIR); fi


.PHONY: dirs/results
dirs/results:
	if [[ ! -e ./$(RESULTS_DIR) ]]; then mkdir ./$(RESULTS_DIR); fi


.PHONY: package/import
package/import: require/arg/name require/arg/version dirs/packages
	mkdir ./$(PACKAGES_DIR)/$(name); \
	cd ./$(PACKAGES_DIR)/$(name); \
	pyp2spec --version $(version) --fedora-compliant $(name)


.PHONY: package/fetch-source
package/fetch-source: require/arg/name
	make -f .copr/Makefile source local=true outdir=$(pkg_dir) spec=$(spec)


.PHONY: copr/add-package/scm
copr/add-package/scm: require/arg/name
	copr-cli add-package-scm \
		--method make_srpm \
		--name "python-$(name)" \
		--clone-url $(REPO_URL) \
		--subdir "$(PACKAGES_DIR)/$(name)" \
		--spec "python-$(name).spec" \
		$(COPR_NAME)


.PHONY: local/srpm
local/srpm: require/arg/name dirs/packages
	if [[ -z "$(skip_build_srpm)" ]]; then \
		make -f .copr/Makefile srpm local=true outdir="$(pkg_dir)" spec="$(spec)"; \
	fi

.PHONY: local/build
local/build: dirs/results local/srpm
	version=$$(rpmspec --parse "$(spec)" | grep -E "^Version: +" | sed -E "s/^Version: +//"); \
	find "$(pkg_dir)" -name "python-$(name)-$${version}-*.fc??.src.rpm" >./srpm_files; \
	trap 'rm -f ./srpm_files' EXIT ERR; \
	if [[ $$(wc -l ./srpm_files | cut -d' ' -f1) -eq 1 ]]; then \
		mock --rebuild --root $(ROOT_CFG) --resultdir "$(result_dir)" "$$(cat srpm_files)"; \
	else \
		printf "Cannot start mock build. Check SRPM under %s\n" "$(pkg_dir)" >&2; \
		exit 1; \
	fi; \

dependent_rpms ?=
srpm ?=

.PHONY: local/build
local/build-custom:
	mock -r $(ROOT_CFG) --dnf --init
	mock -r $(ROOT_CFG) --install which findutils vim-enhanced dnf-utils $(dependent_rpms)
	mock -r $(ROOT_CFG) --no-clean --no-cleanup-after --resultdir ./$(RESULTS_DIR)/ --rebuild $(srpm)


COPR_NAME ?= cqi/hermes-agent
REPO_URL ?= https://github.com/tkdchen/packaging-hermes-agent
ROOT_CFG ?= fedora-rawhide-x86_64

PACKAGES_DIR = packages
RESULTS_DIR = results

name ?=
version ?=

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


.PHONY: copr/add-package/scm
copr/add-package/scm: require/arg/name
	copr-cli add-package-scm \
		--method make_srpm \
		--name "python-$(name)" \
		--clone-url $(REPO_URL) \
		--subdir "$(PACKAGES_DIR)/$(name)" \
		--spec "python-$(name).spec" \
		$(COPR_NAME)


.PHONY: local/build
local/build: require/arg/name dirs/results
	pkg_dir="./$(PACKAGES_DIR)/$(name)/"; \
	spec="$${pkg_dir}/python-$(name).spec"; \
	result_dir="./$(RESULTS_DIR)/$(name)"; \
	make -f .copr/Makefile srpm local=true outdir="$$pkg_dir" spec="$$spec"; \
	version=$$(rpmspec --parse "$$spec" | grep -E "^Version: +" | sed -E "s/^Version: +//"); \
	find "$${pkg_dir}" -name "python-$(name)-$${version}-*.fc??.src.rpm" >./srpm_files; \
	trap 'rm -f ./srpm_files' EXIT ERR; \
	if [[ $$(wc -l ./srpm_files | cut -d' ' -f1) -eq 1 ]]; then \
		mock --rebuild --root $(ROOT_CFG) --resultdir "$$result_dir" "$$(cat srpm_files)"; \
	else \
		printf "Cannot start mock build. Check SRPM under %s\n" "$$pkg_dir" >&2; \
		exit 1; \
	fi; \

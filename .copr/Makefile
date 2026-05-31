pypi_name = $(shell grep -m 1 "^%global pypi_name " $(spec) | cut -d' ' -f3)
# sdist_name=$(shell echo $(pypi_name) | tr - _)
version = $(shell rpm -q --queryformat '%{version}\n' --specfile $(spec) | head -n 1)

ifeq ($(local),true)
sources_dir = ~/rpmbuild/SOURCES/
else
sources_dir = /builddir/build/SOURCES/
endif

.PHONY: srpm
srpm:
	if [ -n "$(local)" ]; then \
		echo python3 -m pip download --no-binary :all: --no-deps --dest ~/rpmbuild/SOURCES "$(pypi_name)==$(version)"; \
	fi; \
	grep -E "^Patch: " $(spec) | while read -r prefix filename; do \
		echo "Patch: $${filename}"; \
		cp "$$(dirname $(spec))/$${filename}" $(sources_dir); \
	done; \
	srpm_file=$$(rpmbuild -bs $(spec) | grep "^Wrote:" | cut -d' ' -f2) ; \
	cp "$${srpm_file}" "$(outdir)"

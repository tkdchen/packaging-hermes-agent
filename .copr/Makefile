srpm:
	if [ -z "$(local)" ]; then dnf install -y rpmbuild python3-pip rpm; fi
	pypi_name=$$(grep -m 1 "^%global pypi_name " $(spec) | cut -d' ' -f3); \
	version=$$(rpm -q --queryformat '%{version}\n' --specfile $(spec) | head -n 1); \
	python3 -m pip download --no-binary :all: --no-deps "$${pypi_name}==$${version}"; \
	if [ -n "$(local)" ]; then \
		mock --buildsrpm --spec $(spec) --sources $$(dirname $(spec)) --resultdir $$(dirname $(spec)); \
	else \
		grep -E "^Patch[0-9]*: " $(spec) | while read -r prefix filename; do \
			cp "$$(dirname $(spec))/${filename}" /builddir/build/SOURCES/; \
		done; \
	fi; \
	srpm_file=$$(rpmbuild -bs $(spec) | grep "^Wrote:" | cut -d' ' -f2) ; \
	cp "$${srpm_file}" "$(outdir)"

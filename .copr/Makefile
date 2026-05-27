srpm:
	if [ -z "$(local)" ]; then dnf install -y rpmbuild python3-pip rpm; fi
	pypi_name=$$(grep -m 1 "^%global pypi_name " $(spec) | cut -d' ' -f3); \
	version=$$(rpm -q --queryformat '%{version}\n' --specfile $(spec) | head -n 1); \
	python3 -m pip download --no-binary :all: --no-deps "$${pypi_name}==$${version}"; \
	if [ -z "$(local)" ]; then \
		mkdir -p $${HOME}/rpmbuild/SPECS $${HOME}/rpmbuild/SOURCES; \
		mv "$${pypi_name}-$${version}.tar.gz" $${HOME}/rpmbuild/SOURCES; \
	fi; \
	srpm_file=$$(rpmbuild -bs $(spec) | grep "^Wrote:" | cut -d' ' -f2) ; \
	cp "$${srpm_file}" "$(outdir)"

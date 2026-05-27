srpm:
	dnf install -y rpmbuild python3-pip rpm
	pypi_name=$$(grep -m 1 "^%global pypi_name " $(spec) | cut -d' ' -f3); \
	version=$$(rpm -q --queryformat '%{version}\n' $(spec) | head -n 1); \
	python3 -m pip download --no-binary :all: --no-deps "$${pypi_name}==$${version}"; \
	mkdir -p $${HOME}/rpmbuild/SPECS $${HOME}/rpmbuild/SOURCES; \
	cp "$${pypi_name}*.tar.gz" $${HOME}/rpmbuild/SOURCES; \
	cp "$(spec)" $${HOME}/rpmbuild/SPECS; \
	rpmbuild -bs $(spec) ; \
	cp $${HOME}/rpmbuild/SRPMS/*.src.rpm $(outdir)

srpm:
	if [ -z "$(local)" ]; then dnf install -y rpmbuild python3-pip rpm; fi
	pypi_name=$$(grep -m 1 "^%global pypi_name " $(spec) | cut -d' ' -f3); \
	version=$$(rpm -q --queryformat '%{version}\n' --specfile $(spec) | head -n 1); \
	python3 -m pip download --no-binary :all: --no-deps "$${pypi_name}==$${version}"; \
	mkdir -p $${HOME}/rpmbuild/SPECS $${HOME}/rpmbuild/SOURCES; \
	mv "$${pypi_name}-$${version}.tar.gz" $${HOME}/rpmbuild/SOURCES; \
	rpmbuild -bs $(spec) ; \
	nvr=$$(rpm -q --queryformat '%{nvr}\n' --specfile $(spec) | grep "^python-"); \
	cp $${HOME}/rpmbuild/SRPMS/$${nvr}.src.rpm $(outdir)

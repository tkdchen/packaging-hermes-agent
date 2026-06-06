Name:           python-httpx-aiohttp
Version:        0.1.12
Release:        %autorelease
Summary:        Aiohttp transport for HTTPX

License:        BSD-3-Clause
URL:            https://karpetrosyan.github.io/httpx-aiohttp/
Source:         %{pypi_source httpx_aiohttp}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
This is package 'httpx-aiohttp' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-httpx-aiohttp
Summary:        %{summary}

%description -n python3-httpx-aiohttp %_description


%prep
%autosetup -p1 -n httpx_aiohttp-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l httpx_aiohttp


%check
# Do not run the tests. Network is required.
%pyproject_check_import


%files -n python3-httpx-aiohttp -f %{pyproject_files}


%changelog
%autochangelog

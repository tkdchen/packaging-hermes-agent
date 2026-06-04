Name:           python-firecrawl-py
Version:        4.17.0
Release:        %autorelease
Summary:        Python SDK for Firecrawl API

License:        MIT
URL:            https://github.com/firecrawl/firecrawl
Source:         %{pypi_source firecrawl_py}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
The Firecrawl Python SDK is a library that lets you easily search, scrape, and
interact with the web for AI agents — returning clean Markdown or structured
data your agents can ship with. It provides a simple and intuitive interface
for the Firecrawl API.}

%description %_description

%package -n     python3-firecrawl-py
Summary:        %{summary}

%description -n python3-firecrawl-py %_description


%prep
%autosetup -p1 -n firecrawl_py-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l firecrawl

rm -rf %{buildroot}%{python3_sitelib}/tests/


%check
%pyproject_check_import


%files -n python3-firecrawl-py -f %{pyproject_files}


%changelog
%autochangelog

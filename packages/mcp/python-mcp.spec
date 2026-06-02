%global pypi_name mcp
Name:           python-mcp
Version:        1.26.0
Release:        %autorelease
Summary:        Model Context Protocol SDK

License:        MIT
URL:            https://modelcontextprotocol.io
Source:         %{pypi_source mcp}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
The official Python SDK for Model Context Protocol servers and clients.}

%description %_description

%package -n     python3-mcp
Summary:        %{summary}

%description -n python3-mcp %_description

%pyproject_extras_subpkg -n python3-mcp cli,rich,ws


%prep
%autosetup -p1 -n mcp-%{version}


%generate_buildrequires
# Keep only those extras which you actually want to package or use during tests
%pyproject_buildrequires -x cli,rich,ws


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l mcp


%check
%pyproject_check_import


%files -n python3-mcp -f %{pyproject_files}
%doc README.md RELEASE.md SECURITY.md CODE_OF_CONDUCT.md
%license LICENSE
%{_bindir}/mcp


%changelog
%autochangelog

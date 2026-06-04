Name:           python-fal-client
Version:        0.13.1
Release:        %autorelease
Summary:        Python client for fal.ai

License:        Apache-2.0
URL:            https://fal.ai
Source:         %{pypi_source fal_client}
# Upstream issue: https://github.com/fal-ai/fal/issues/1066
Patch:          add-license.patch

BuildArch:      noarch
BuildRequires:  python3-devel

BuildRequires:  python3-pytest
BuildRequires:  python3-pytest-asyncio
BuildRequires:  python3-pytest-mock
BuildRequires:  python3-pillow


%global _description %{expand:
Fastest way to serve open source ML models to millions.}

%description %_description

%package -n     python3-fal-client
Summary:        %{summary}

%description -n python3-fal-client %_description


%prep
%autosetup -p1 -n fal_client-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l fal_client


%check
%pyproject_check_import

%pytest


%files -n python3-fal-client -f %{pyproject_files}
%doc README.md
# %license LICENSE


%changelog
%autochangelog

Name:           python-google-auth-httplib2
Version:        0.3.1
Release:        %autorelease
Summary:        Google Authentication Library: httplib2 transport

License:        Apache-2.0
URL:            https://github.com/googleapis/google-cloud-python/packages/google-auth-httplib2
Source:         %{pypi_source google_auth_httplib2}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(flask)
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-localserver)


%global _description %{expand:
The library was created to help clients migrate from oauth2client to
google-auth, however this library is no longer maintained. For any new usages
please see provided transport layers by google-auth library.}

%description %_description

%package -n     python3-google-auth-httplib2
Summary:        %{summary}

%description -n python3-google-auth-httplib2 %_description


%prep
%autosetup -p1 -n google_auth_httplib2-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l google_auth_httplib2


%check
%pytest


%files -n python3-google-auth-httplib2 -f %{pyproject_files}
%doc README.rst
%license LICENSE


%changelog
%autochangelog

Name:           python-google-api-python-client
Version:        2.194.0
Release:        %autorelease
Summary:        Google API Client Library for Python

License:        Apache-2.0
URL:            https://github.com/googleapis/google-api-python-client/
Source:         %{pypi_source google_api_python_client}

# Remove discovery_cache/file_cache.py
# oauth2client was a dependency but replaced with google-auth.
# file_cache.py can't be imported. Error is raised during import.
Patch:          remove-discovery_cache-file_cache.patch

# Remove discovery_cache/appengine_memcache.py
# Quote from source code:
# This is only an optional dependency because we only import this
# module when google.appengine.api.memcache is available.
# from google.appengine.api import memcache
# Google appengine is not a dependency so far.
Patch:          remove-discovery_cache-appengine_memcache.patch

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
The official Python client library for Google's discovery based APIs.}

%description %_description

%package -n     python3-google-api-python-client
Summary:        %{summary}

%description -n python3-google-api-python-client %_description


%prep
%autosetup -p1 -n google_api_python_client-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l googleapiclient apiclient


%check
%pyproject_check_import


%files -n python3-google-api-python-client -f %{pyproject_files}
%doc README.md


%changelog
%autochangelog

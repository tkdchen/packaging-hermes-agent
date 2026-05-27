%global pypi_name typing_extensions
Name:           python-typing-extensions
Version:        4.15.0
Release:        %autorelease
Summary:        Backported and Experimental Type Hints for Python 3.9+

License:        PSF-2.0
URL:            https://github.com/python/typing_extensions
Source:         %{pypi_source typing_extensions}

BuildArch:      noarch
BuildRequires:  python3-devel

# As of building this package, tests fail to run with python3.14-3.14.4-2.fc44.
# Check python3.14 after a period of time.
BuildRequires:  python3.13
BuildRequires:  python3.13-test


%global _description %{expand:
The typing_extensions module serves two related purposes:

- Enable use of new type system features on older Python versions. For example,
  typing.TypeGuard is new in Python 3.10, but typing_extensions allows users on
  previous Python versions to use it too.
- Enable experimentation with new type system PEPs before they are accepted and
  added to the typing module.}

%description %_description

%package -n     python3-typing-extensions
Summary:        %{summary}

%description -n python3-typing-extensions %_description


%prep
%autosetup -p1 -n typing_extensions-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l typing_extensions


%check
cd src/
python3.13 -m unittest discover


%files -n python3-typing-extensions -f %{pyproject_files}


%changelog
* Wed May 27 2025 Chenxiong Qi <qcxhome@gmail.com>
- Initial package

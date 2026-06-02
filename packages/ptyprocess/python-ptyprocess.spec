Name:           python-ptyprocess
Version:        0.7.0
Release:        %autorelease
Summary:        Run a subprocess in a pseudo terminal

License:        ISC
URL:            https://github.com/pexpect/ptyprocess
Source:         %{pypi_source ptyprocess}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
Run a subprocess in a pseudo terminal.}

%description %_description

%package -n     python3-ptyprocess
Summary:        %{summary}

%description -n python3-ptyprocess %_description


%prep
%autosetup -p1 -n ptyprocess-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
# Add top-level Python module names here as arguments, you can use globs
%pyproject_save_files -l ptyprocess


%check
%pyproject_check_import


%files -n python3-ptyprocess -f %{pyproject_files}
%doc README.rst
%license LICENSE


%changelog
%autochangelog

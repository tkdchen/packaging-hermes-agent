Name:           python-simple-term-menu
Version:        1.6.6
Release:        %autorelease
Summary:        A Python package which creates simple interactive menus on the command line.

License:        MIT
URL:            https://github.com/IngoMeyer441/simple-term-menu
Source:         %{pypi_source simple_term_menu}

BuildArch:      noarch
BuildRequires:  python3-devel

%global _description %{expand:
A Python package which creates simple interactive menus on the command line.}

%description %_description

%package -n     python3-simple-term-menu
Summary:        %{summary}

%description -n python3-simple-term-menu %_description


%prep
%autosetup -p1 -n simple_term_menu-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l simple_term_menu


%check
%pyproject_check_import


%files -n python3-simple-term-menu -f %{pyproject_files}
%{_bindir}/simple-term-menu 


%changelog
%autochangelog

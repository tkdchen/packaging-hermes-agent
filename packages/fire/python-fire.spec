%global pypi_name fire
Name:           python-fire
Version:        0.7.1
Release:        %autorelease
Summary:        A library for automatically generating command line interfaces.

License:        Apache-2.0
URL:            https://github.com/google/python-fire
Source:         %{pypi_source fire}
Patch:          fix-get-event-loop.patch

BuildArch:      noarch
BuildRequires:  python3-devel

BuildRequires:  python3-pytest
BuildRequires:  python3-hypothesis
BuildRequires:  python3-Levenshtein


%global _description %{expand:
This is package 'fire' generated automatically by pyp2spec.}

%description %_description

%package -n     python3-fire
Summary:        %{summary}

%description -n python3-fire %_description


%prep
%autosetup -p1 -n fire-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l fire


%check
%pyproject_check_import
%pytest


%files -n python3-fire -f %{pyproject_files}


%changelog
* Wed May 27 2026 Chenxiong Qi <qcxhome@gmail.com>
- Build fire==0.7.1

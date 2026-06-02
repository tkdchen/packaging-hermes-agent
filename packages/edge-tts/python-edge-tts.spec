%global srcname edge_tts
Name:           python-edge-tts
Version:        7.2.7
Release:        %autorelease
Summary:        Microsoft Edge_s TTS

License:        LGPL-3.0-or-later
URL:            https://github.com/rany2/edge-tts/
Source:         %{pypi_source %{srcname}}

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
Use Microsoft Edge's online text-to-speech service from Python WITHOUT needing
Microsoft Edge or Windows or an API key.}

%description %_description

%package -n     python3-edge-tts
Summary:        %{summary}

%description -n python3-edge-tts %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l 'edge_*'


%check
# Upstream does not have test code.
%pyproject_check_import


%files -n python3-edge-tts -f %{pyproject_files}
%doc README.md
%license LICENSE
%{_bindir}/edge-tts
%{_bindir}/edge-playback


%changelog
%autochangelog

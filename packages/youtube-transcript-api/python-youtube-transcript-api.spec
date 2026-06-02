Name:           python-youtube-transcript-api
Version:        1.2.4
Release:        %autorelease
Summary:        YouTube Transcript API

License:        MIT
URL:            https://github.com/jdepoix/youtube-transcript-api
Source:         %{pypi_source youtube_transcript_api}

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(httpretty)


%global _description %{expand:
This is a python API which allows you to get the transcript/subtitles for a
given YouTube video. It also works for automatically generated subtitles and it
does not require an API key nor a headless browser, like other selenium based
solutions do!}

%description %_description

%package -n     python3-youtube-transcript-api
Summary:        %{summary}

%description -n python3-youtube-transcript-api %_description


%prep
%autosetup -p1 -n youtube_transcript_api-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -l youtube_transcript_api


%check
%pyproject_check_import


%files -n python3-youtube-transcript-api -f %{pyproject_files}
%doc README.md
%{_bindir}/youtube_transcript_api


%changelog
%autochangelog

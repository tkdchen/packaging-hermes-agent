%global srcname hermes_agent
Name:           python-hermes-agent
Version:        0.14.0
Release:        %autorelease
Summary:        The self-improving AI agent — creates skills from experience, improves them during use, and runs anywhere

License:        MIT
URL:            github.com/NousResearch/hermes-agent
Source:         %{pypi_source %{srcname}}
Source:         hermes.sh
# Proxy of executable hermes CLI.
Patch:          relax-deps.patch
# Fix: https://github.com/NousResearch/hermes-agent/pull/35346
# It is marked as P3 (Low).
Patch:          tests-conftest-0.14.0.patch

BuildArch:      noarch
BuildRequires:  python3-devel
BuildRequires:  python3dist(pytest)
BuildRequires:  python3dist(pytest-xdist)
BuildRequires:  python3dist(pytest-asyncio)
BuildRequires:  python3dist(pytest-split)


%global _description %{expand:
The agent that grows with you}

%description %_description

%package -n     hermes-agent
Summary:        %{summary}

Requires:       chromium
# ffmpeg for TTS voice messages
Requires:       ffmpeg-free
# required for browser tools and TUI
Requires:       nodejs
# ripgrep for faster file search
Requires:       ripgrep

Requires:       python3dist(aiohttp) == 3.13.5
Requires:       python3dist(ptyprocess) == 0.7
Requires:       python3dist(simple-term-menu) == 1.6.6
# TTS provider. Install to avoid lazy-install when launching hermes for the
# first time.
Requires:       python3dist(edge-tts) == 7.2.7-1
# Image generation backends
Requires:       python3dist(fal-client) == 0.13.1-1
# mcp
Requires:       python3dist(mcp) == 1.27.1
# tool: acp
Requires:       python3dist(agent-client-protocol) == 0.9
# tool: hermes dashboard
Requires:       python3dist(fastapi) == 0.136.3
Requires:       python3dist(uvicorn[standard]) == 0.40
# Skills: Google workspace
Requires:       python3dist(google-api-python-client) == 2.194
Requires:       python3dist(google-auth-httplib2) == 0.3.1
Requires:       python3dist(google-auth-oauthlib) == 1.2.4
# Skills: youtube
Requires:       python3dist(youtube-transcript-api) == 1.2.4
# Web search backends
Requires:       python3dist(exa-py) == 2.10.2
Requires:       python3dist(firecrawl-py) == 4.17
Requires:       python3dist(parallel-web) == 0.4.2
# Inference providers
Requires:       python3dist(anthropic) == 0.87
Requires:       python3dist(azure-identity) == 1.25.3
# AWS Bedrock
Requires:       python3dist(boto3) == 1.43.21


%description -n hermes-agent %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

mv %{buildroot}/%{_bindir}/hermes %{buildroot}/%{_bindir}/hermes-cli
install %{_sourcedir}/hermes.sh %{buildroot}/%{_bindir}/hermes

mkdir -p %{buildroot}/%{_datadir}/hermes-agent
cp -r skills/ %{buildroot}/%{_datadir}/hermes-agent/
cp -r optional-skills/ %{buildroot}/%{_datadir}/hermes-agent/
cp -r plugins/ %{buildroot}/%{_datadir}/hermes-agent/


%check
# Deselect tests tests/test_install_sh_*.py. They require scripts/install.sh
# which is not included in sdist.

# Deselect test test_lint_config.py. It requires .github/workflows/lint.yml
# which is not included in sdist.

# Deselect part of test_live_system_guard_self_test that require real systemctl
# command.

# Deselect test_mini_swe_runner, its requirements is not included in base
# dependencies.

PYTHONPATH=. %pytest \
             --deselect=tests/test_mcp_serve.py \
             --deselect=tests/test_install_sh_symlink_stomp.py \
             --deselect=tests/test_install_sh_setup_wizard_tty_probe.py \
             --deselect=tests/test_install_sh_root_fhs_uv_python_path.py \
             --deselect=tests/test_install_sh_browser_install.py \
             --deselect=tests/test_install_sh_termux_network_prereqs.py \
             --deselect=tests/test_install_sh_pythonpath_sanitization.py \
             --deselect=tests/test_lint_config.py \
             --deselect=tests/test_mini_swe_runner.py \
             --deselect=tests/test_termux_all_extra_compat.py::test_install_script_prefers_termux_all_then_fallbacks \
             --deselect=tests/test_live_system_guard_self_test.py::test_systemctl_unrelated_unit_passes_through \
             --deselect=tests/test_live_system_guard_self_test.py::test_systemctl_list_units_passes_through \
             --deselect=tests/test_live_system_guard_self_test.py::test_systemctl_show_passes_through \
             --deselect=tests/test_live_system_guard_self_test.py::test_systemctl_status_passes_through \
             tests/test_*.py


%files -n hermes-agent
%doc README.md
%license LICENSE

%{python3_sitelib}/__pycache__/
%{python3_sitelib}/%{srcname}-%{version}.dist-info/

%{_bindir}/hermes
%{_bindir}/hermes-cli
%{_bindir}/hermes-acp
%{_bindir}/hermes-agent

%{python3_sitelib}/acp_adapter/
%{python3_sitelib}/agent/
%{python3_sitelib}/cron/
%{python3_sitelib}/gateway/
%{python3_sitelib}/hermes_cli/
%{python3_sitelib}/plugins/
%{python3_sitelib}/providers/
%{python3_sitelib}/tools/
%{python3_sitelib}/tui_gateway/

%{python3_sitelib}/batch_runner.py
%{python3_sitelib}/cli.py
%{python3_sitelib}/hermes_bootstrap.py
%{python3_sitelib}/hermes_constants.py
%{python3_sitelib}/hermes_logging.py
%{python3_sitelib}/hermes_state.py
%{python3_sitelib}/hermes_time.py
%{python3_sitelib}/model_tools.py
%{python3_sitelib}/run_agent.py
%{python3_sitelib}/toolset_distributions.py
%{python3_sitelib}/toolsets.py
%{python3_sitelib}/trajectory_compressor.py
%{python3_sitelib}/utils.py

# Include skills, optional-skills and plugins
%{_datadir}/hermes-agent/

%changelog
%autochangelog

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

# This is a workaround taking over hermes update and uninstall command.
# It borrows the managed system concept of hermes, which looks applies to NixOS and perhaps Homebrew.
# This workaround will be deleted when upstream has a better managed system support (maybe need redesign).
Patch:          0001-Take-over-update-and-uninstall-command.patch

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

# Background of listing these dependencies explicitly:
# When building 0.14.0, hermes-agent project does not support namespaced modules.
# Source code is not organized in the src-layout, e.g. src/hermes_agent/...
# In order to not pollute site-packages/, a workaround is to install into /usr/share/hermes-agent,
# which results in .dist-info/ is moved outside site-packages/, then automatic dependency generator does not work.
#
# When hermes-agent upstream starts to support namespaced modules, remove these and back to rely on the
# automatic dependency generator.

# Base dependencies
Requires:       python3dist(openai) == 2.24
Requires:       python3dist(python-dotenv) == 1.2.2
Requires:       python3dist(fire) == 0.7.1
Requires:       python3dist(httpx[socks]) == 0.28.1
Requires:       python3dist(rich) == 15
Requires:       python3dist(tenacity) == 9.1.4
Requires:       python3dist(pyyaml) == 6.0.3
Requires:       python3dist(ruamel-yaml) == 0.19.1
Requires:       python3dist(requests) == 2.33.1
Requires:       python3dist(jinja2) == 3.1.6
Requires:       python3dist(pydantic) == 2.13.4
Requires:       python3dist(prompt-toolkit) == 3.0.52
Requires:       python3dist(croniter) == 6.2.2
Requires:       python3dist(pyjwt[crypto]) == 2.12.1
Requires:       python3dist(psutil) == 7.2.2


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
Requires:       python3dist(fastapi) >= 0.136.3
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
Requires:       python3dist(boto3) >= 1.43.21


%description -n hermes-agent %_description


%prep
%autosetup -p1 -n %{srcname}-%{version}


%generate_buildrequires
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install

mv %{buildroot}/%{_bindir}/hermes %{buildroot}%{_bindir}/hermes-cli
install -p %{_sourcedir}/hermes.sh %{buildroot}%{_bindir}/hermes

HERMES_INST_DIR=%{buildroot}%{_datadir}/hermes-agent/

mkdir -p ${HERMES_INST_DIR}
cp -r skills/ ${HERMES_INST_DIR}
cp -r optional-skills/ ${HERMES_INST_DIR}

mkdir ${HERMES_INST_DIR}/__pycache__/

hermes_files_and_dirs=(
    %{srcname}-%{version}.dist-info/

    acp_adapter/
    agent/
    cron/
    gateway/
    hermes_cli/
    plugins/
    providers/
    tools/
    tui_gateway/

    batch_runner.py
    cli.py
    hermes_bootstrap.py
    hermes_constants.py
    hermes_logging.py
    hermes_state.py
    hermes_time.py
    model_tools.py
    run_agent.py
    toolset_distributions.py
    toolsets.py
    trajectory_compressor.py
    utils.py
)

for file_or_dir_name in ${hermes_files_and_dirs[@]}
do
    mv %{buildroot}/%{python3_sitelib}/${file_or_dir_name} ${HERMES_INST_DIR}
    if [[ .${file_or_dir_name##*.} == .py ]]; then
        mv %{buildroot}/%{python3_sitelib}/__pycache__/${file_or_dir_name%.*}.cpython-3??.pyc \
           ${HERMES_INST_DIR}/__pycache__/
    fi
done


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

%{_bindir}/hermes
%{_bindir}/hermes-cli
%{_bindir}/hermes-acp
%{_bindir}/hermes-agent

# Include the installation directory
%{_datadir}/hermes-agent/


%changelog
%autochangelog

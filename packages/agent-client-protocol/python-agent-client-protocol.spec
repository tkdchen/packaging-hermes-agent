Name:           python-agent-client-protocol
Version:        0.9.0
Release:        %autorelease
Summary:        Python SDK for ACP clients and agents.

License:        Apache-2.0
URL:            https://agentclientprotocol.github.io/python-sdk/
Source:         https://github.com/agentclientprotocol/python-sdk/archive/refs/tags/%{version}.tar.gz
# 2026-06-07: Fedora 45 Python 3.15 side tag has been merged
Patch:          allow-building-with-python-3.15.patch

BuildArch:      noarch
BuildRequires:  python3-devel


%global _description %{expand:
Build ACP-compliant agents and clients in Python with generated schema models, asyncio transports, helper builders, and runnable demos.}

%description %_description

%package -n     python3-agent-client-protocol
Summary:        %{summary}

%description -n python3-agent-client-protocol %_description


%prep
%autosetup -p1 -n python-sdk-%{version}


%generate_buildrequires
# Exclude extra logfire, hermes-agent does not rely on it.
%pyproject_buildrequires


%build
%pyproject_wheel


%install
%pyproject_install
%pyproject_save_files -L acp


%check
%pyproject_check_import


%files -n python3-agent-client-protocol -f %{pyproject_files}
%doc README.md CONTRIBUTING.md
%license LICENSE


%changelog
%autochangelog

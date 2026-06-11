#!/usr/bin/env bash

# This script intend to run inside test container.

set -ex

COPR_NAME=${1:?Missing Copr name}

dnf install -y dnf-utils which
dnf copr enable -y "${COPR_NAME}"
dnf install -y hermes-agent

which hermes
which hermes-acp
which hermes-agent

chromium-browser --version
ffmpeg -version
node --version

declare -r DATA_DIR=/usr/share/hermes-agent

if [[ ! -e "${DATA_DIR}/skills" ]]; then
    printf "Bundled skills are not installed under %s\n" "$DATA_DIR" >&2
    exit 1
fi
if [[ ! -e "${DATA_DIR}/optional-skills" ]]; then
    printf "Optional skills are not installed under %s\n" "$DATA_DIR" >&2
    exit 1
fi

python3 -c "
import plugins
print(plugins)
"

if ! hermes update 2>&1 | grep -E "this Hermes installation is managed by Fedora"; then
    printf "Managed system does not cover command 'hermes update'.\n" >&2
    exit 1
fi


if ! hermes update --check 2>&1 | grep -E "this Hermes installation is managed by Fedora"; then
    printf "Managed system does not cover command 'hermes update --check'.\n" >&2
    exit 1
fi

if ! hermes uninstall 2>&1 | grep -E "this Hermes installation is managed by Fedora"; then
    printf "Managed system does not cover command 'hermes uninstall'.\n" >&2
    exit 1
fi

if ! hermes uninstall 2>&1 | grep -E "dnf remove hermes-agent"; then
    printf "Managed system covers command 'hermes uninstall', but 'dnf remove hermes-agent' is not prompted.\n" >&2
    exit 1
fi

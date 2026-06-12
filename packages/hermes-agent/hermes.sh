#!/usr/bin/env bash

declare -r INST_DIR=/usr/share/hermes-agent

: "${HERMES_BUNDLED_SKILLS:=${INST_DIR}/skills}"
: "${HERMES_OPTIONAL_SKILLS:=${INST_DIR}/optional-skills}"

export HERMES_BUNDLED_SKILLS
export HERMES_OPTIONAL_SKILLS

export PYTHONPATH=$INST_DIR

# Prevent relative commands from run and prompt right dnf command.
export HERMES_MANAGED_BY=fedora

/usr/bin/hermes-cli "$@"

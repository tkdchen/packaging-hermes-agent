#!/usr/bin/env bash

declare -r DATA_DIR=/usr/share/hermes-agent

: "{HERMES_BUNDLED_SKILLS:-${DATA_DIR}}"
: "{HERMES_OPTIONAL_SKILLS:-${DATA_DIR}}"

export HERMES_BUNDLED_SKILLS
export HERMES_OPTIONAL_SKILLS

hermes-cli "$@"

#!/usr/bin/env bash

declare -r DATA_DIR=/usr/share/hermes-agent

: "${HERMES_BUNDLED_SKILLS:=${DATA_DIR}/skills}"
: "${HERMES_OPTIONAL_SKILLS:=${DATA_DIR}/optional-skills}"

export HERMES_BUNDLED_SKILLS
export HERMES_OPTIONAL_SKILLS

hermes-cli "$@"

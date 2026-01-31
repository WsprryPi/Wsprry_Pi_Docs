#!/usr/bin/env bash

# -----------------------------------------------------------------------------
# @brief  Create or activate a Python venv in {repo-root}/docs.
# @details
#   Always uses the docs directory at the repository root, regardless of the
#   current working directory. Creates .venv if missing and installs
#   requirements.txt. Activates the venv in all cases.
#
#   This script must be sourced:
#       source setup_docs_venv.sh
# -----------------------------------------------------------------------------

# Ensure the script is sourced
if [[ "${BASH_SOURCE[0]}" == "${0}" ]]; then
    printf "%s\n" "Error: This script must be sourced, not executed." >&2
    exit 1
fi

# Determine repository root
if repo_root=$(git rev-parse --show-toplevel 2>/dev/null); then
    :
else
    printf "%s\n" "Error: Not inside a git repository." >&2
    exit 1
fi

docs_dir="${repo_root}/docs"
venv_dir="${docs_dir}/.venv"
requirements_file="${docs_dir}/requirements.txt"

# Sanity checks
if [[ ! -d "${docs_dir}" ]]; then
    printf "%s\n" "Error: docs directory not found at ${docs_dir}." >&2
    exit 1
fi

# Create venv if needed
if [[ ! -d "${venv_dir}" ]]; then
    printf "%s\n" "Creating virtual environment in ${venv_dir}."
    python3 -m venv "${venv_dir}" || return 1

    source "${venv_dir}/bin/activate"

    python -m pip install --upgrade pip

    if [[ -f "${requirements_file}" ]]; then
        python -m pip install -r "${requirements_file}" || return 1
    else
        printf "%s\n" "Warning: requirements.txt not found in docs."
    fi
else
    source "${venv_dir}/bin/activate"
fi

printf "%s\n" "Activated docs virtual environment."

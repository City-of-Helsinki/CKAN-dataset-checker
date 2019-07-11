#!/bin/bash
cd "$( dirname "${BASH_SOURCE[0]}" )"

. $HOME/ckan-links/bin/activate

export LC_CTYPE="fi_FI.utf8"

python run_hri_checks.py

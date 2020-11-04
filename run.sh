#!/bin/sh

set -e

cd /Users/mike/work/git-repos/stuff/zeplin-download-recent

source .venv/bin/activate

python zeplin-download-screens.py
python figma-download-screens.py
# !/bin/bash

export WORK_PATH_MAIN="$( cd "$( dirname "${BASH_SOURCE[0]}" )" && pwd )"
cd $WORK_PATH_MAIN

source venv/bin/activate

pip freeze > requirements.txt 
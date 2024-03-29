#!/bin/bash
cd "$(dirname -- "$(dirname -- "$(readlink -f "$0")")")"

for cmd in black autopep8 isort; do
    if [[ ! -x "$(which "$cmd")" ]]; then
        echo "Could not find $cmd. Please make sure that black, autopep8, and isort are all installed."
        exit 1
    fi
done

# Order is important. There are a few things that black and autopep8 disagree on, and we want to go with
# autopep8 on those because it makes flake8 happy.
black tjhsst && autopep8 --in-place --recursive tjhsst && isort tjhsst

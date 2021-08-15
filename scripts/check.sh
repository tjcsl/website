#!/bin/bash
cd "$(dirname -- "$(dirname -- "$(readlink -f "$0")")")"

for cmd in flake8 isort pylint; do
    if [[ ! -x "$(which "$cmd")" ]]; then
        echo "Could not find $cmd. Please make sure that flake8, isort, and pylint are all installed."
        exit 1
    fi
done

flake8 tjhsst && isort --check tjhsst && pylint tjhsst

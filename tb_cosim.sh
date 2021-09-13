#!/bin/bash
set -e
ENTITY="adder"
DIR="/tmp/fusesoc_cosim_example/"
LOG_FILE="$ENTITY.log"
PYTHON_FILE="../../../fw/$ENTITY/tb/tb_cosim.py"

export PYTHONPATH="$PYTHONPATH:$PWD/../../agwb/$ENTITY/python/:$PWD/../../../sw/"

mkdir -p $DIR
if [ ! -f "$PYTHON_FILE" ]; then
	>&2 echo "$PYTHON_FILE not found"
	exit 1
fi
python3 $PYTHON_FILE > "$DIR$LOG_FILE" 2>&1 &

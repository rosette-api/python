#!/bin/bash
for f in *.py
do
    python $f --key $1
done

#!/bin/bash

f1="Beispiel.ahn"
f2="Beispiel_written_by_python.ahn"

hexdump -C $f1 > $f1.hex
hexdump -C $f2 > $f2.hex

diff $f1.hex $f2.hex

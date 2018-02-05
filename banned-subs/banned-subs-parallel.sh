#!/bin/bash

subsFile=../output/quarantined-subs
subreddits=$( wc -l < $subsFile )

# How many processes to run the program
processes=32

step=$(($subreddits / $processes + $processes + 1))
line=0


for process in $(seq 1 $processes)
do
  x-terminal-emulator --working-directory $PWD -e "python3 banned-subs.py $line $(($line+$step))"

  line=$(($line+$step))
done


# ESTIMATED TIME
## subs ≈ 380000
## requests ≈ 2 / sec
## processes = 32

## Time = 380000 / 2 / 32 = 5937 sec = 1.64 h

## Actual time = 6129 sec = 1.70 h

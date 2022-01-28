#!/bin/sh

make exe -j || exit -1

sh scripts/submit_all_signal.sh -r sr $@ &
sh scripts/submit_all_qcd.sh  -r sr $@ &
sh scripts/submit_all_ttbar.sh -r sr $@ &

wait $!

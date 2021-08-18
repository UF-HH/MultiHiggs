#!/bin/sh

make exe -j || exit -1

sh scripts/submit_all_data.sh -r cr $@ &
sh scripts/submit_all_qcd.sh  -r cr $@ &
sh scripts/submit_all_ttbar.sh -r cr $@ &

wait $!

#!/bin/bash

OUTPUT=$1
shift
INPUTS=$@

if [[ -z $OUTPUT || -z $INPUTS ]]; then
    echo """
Convert input filelists to python samples
Assumes that each filelist comes from the same DAS path
Will create samples as merged dictionary of all input filelists given
Usage: bash convert_input.sh /path/to/output/samples.py /path/to/input/filelist_1.txt /path/to/input/filelist_2.txt ...
    """
    exit
fi

echo "Inputs:  "
for INPUT in ${INPUTS[@]}; do
    echo "    $INPUT"
done
echo "Output: $OUTPUT"

TMPOUT=/tmp/convert_input.tmp.py

cat << EOF > $TMPOUT
from metis.Sample import DirectorySample, DBSSample

samples = {
EOF

for INPUT in ${INPUTS[@]}; do
    file=$(cat $INPUT | head -n 1)

    if [ ! $? ]; then
        continue
    fi

    file=${file/root:\/\/cmsxrootd.fnal.gov\//}

    das=$(dasgoclient --query="dataset file=$file")

    if [ ! $? ]; then
        continue
    fi

    sample=${das//\//_}
    sample="${sample:1}"

    echo " ... adding $das"
    echo "\"$sample\" : DBSample(dataset=\"$das\")," >> $TMPOUT

done

echo "}" >> $TMPOUT

mkdir -p $(dirname $OUTPUT)
mv $TMPOUT $OUTPUT

echo "done"
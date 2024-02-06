#!/bin/bash

OUTPUT=$1
shift
INPUTS=$@

if [[ -z $OUTPUT || -z $INPUTS ]]; then
    echo """
Merge python samples into a single file
Usage: bash merge_samples.sh /path/to/output/samples.py /path/to/input/sample_1.py /path/to/input/sample_2.py ...
    """
    exit
fi


echo "Inputs:  "
for INPUT in ${INPUTS[@]}; do
    echo "    $INPUT"
done
echo "Output: $OUTPUT"

TMPOUT=/tmp/merge_samples.tmp.py

cat << EOF > $TMPOUT
merged_samples = {}

EOF

for input in ${INPUTS[@]}; do 
    echo " ... adding $input"

cat << EOF >> $TMPOUT

# ---- $input

$(cat $input)

merged_samples.update(samples)

EOF
done

cat << EOF >> $TMPOUT

samples = dict(merged_samples)

EOF

mkdir -p $(dirname $OUTPUT)
mv $TMPOUT $OUTPUT

echo done
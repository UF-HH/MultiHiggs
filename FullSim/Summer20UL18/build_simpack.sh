#!/bin/sh

build_pack () {
    gridpack=$(basename $1)
    mx=$(echo $1 | grep -oP "MX_\d+" | grep -oP "\d+")
    my=$(echo $1 | grep -oP "MY_\d+" | grep -oP "\d+")
    simpack="NMSSM_XYY_YToHH_8b_MX_${mx}_MY_${my}"

    echo "... Creating Simpack for ${simpack}"
    mkdir -p ${simpack}
    cp -v Template/* ${simpack}
    cp -v $1 ${simpack}/${gridpack}
    sed -i "s/NMSSM_XYY_YToHH_8b_MX_800_MY_300/${simpack}/" ${simpack}/genSim_step.py
    sed -i "s/NMSSM_XYY_YToHH_8b_MX_800_MY_300/${simpack}/" ${simpack}/crabConfig.py
    echo "... Finished"
    echo
}

for gridpack in $@; do 
    build_pack $gridpack 
done
## THIS TO CHECK ON LD_LYBRARY_PATH: will work on screen but leave previous path in the config

# paths=$(echo $LD_LIBRARY_PATH | tr ":" "\n") # split on :
# pathunset=true
# for pp in $paths
# do
#     if [[ $pp == *"`pwd`/lib"* ]] ; then
#         echo "Warning: path to KLUB binaries already set to: $pp"
#         echo "         ... Ignoring this setup command"
#         pathunset=false
#     fi
# done

paths=$(echo $PATH | tr ":" "\n") # split on :
pathunset=true
for pp in $paths
do
    if [[ $pp == *"sixBanalysis/bin"* ]] ; then
        echo "Warning: path to sixBanalysis binaries already set to: $pp"
        echo "         ... Ignoring this setup command"
        pathunset=false
    fi
done

if [ "$pathunset" = true ] ; then
    export THISDIR=`pwd`

    ## note : the CPP_BOOST_PATH is also fed to the makefile to use the boost libraries under $(CPP_BOOST_PATH)/lib
    ## comment it to use system default libraries in compilation and linking 
    if [ -d /cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt ]; then
        export CPP_BOOST_PATH=/cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt
    fi
    
    export CPATH=${CPATH}:${CPP_BOOST_PATH}/include
    export CPATH=${CPATH}:${CMSSW_BASE}/src/
    export LD_LIBRARY_PATH=${LD_LIBRARY_PATH}:${THISDIR}/lib:${CPP_BOOST_PATH}/lib
    
    for ext in tensorflow protobuf eigen; do
	export TFINC="${TFINC} -I$(scram tool tag ${ext} include)"
	export LIBRARY_PATH=${LIBRARY_PATH}:$(scram tool tag ${ext} libdir)
    done
    

    

    
    ## NB: /cvmfs/sft.cern.ch/... is needed to source most recent boost libraries

    if [ -n "${DYLD_LIBRARY_PATH}" ] ; then
    # export DYLD_LIBRARY_PATH=/cvmfs/sft.cern.ch/lcg/views/LCG_89/x86_64-slc6-gcc62-opt/lib:${DYLD_LIBRARY_PATH}:${THISDIR}/lib
    export DYLD_LIBRARY_PATH=${THISDIR}/lib
    fi

    export PATH=${PATH}:${THISDIR}/bin
fi

IN_MX=$1
IN_MY=$2
IN_NEVT=$3
IN_ONAME=$4

PROCFOLDER=X_YH_HHH_6b

if [ -z "$IN_MX" ] || [ -z "$IN_MY" ]; then
    echo "Usage : source generate_LHE.sh mX mY [n_events=10000] [oname=gen6b_MX_MY]"
    echo "(parameters between square brackets are optional)"
    return 1
fi

if [ -z "$IN_NEVT" ];  then IN_NEVT=10000; fi
if [ -z "$IN_ONAME" ]; then IN_ONAME="gen6b_${IN_MX}_${IN_MY}"; fi

echo "[INFO] ... mX = ${IN_MX}, mY = ${IN_MY}"
echo "[INFO] ... will generate ${IN_NEVT} events"
echo "[INFO] ... ouput folder is $IN_ONAME"

SCRIPTSDIR=`pwd`
MG5DIR=${CMSSW_BASE}/src/sixB/MadGraph/MG5_aMC_v2_6_5

echo "[INFO] Launching event generation with MadGraph"
cd ${MG5DIR}/${PROCFOLDER}

./bin/generate_events ${IN_ONAME} <<EOF
0
set nevents ${IN_NEVT}
set MH03 ${IN_MX}
set MH02 ${IN_MY}
0

EOF

cd ${SCRIPTSDIR}
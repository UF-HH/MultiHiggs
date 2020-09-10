## run MG5 process

cmsenv # just in case

SCRIPTSDIR=`pwd`
MG5DIR=${CMSSW_BASE}/src/sixB/MadGraph/MG5_aMC_v2_6_5

echo "Scripts directory : ${SCRIPTSDIR}"
echo "MG5 directory     : ${MG5DIR}"

echo "[INFO] Launching process generation with MadGraph"

cd $MG5DIR
./bin/mg5_aMC ${SCRIPTSDIR}/configs/proc_card.dat

## now replace the param and run cards with the external ones (taken from CMSSW repo)
cd $SCRIPTSDIR

echo "[INFO] Replacing default cards with updated ones"

cp ${SCRIPTSDIR}/configs/run_card.dat  ${MG5DIR}/X_YH_HHH_6b/Cards
cp ${SCRIPTSDIR}/configs/param_card.dat  ${MG5DIR}/X_YH_HHH_6b/Cards


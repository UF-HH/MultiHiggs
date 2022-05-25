# set -e
# if submitting -b and -t, make sure -b is before -t !!!!

ODIR="/store/user/srosenzw/sixb/ntuples/Summer2018UL/"
CFG="config/skim_ntuple_2018.cfg"
TAG="bias/NMSSM"
EXTRA=""

ARGS=$(getopt -a --options npbo:c:t:d --long "jes:,jer:,no-cuts,presel,btag-ordered,odir:,cfg:,tag:dry-run" -- "$@")
eval set -- "$ARGS"

while true; do
  case "$1" in
      --jes)
         EXTRA+="--jes-shift-syst $2 "
         shift 2;;
      --jer)
         EXTRA+="--jer-shift-syst $2 "
         shift 2;;
      -n|--no-cuts)
         TAG="NMSSM_nocuts"
         CFG="config/skim_ntuple_2018_nocuts.cfg"
         shift;;
      -p|--presel)
         TAG="NMSSM_presel"
         CFG="config/skim_ntuple_2018_presel.cfg"
         shift;;
      -b|--btag-ordered) # order by b tag
         TAG="btag/NMSSM"
         CFG="config/skim_ntuple_2018_maxbtag.cfg"
         shift;;
      -o|--odir) # specify output directory
         ODIR="$2"
         shift 2;;
      -c|--cfg) # specify config file
         CFG="$2"
         shift 2;;
      -t|--tag) # specify tag
         TAG="$2"
         shift 2;;
      -d|--dry-run)
         EXTRA+="--dryrun"
         shift;;
      --)
      break;;
      *)
      printf "Unknown option %s\n" "$1"
      exit 1;;
  esac
done

make exe -j || exit -1

echo "... tag       : ", $TAG
echo "... cfg       : ", $CFG
echo "... saving to : ", $ODIR

relDir='input/PrivateMC_2018/NMSSM_XYH_YToHH_6b/'
files=$(ls ${relDir})
for input in ${files[@]}; do
    if [[ "$input" == "misc" ]]; then
        continue
    fi
    input="${relDir}${input}"
    python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 100 --input $input --is-signal --forceOverwrite "$EXTRA"
done

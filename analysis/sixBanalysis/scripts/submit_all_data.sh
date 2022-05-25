# set -e
# if submitting -b and -t, make sure -b is before -t !!!!

ODIR="/store/user/srosenzw/sixb/ntuples/Summer2018UL/"
CFG="config/skim_ntuple_2018.cfg"
TAG="bias/JetHT_Data_UL"
EXTRA=""

ARGS=$(getopt -a --options bo:c:t:d:f --long "btag-ordered,odir:,cfg:,tag:dry-run;force" -- "$@")
eval set -- "$ARGS"

while true; do
  case "$1" in
      -b|--btag-ordered) # order by b tag
         TAG="btag/JetHT_Data_UL"
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
      -f|--force)
         EXTRA+="--forceOverwrite"
         shift;;
      --)
      break;;
      *)
      printf "Unknown option %s\n" "$1"
      exit 1;;
  esac
done

make exe -j || exit -1

echo "... cfg       : ", $CFG
echo "... tag       : ", $TAG
echo "... saving to : ", $ODIR

python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 200 --input input/Run2_UL/2018/JetHT_Run2018_full.txt --is-data $EXTRA


# data_files=$(ls input/Run2_UL/2018/JetHT*)

# for input in ${data_files[@]}; do
#     python scripts/submitSkimOnBatch.py --tag $TAG --outputDir $ODIR --cfg $CFG --njobs 200 --input $input --is-data
# done

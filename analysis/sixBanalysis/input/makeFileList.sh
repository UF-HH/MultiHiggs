XRDSERVER="root://cmsxrootd.fnal.gov/"
SAMPLENAME=$1
OUTNAME=$2

# if OUTNAME is a directory, automatically build the filelist name from the dataset name
if [ -d "$OUTNAME" ] ; then
    PROCESS=$(echo $SAMPLENAME | tr "/" " " | awk '{print $1}')
    OUTNAME=$OUTNAME/${PROCESS}.txt
fi

if [ -z "$SAMPLENAME" ] ; then
    echo "... please provide a dataset name"
    echo "... usage: source makeFileList.sh DATASETNAME OUTPUTNAME"
    return
fi

if [ -z "$OUTNAME" ] ; then
    echo "... please provide a output file name"
    echo "... usage: source makeFileList.sh DATASETNAME OUTPUTNAME"
    return
fi

echo "... running on $SAMPLENAME"
echo "... saving output to $OUTNAME"
echo "... prepending server name $XRDSERVER"

# here we redirect with ">" instead of ">>" to avoid that files from a dataset are duplicated if the command is called twice
dasgoclient --query="file dataset=$SAMPLENAME" --unique > $OUTNAME
sed -i -e "s#^#$XRDSERVER#" $OUTNAME

NFILES=`cat $OUTNAME | grep .root | wc -l`
echo "... listed $NFILES to output"

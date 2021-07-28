XRDSERVER="root://cmsxrootd.fnal.gov/"
SAMPLENAME=$1
OUTNAME=$2

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

dasgoclient --query="file dataset=$SAMPLENAME" --unique > $OUTNAME
sed -i -e "s#^#$XRDSERVER#" $OUTNAME

NFILES=`cat $OUTNAME | grep .root | wc -l`
echo "... listed $NFILES to output"

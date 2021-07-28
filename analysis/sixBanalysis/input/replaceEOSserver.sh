FILETORUNON=$1

if [ -z "$FILETORUNON" ]; then
    echo "Please specify a file"
    return 1
fi

echo "Running on file : $FILETORUNON"
if [ ! -f $FILETORUNON ]; then
    echo "File does not exist"
    return 1
fi
# perl -i -pe 'BEGIN{undef $/;} s/{//}eos{//}uscms/root:{//}{//}cmsxrootd.fnal.gov{//}/smg' $FILETORUNON
sed -i.bak -e 's+/eos/uscms+root://cmsxrootd.fnal.gov/+g' $FILETORUNON
rm $FILETORUNON.bak

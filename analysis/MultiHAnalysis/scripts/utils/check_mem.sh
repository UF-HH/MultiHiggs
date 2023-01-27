## use top to follow the usage of memory of PROCNAME and save results to LOGNAME . Usage : 
## source check_mem.sh [logname] [procname]

LOGNAME='mem_log.txt'
PROCNAME='skim_ntuple'

if [ -n "$1" ]; then
    LOGNAME=$1
fi    

if [ -n "$2" ]; then
    PROCNAME=$2
fi    

echo "... will follow the process : $PROCNAME"
echo "... will save the output to : $LOGNAME"

rm ${LOGNAME}

top -b -n 1 | grep ${PROCNAME}
code=$?
while [ $code -eq 0 ]; do
    echo "`date`" >> ${LOGNAME}
    top -b -n 1 | grep ${PROCNAME} >> ${LOGNAME}
    code=$?
    echo "" >> ${LOGNAME}
    sleep 15s
done

echo "`date`" >> ${LOGNAME}
echo "all finished" >> ${LOGNAME}
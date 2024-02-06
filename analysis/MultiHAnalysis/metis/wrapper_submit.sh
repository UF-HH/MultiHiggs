#!/bin/bash
set -e

# ---- Make sure project is compiled 

make -q exe --silent || {
    echo "Project is not completely compiled"
    echo "Please run make in a fresh shell"
    echo "    make exe -j"
    exit 1
}

# ---- Install Metis

METIS_PATH=$HOME/workdir/ProjectMetis
if [ ! -d $METIS_PATH ]; then 
    echo "Installing Metis into $METIS_PATH"
    CWD=$PWD
    DIRNAME=$(dirname $METIS_PATH)
    mkdir -p $DIRNAME
    cd $DIRNAME

    git clone https://github.com/aminnj/ProjectMetis.git

    cd $CWD
fi

# ---- Init Arguments ---- #

VALID_SKIM=1
if [ -z $CONFIG ]; then
    echo Specify a skim config using the CONFIG env variable
    VALID_SKIM=0
elif [ ! -f $CONFIG ]; then
    echo CONFIG=$CONFIG does not exist
    VALID_SKIM=0
fi

if [ -z $SAMPLES ]; then
    echo Specify a skim sample using the SAMPLES env variable
    VALID_SKIM=0
elif [ ! -f $SAMPLES ]; then
    echo SAMPLES=$SAMPLES does not exist
    VALID_SKIM=0
fi

if [ -z $OUTPUT ]; then
    echo Specify a skim output using the OUTPUT env variable
    VALID_SKIM=0
fi

if [ -z $TAG ] ; then
    echo Specify a skim tag using the TAG env variable
    VALID_SKIM=0
fi

if [ $VALID_SKIM -eq 0 ]; then
    echo An error occured, please fix this before continuing
    exit 1
fi

# --- Setup Metis

voms-proxy-info -exists || {
    voms-proxy-init -hours 168 -voms cms -rfc # to setup proxy
}

if [ -z $METIS_BASE ]; then
    echo "Setting up Metis"
    source $METIS_PATH/setup.sh
fi

# ---- Build submission directory

JOBDIR=$PWD/jobs_metis/$OUTPUT/$TAG
TARFILE=$JOBDIR/project.tar.xz

if [ ! -d $PWD/jobs_metis ]; then
    mkdir -p $PWD/jobs_metis
    echo "*" > $PWD/jobs_metis/.gitignore
fi

mkdir -p $JOBDIR

if [ ! -f $TARFILE ]; then
    echo "Building Metis Submission Workspace"
    git log -n 1
    git status

    FILES_TO_TAR=(
        bin/
        lib/
        config/
        data/
        models/
    )

    echo "Building Tarball"
    tar -chJf $TARFILE $FILES_TO_TAR
    git log -n 1 > $JOBDIR/commit
fi

cp metis/condor_executable_metis.sh $JOBDIR
cp $SAMPLES $JOBDIR/samples.py
sed "s|\${OUTPUT}|$OUTPUT|g; s|\${CONFIG}|$CONFIG|g; s|\${TAG}|${TAG}|g" metis/submit.py > $JOBDIR/submit.py

echo "Finished Building Workspace"
echo "    $JOBDIR"

# ----

export METIS_JOBDIR=$JOBDIR
TMUX_SESSION=${OUTPUT}_${TAG}

echo "Submitting samples in tmux"
tmux new-session -d -s $TMUX_SESSION
tmux send-keys -t $TMUX_SESSION 'cd ${METIS_JOBDIR}; python submit.py' Enter

echo "Attach tmux session with"
echo "    tmux attach-session -t $TMUX_SESSION"
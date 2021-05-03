#Usage: bash install.sh [SCSPKG_ROOT]
#!/bin/bash

if [ $# -lt 1 ]; then
  SCSPKG_ROOT=`pwd`
else
  SCSPKG_ROOT=$1
  if [ -d ${SCSPKG_ROOT}]; then
    echo "${SCSPKG_ROOT} exists. Are you sure you want to override the current installation (y/n)?"
    read OVERRIDE
    if [ $OVERRIDE -neq "y"]; then
      exit
    fi
  fi
fi

mkdir -p ${SCSPKG_ROOT}
cp -r . ${SCSPKG_ROOT}
echo export SCSPKG_ROOT=${SCSPKG_ROOT} >> ~/.bashrc
echo export PATH=${SCSPKG_ROOT}/bin:$PATH >> ~/.bashrc
module use ${SCSPKG_ROOT}/modulefiles
mkdir ${SCSPKG_ROOT}/packages
mkdir ${SCSPKG_ROOT}/modulefiles
mkdir ${SCSPKG_ROOT}/modulefiles_json

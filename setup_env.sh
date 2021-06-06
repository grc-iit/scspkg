#Usage: bash connect.sh [SCSPKG_ROOT]
#!/bin/bash

if [ $# -lt 1 ]; then
  SCSPKG_ROOT=`pwd`
else
  SCSPKG_ROOT=$1
fi

echo export SCSPKG_ROOT=${SCSPKG_ROOT} >> ~/.bashrc
echo export PATH=${SCSPKG_ROOT}/bin:$PATH >> ~/.bashrc
module use ${SCSPKG_ROOT}/modulefiles
source ~/.bashrc

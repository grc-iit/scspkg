#Usage: bash connect.sh [SCSPKG_ROOT]
#!/bin/bash

if [ $# -lt 1 ]; then
  SCSPKG_ROOT=`pwd`
else
  SCSPKG_ROOT=$1
fi

echo export SCSPKG_ROOT=${SCSPKG_ROOT} >> ~/.bashrc
echo export PATH=${SCSPKG_ROOT}/bin:$PATH >> ~/.bashrc
if ! command -v module &> /dev/null
then
    echo "Warning: environment modules not installed"
else
    module use ${SCSPKG_ROOT}/modulefiles
fi
source ~/.bashrc

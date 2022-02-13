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
  mkdir -p ${SCSPKG_ROOT}
  cp -r . ${SCSPKG_ROOT}
fi

echo export SCSPKG_ROOT=${SCSPKG_ROOT} >> ~/.bashrc
echo export PATH=${SCSPKG_ROOT}/bin:"\$PATH" >> ~/.bashrc
mkdir ${SCSPKG_ROOT}/packages
mkdir ${SCSPKG_ROOT}/modulefiles
mkdir ${SCSPKG_ROOT}/modulefiles_json
source ~/.bashrc
if ! command -v module &> /dev/null
then
    echo "Warning: environment modules not installed, will install now"
    scspkg create modules
    cd `scspkg pkg-src modules`
    curl -LJO https://github.com/cea-hpc/modules/releases/download/v4.7.1/modules-4.7.1.tar.gz
    tar xfz modules-4.7.1.tar.gz
    cd modules-4.7.1
    ./configure --prefix=`scspkg pkg-root modules`
    make
    make install
    echo "source \`scspkg pkg-root modules\`/init/bash" >> ~/.bashrc
    echo "module use \`scspkg modules-path\`" >> ~/.bashrc
    source ~/.bashrc
else
    echo "module use \${SCSPKG_ROOT}/modulefiles" >> ~/.bashrc
fi

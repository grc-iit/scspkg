#Usage: bash install.sh [SCSPKG_ROOT]
#!/bin/bash

#Detect the distribution
if command -v apt &> /dev/null
then
  IS_DEBIAN=true
fi

if command -v yum &> /dev/null
then
  IS_RED_HAT=true
fi

#SCSPKG ROOT AND PATH
export SCSPKG_ROOT=`pwd`
export PATH=${SCSPKG_ROOT}/bin:$PATH

#Add to bashrc
echo "export SCSPKG_ROOT=${SCSPKG_ROOT}" >> ~/.bashrc
echo "export PATH=${SCSPKG_ROOT}/bin:\$PATH" >> ~/.bashrc
source ~/.bashrc

#Check if this is an existing installation
echo ${SCSPKG_ROOT}/packages
if [ -d ${SCSPKG_ROOT}/packages ]
then
  echo "Warning: this SCSPKG seems to be initialized"
fi

#Create initial directories
mkdir ${SCSPKG_ROOT}/packages
mkdir ${SCSPKG_ROOT}/modulefiles
mkdir ${SCSPKG_ROOT}/modulefiles_json

#Install TCLSH
if ! command -v tclsh &> /dev/null
then
  echo "Warning: tclsh was not installed, will install now"
  if $IS_DEBIAN
  then
    sudo apt install -y tcl-dev python3 python3-pip
  elif $IS_RED_HAT
  then
    sudo yum install -y tcl-devel python3 python3-pip
  else
    echo "Error: only apt and yum are supported in this script. Sorry."
    exit
  fi
  sudo pip3 install --upgrade pip
fi

#Install enviornment-modules
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
else
    echo "module use \${SCSPKG_ROOT}/modulefiles" >> ~/.bashrc
fi

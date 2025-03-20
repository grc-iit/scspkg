# SCSPKG

SCSPKG provides an infrastructures for installing packages manually.
It provides a structure to modulefiles so that you don't have to build them manually.
It's useful for when you're developing things or when spack fails.
We will go through an example which installs zlib.

## Dependencies

SCSPKG wraps around the system's installation of modules.
If your system doesn't have this, you'll need to install 
to make use of this tool. To check if your system has modules,
run the following command:

```bash
module avail
```

It it succeeds, skip this section.

### Install LMOD

There are two major implementations of modules: 
``LMOD`` and ``Environment Modules``.

To install LMOD, follow this [guide](https://lmod.readthedocs.io/en/latest/030_installing.html).
LMOD is recommended -- only use environment modules if that's what your system
comes with. We'll repeat the steps used for installing on Ubuntu + bash here.
LMOD is installed differently for different distros and different shell types.

```bash
sudo apt -y install lmod
nano ~/.bashrc
```

In your bashrc, append:
```bash
if ! shopt -q login_shell; then
  if [ -d /etc/profile.d ]; then
    for i in /etc/profile.d/*.sh; do
      if [ -r $i ]; then
        . $i
      fi
    done
  fi
fi
```


## Installation

### Clone the IoWarp Spack Repo
```bash
cd ${HOME}
git clone https://github.com/iowarp/iowarp-install.git
spack repo add iowarp-install/iowarp-spack
```

### Install SCSPKG
```bash
spack install py-ppi-scspkg
```

Spack packages must be loaded to use them.
You'll have to do this for each new terminal.
```bash
spack load py-ppi-scspkg
```

### Setting up terminal

We need to ensure that LMOD will search for your modules:

```bash
SCSPKG_MODULE_DIR=$(scspkg module dir)
echo "module use ${SCSPKG_MODULE_DIR}" >> ~/.bashrc
module use ${SCSPKG_MODULE_DIR}
```

### Initializing SCSPKG configuration

Create the scspkg configuration file.
```bash
scspkg init
```

This will create a directory ``~/.scspkg``, which is
where your modulefiles will all be stored.

## EXAMPLE: Creating a modulefile
Say you want to install zlib manually:
```bash
scspkg create zlib
cd $(scspkg pkg src zlib)
wget https://www.zlib.net/zlib-1.3.tar.gz
tar -xzf zlib-1.3.tar.gz
cd zlib-1.3
./configure --prefix=$(scspkg pkg root zlib)
make -j8 install
```

You can now run the following, and your environment
will be updated:
```bash
module load zlib
```

## Using the modulefiles

```bash
module avail #List of available modules
module list #List of currently running modules
module load [package] #Load a module corresponding to a package
module unload [package] #Unload a module
module purge #Unload all modules
```

## Uninstallation

```bash
scspkg reset
```

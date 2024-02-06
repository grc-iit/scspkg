A simple tool for building modulefiles and testing build scripts before building 
a spack script. It's also useful for when spack fails. 
More detailed doucmentation for its usage is [here](https://github.com/scs-lab/scspkg/wiki).

# 0.1. Dependencies

1. [jarvis-util](https://github.com/grc-iit/jarvis-util): a library which contains various utilities to aid with creating shell scripts within Python.
2. LMOD or environment modules

## 0.1.2. Install LMOD or Environment Modules

If your machine does not have module support, then install
[LMOD](https://lmod.readthedocs.io/en/latest/030_installing.html). 
LMOD is recommended as it has a few more features, although environment
modules is compatible with SCSPKG as well. 

We'll repeat the steps used for installing on Ubuntu + bash here.
LMOD is installed differently for different distros and different shell types.

```
sudo apt -y install lmod
nano ~/.bashrc
```

In your bashrc, append:
```
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

# 0.2. Installation

```bash
cd /path/to/scspkg
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
SCSPKG_MODULE_DIR=`scspkg module dir`
echo "module use ${SCSPKG_MODULE_DIR}" >> ~/.bashrc
```

IMPORTANT NOTE: Sometimes adding "module use" to bashrc doesn't work.
The module program may not be quite loaded during bashrc. If you find
your custom modules don't work, do the following:

```bash
module use `scspkg module dir` 
```

# 0.3. Setup

After installing, you'll have to bootstrap scspkg.

If using LMOD for environment variables:
```
scspkg init
```

If using Environment Modules (tcl):
```
scspkg init False
```

If you don't know whether LMOD or Environment Modules is installed, assume 
Environment Modules. LMOD is compatible with Environment Module scripts.

# 0.4. Using the modulefiles

```{bash}
module avail #List of available modules
module list #List of currently running modules
module load [package] #Load a module corresponding to a package
module unload [package] #Unload a module
module purge #Unload all modules
```

# 0.5. Uninstallation

```
scspkg reset
```
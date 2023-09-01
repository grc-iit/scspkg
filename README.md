# SCSPKG

A simple tool for building modulefiles and testing build scripts before building 
a spack script. It's also useful for when spack fails. 
The wiki is [here](https://github.com/scs-lab/scspkg/wiki).

## 0.1. Dependencies

### 0.1.1. Jarvis-Util
SCSPKG depends on [jarvis-util](https://github.com/scs-lab/jarvis-util).
It's a library which contains wrappers around shell commands.

```bash
git clone https://github.com/scs-lab/jarvis-util.git
cd jarvis-util
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
```

### 0.1.2. LMOD or Environment Modules

To install LMOD, follow this [guide](https://lmod.readthedocs.io/en/latest/030_installing.html).
LMOD is recommended -- only use environment modules if that's what your system
comes with. We'll repeat the steps used for installing on Ubuntu + bash here.
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

## 0.2. Installation

```bash
cd /path/to/scspkg
python3 -m pip install -r requirements.txt
python3 -m pip install -e .
echo "module use \`scspkg modules path\`" >> ~/.bashrc
```

## 0.3. Setup

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

## 0.4. Using the modulefiles

```{bash}
module avail #List of available modules
module list #List of currently running modules
module load [package] #Load a module corresponding to a package
module unload [package] #Unload a module
module purge #Unload all modules
```

## 0.5. Uninstallation

```
scspkg reset
```
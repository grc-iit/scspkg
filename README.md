# SCSPKG

A simple tool for building modulefiles and testing build scripts before building a spack script.

## Dependencies

* Python3
* tclsh
* Environment Modules
* jarvis-cd

These dependencies are automatically installed using install.sh for debian-based and red-hat based distros.

## Installation / Environment Setup

If there is no version currently installed:
```{bash}
cd /path/to/scspkg
bash install.sh
source ~/.bashrc
```

### Uninstallation

```{bash}
rm -rf $SCSPKG_ROOT
#Remove export commands from ~/.bashrc
```

## Usage

### Creating a Package

A package is simply a location where the application files will be installed.  

Packages will be placed under ${SCSPKG_ROOT}/packages and their modulefiles will
be placed under ${SCSPKG_ROOT}/modulefiles.  

When installing your custom package, you can install its data into the package
path, which is discovered using "scspkg path [package]".

You can edit the modulefile by editing the json file found using "scspkg schema-path [package]".

```{bash}
scspkg list
scspkg create package1 ... packageN
scspkg remove package1 ... packageN
scspkg add_deps package dep1 ... depN
scspkg rm_deps package dep1 ... depN
scspkg pkg-root package1 ... packageN
scspkg pkg-src package1 ... packageN
scspkg schema-path package1 ... packageN
scspkg show-schema package1 ... packageN
```

### Using the modulefiles

```{bash}
module avail #List of available modules
module list #List of currently running modules
module load [package] #Load a module corresponding to a package
module unload [package] #Unload a module
module purge #Unload all modules
```

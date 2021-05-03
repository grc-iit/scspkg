# SCSPKG

A simple tool for building modulefiles and testing build scripts before building a spack script.

## Dependencies

* Python3
* Environment Modules

### Enviornment Modules

```{bash}
spack install environment-modules
spack load environment-modules
source /etc/profile.d/modules.sh
```

## Existing Installation

If there is a version of SCSPKG currently installed, add it to your environment
```{bash}
bash setup_env.sh [INSTALL_DIR]
source ~/.bashrc
```

## New Installation

If there is no version currently installed:
```{bash}
bash install.sh [INSTALL_DIR]
source ~/.bashrc
```

### Uninstallation

```{bash}
rm -r $SCSPKG_ROOT
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
scspkg create [package] #Create an empty package
scspkg remove [package] #Deletes the package permanently (including source)
scspkg add_dep [package] dep ... #Add a dependency to a module
scspkg rm_dep [package] dep ... #Remove a dependency from a module (but will not unload it)
scspkg path [package] #Return the location of the package folder (used for setting prefixes when building; e.g., CMAKE_INSTALL_PREFIX)
scspkg schema-path [package] #Return the location of the package modulefile schema (for custom edits)
```

### Using the modulefiles

```{bash}
module avail #List of available modules
module list #List of currently running modules
module load [package] #Load a module corresponding to a package
module unload [package] #Unload a module
module purge #Unload all modules
```

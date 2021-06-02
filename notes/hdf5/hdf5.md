# Install HDF5 from source

## Create SCSPKG

```{bash}
scspkg create orangefs-hdf5
cd `scspkg pkg-src orangefs-hdf5`
```

## Dependencies

```{bash}
spack load gcc@9.3.0
spack unload gcc@9.3.0
```

```{bash}
module add_deps orangefs-hdf5 orangefs-mpich
module load orangefs-mpich
```

## Installation

Install Hdf51.8.20 in serial
```{bash}
wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-1.8.20/src/hdf5-1.8.20.tar.gz
tar -xavf hdf5-1.8.20.tar.gz
cd hdf5-1.8.20
./configure --prefix=`scspkg pkg-root orangefs-hdf5` --enabled-shared
make
make install
```

Install Hdf51.8.20 in parallel
```{bash}
wget https://support.hdfgroup.org/ftp/HDF5/releases/hdf5-1.8/hdf5-1.8.20/src/hdf5-1.8.20.tar.gz
tar -xavf hdf5-1.8.20.tar.gz
cd hdf5-1.8.20
./configure --prefix=`scspkg pkg-root orangefs-hdf5` --enabled-shared
make
make install
```

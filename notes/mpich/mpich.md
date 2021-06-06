# How to Install MPICH from source (with orangefs)

## Dependencies

```{bash}
spack load gcc@9.3.0
spack unload gcc@9.3.0
```

## Install MPICH
```{bash}
scspkg create orangefs-mpich
cd `scspkg pkg-src orangefs-mpich`
wget http://www.mpich.org/static/downloads/3.2/mpich-3.2.tar.gz
tar -xzf mpich-3.2.tar.gz
cd mpich-3.2
./configure --prefix=`scspkg pkg-root orangefs-mpich` --enable-romio --enable-shared --with-pvfs2=/opt/ohpc/pub/orangefs --with-file-system=pvfs2
make -j8
make install
```

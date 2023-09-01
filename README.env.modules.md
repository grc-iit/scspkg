
This guide documents how to install Environment Modules

# Dependencies

```
sudo apt install -y tcl-dev python3 python3-pip
sudo yum install -y tcl-devel python3 python3-pip
```

# Install
```
scspkg create modules
cd `scspkg pkg src modules`
curl -LJO https://github.com/cea-hpc/modules/releases/download/v4.7.1/modules-4.7.1.tar.gz
tar xfz modules-4.7.1.tar.gz
cd modules-4.7.1
./configure --prefix=`scspkg pkg root modules`
make
make install
echo "source \`scspkg pkg root modules\`/init/bash" >> ~/.bashrc
echo "module use \`scspkg modules path\`" >> ~/.bashrc
```
#!/bin/bash
export CONDA_URL=https://repo.continuum.io/miniconda/Miniconda3-latest-Linux-x86_64.sh

unamestr=`uname`
if [[ "$unamestr" == 'Darwin' ]];
then
   echo "Using OSX Conda"
   export CONDA_URL=https://repo.anaconda.com/miniconda/Miniconda3-latest-MacOSX-x86_64.sh
   export CPU_ONLY=1
   sed -i '' "1s/.*/__version__\ =\ \"$DATE\"/" ligand_ml/__init__.py
else
   sed -i "1s/.*/__version__\ =\ \"$DATE\"/" ligand_ml/__init__.py
fi

wget ${CONDA_URL} -O anaconda.sh;
bash anaconda.sh -b -p `pwd`/anaconda
export PATH=`pwd`/anaconda/bin:$PATH
conda install requests pandas matplotlib seaborn jinja2

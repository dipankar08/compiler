echo ' Installing software.....'
sudo apt-get install gcc
sudo apt-get install g++
sudo apt-get install default-jdk

sudo apt-get install python-setuptools
sudo easy_install virtualenv

echo '[MUST] You must run this file at least once ...'
echo '[INFO] Copying Header file in temp ....'
cp -r ./lib/*.* /tmp/
echo '[INFO] Conpying config files...'
cp -r ./lib/gdbinit ~/.gdbinit

echo '[INFO] Staring virtiual env  in python 3  \n\n]n'
virtualenv  -p python3  venv_compiler
source venv_compiler/bin/activate
which python
python --version
sudo python -m pip install tornado
#python -m pip install pymongo
pip list
sudo python server.py

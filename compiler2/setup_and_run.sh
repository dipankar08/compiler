echo '[MUST] You must run this file at least once ...'
echo '[INFO] Copying Header file in temp ....'
cp -r ./lib/*.* /tmp/
echo '[INFO] Conpying config files...'
cp -r ./lib/gdbinit ~/.gdbinit

sudo pip install virtualenv
virtualenv --python=/usr/bin/python  venv_compiler
source venv_compiler/bin/activate
which python
python -m pip install tornado
python -m pip install pymongo
pip list
sudo python server.py

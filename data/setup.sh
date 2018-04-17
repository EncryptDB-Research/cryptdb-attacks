# install python deps to run the insert scripts
apt-get update \
&& apt-get install -y python-pip python-pandas python-numpy \
&& pip install --upgrade pip \
&& pip install -r $EDBDIR/data/requirements.txt
&& python insert.py
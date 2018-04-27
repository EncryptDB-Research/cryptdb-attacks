# created by Joannier Pinales

# install python deps to run the insert scripts
export TERM=xterm

apt-get update \
&& apt-get install -y python-pip python-pandas python-numpy python-mysqldb \
&& pip install --upgrade pip \
&& pip install -r $EDBDIR/data/requirements.txt
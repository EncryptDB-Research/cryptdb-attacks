apt-get update \
&& apt-get install -y python-pip python-pandas python-numpy \
&& pip install --upgrade pip \
&& pip install -r ./requirements.txt \
&& python insert.py
&& python insert_sensitive.py
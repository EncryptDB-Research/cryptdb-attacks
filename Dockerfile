## Created by Joannier Pinales
## Sets up the Docker image with cryptdb installed.

# ubuntu:14.04
FROM ubuntu:14.04

LABEL cryptdb='1.0'

# make sure the package repository is up to date
RUN apt-get update

# Install stuff
RUN apt-get install -y ca-certificates supervisor sudo ruby git vim less net-tools gdb --fix-missing

RUN mkdir -p /var/log/supervisor

RUN echo 'root:root' |chpasswd

# Set Password of MySQL root
ENV MYSQL_PASSWORD letmein

# Install MySQL Server in a Non-Interactive mode. Default root password will be $MYSQL_PASSWORD
RUN echo "mysql-server mysql-server/root_password password $MYSQL_PASSWORD" | debconf-set-selections
RUN echo "mysql-server mysql-server/root_password_again password $MYSQL_PASSWORD" | debconf-set-selections
RUN DEBIAN_FRONTEND=noninteractive apt-get -y install mysql-server mysql-client

RUN sed -i -e"s/^bind-address\s*=\s*127.0.0.1/bind-address = 0.0.0.0/" /etc/mysql/my.cnf
RUN /usr/sbin/mysqld & sleep 10s && echo "GRANT ALL ON *.* TO root@'%' IDENTIFIED BY 'letmein' WITH GRANT OPTION; FLUSH PRIVILEGES"

# Clone project repository
RUN git clone https://github.com/EncryptDB-Research/cryptdb-seed.git /opt/cryptdb

# adding data file
ADD ./data /opt/cryptdb/data/

# chaning working dir
WORKDIR /opt/cryptdb

RUN apt-get remove bison libbison-dev

RUN cd packages \
    && apt-get -y install m4 \
    && dpkg -i libbison-dev_2.7.1.dfsg-1_amd64.deb \
    && dpkg -i bison_2.7.1.dfsg-1_amd64.deb \
    && cd ..

RUN apt-get update


USER root

# instal cryptdb
RUN scripts/install.rb . 

RUN echo "\
[supervisord]\n\
nodaemon=true\n\
\n\
[program:mysql]\n\
command=service mysql start\n\
\n\
" > /etc/supervisor/conf.d/supervisord.conf

RUN touch /opt/cryptdb/mysqlproxy/freqs 

ENV TERM xterm

ENV EDBDIR /opt/cryptdb

ENV LD_LIBRARY_PATH $EDBDIR/obj/

CMD ["/usr/bin/supervisord"]

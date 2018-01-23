# CryptDB_Docker_SEED

## This repo contains the main cryptdb dockerfile, 
## We are using a version of cryptdb that is updated to ubuntu 16.04 https://github.com/yiwenshao/Practical-Cryptdb

## How to setup (From the github readme):

##### 1. Make sure to have Docker installed

http://docs.docker.com/v1.8/installation/

###### This setup is for Linux. For OS X and Windows, install Docker Toolbox and skip the sudo part of the commands.

##### 2. Create a folder, clone project and navigate to folder containing the Dockerfile

    git clone https://github.com/agribu/Practical-Cryptdb_Docker.git

##### 3. Build docker image

    sudo docker build -t **name-of-image**:**version** **.**

    #Example:
    sudo docker build -t cryptdb:v1 .
    
    #To build without caching use:
    sudo docker build --no-cache=true -t cryptdb:v1 .

(Open the Docker Quickstart Terminal if OS X or Windows)


## How to run the program

#### AutoRun:

sudo ./run.sh

This runs the docker container then opens the command line inside the docker container
After exiting the comand line the script stops the docker container then removes it

#### Manual Run

##### 4. Run docker container based built image

    sudo docker run -d --name **name-of-container** -p **port-in**:**port-out** -p **port-in**:**port-out** -e MYSQL_ROOT_PASSWORD='letmein' **name-of-image**:**version**

    #Example:
    sudo docker run -d --name cryptdb_v1 -p 3306:3306 -p 3399:3399 -e MYSQL_ROOT_PASSWORD='letmein' cryptdb:v1

(Important: The password must be 'letmein')

##### 5. For accessing a docker container, use

    sudo docker exec -it **name-of-container** bash

    #Example:
    sudo docker exec -it cryptdb_v1 bash



## How to start encryptdb inside the container bash:

```
./cdbserver.sh
./cdbclient.sh
```

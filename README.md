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

## How to run docker

#### Auto Run:

sudo ./run.sh

This runs the docker container then opens the command line inside the docker container
After exiting the comand line the script stops the docker container

#### Manual Run

##### 1. Run docker container based built image

    sudo docker run -d --name cryptdb_v1 -p 3306:3306 -p 3399:3399 -e MYSQL_ROOT_PASSWORD='letmein' cryptdb:v1

(Important: The password must be 'letmein')

## How to acccess docker shell

    sudo docker exec -it cryptdb_v1 bash

## How to start Cryptdb inside the docker shell:

##### if running for the first time, you must run the following commands to insert the generated data into the database:

```
bash proxy.sh
bash scripts/setup.sh
export EBDIR=/opt/cryptdb/
export LD_LIBRARY_PATH=$EDBDIR/obj/
export CRYPTDB_PROXY_DEBUG=true
export CRYPTDB_MODE=single
export CRYPTDB_DB=MedicalS
echo $CRYPTDB_DB $CRYPTDB_PROXY_DEBUG $CRYPTDB_MODE $EDBDIR $LD_LIBRARY_PATH
```
##### To run cryptdb client and server use the following commands
Server
```
bash proxy.sh
```
Client
```
mysql -u root -pletmein -h 127.0.0.1 -P 3307

```

## How do we run the attacks?

We created two insertion scripts, one insert data normally and the other one inserts data using cryptdb sensitive annotations. Using pandas data frame with load up ~50k records of names but only insert about ~5k non-unique . Depending on the type of attack that we might want to test against we can keep one of the columns with unique values which will be ~1.9k records. Before inserting each data item we create a data set of patient records with 4 diseases, cancer, pneumonia, headache and flu, we then add them to the records about to be inserted with a desired distrubion for later comparison. 

After all the data is inserted we login through mysql and run a couple queries to test that the insertion step worked. Then we run a query to take of the random layer from the illness column with the 4 distinct values to leave it at the DET layer. Then we use a python script that we created to run the frequency analyser on this column. Before we created the fake insertion we get a perfect frequency matct. 

## Functionalities added to cryptdb

Fake data insertion in the wrapper lua that communicates to cryptdb. We created two main functions to intersect the query from the user
and modify it to insert fake data and mark each data row. Then we also created a filter function that after the results are back from the servers
takes out any fake data. These functions can be found in the lua wrapper file: **create_table_checker** and **lazy_active_smooth**. The filtering happens in the results codeblock on **next_handle**.



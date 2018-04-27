# Cryptdb Seed Setup

## This repo contains the Dockerfile that donwloads and installs cryptdb, python scripts to insert data and research papers published by cryptdb developers.

##  The cryptdb code base was forked from https://github.com/CryptDB/cryptdb to https://github.com/EncryptDB-Research/cryptdb-seed where it was modified.

## How to get started using Docker:

#### 1. Install Docker from https://docs.docker.com/install/

#### 2. Clone down the docker repo https://github.com/EncryptDB-Research/cryptdb-attacks

    git clone https://github.com/EncryptDB-Research/cryptdb-attacks
    cd cryptdb-attacks

#### 3. Build docker image (Open the Docker Quickstart Terminal if using OS X or Windows)

    sudo docker build -t cryptdb:v1 .
    
    #To build without caching use:
    sudo docker build --no-cache=true -t cryptdb:v1 .

This will create a docker image using ubuntu 14.04 with cryptdb installed inside. Then we can run this image as a virtual machine.

#### 4. Running Docker

Option 1: Autorun
    
    sudo ./run.sh


This runs docker container and then opens the command line inside the vm. If you exit from here the run commands auto stops the vm.

Option 2: Manual Run

    docker run --name cryptdb_v1 --volume $(pwd)/data:/opt/cryptdb/data/ -d -p 3306:3306 -p 3307:3307 -e MYSQL_ROOT_PASSWORD='letmein' cryptdb:1.0

The password must be `letmein`. This will run the docker container but we still have to login into the command line inside by doing

    sudo docker exec -it cryptdb_v1 bash


## How to get started in a regular VM

#### 1. Downloading and installing required software.
* Download and install VirtualBox from https://www.virtualbox.org/wiki/Downloads
* Download a desktop image of Ubuntu14 from http://releases.ubuntu.com/14.04/
* Open VirtualBox and create a new machine
	* Type: Linux
	* Version: Ubuntu
	* Hard disk: Create a virtual hard disk now
	* Allocation of 15GB is recommended

#### 2. Set up the machine using the Ubuntu14 image
* Select the new machine, and click start
* Select the ubuntu image, if not already selected, and click start
* Once the machine boots, follow on-screen instructions to install Ubuntu

#### 3. Updating the software
* On first reboot, the system will prompt you to upgrade to the newer Ubuntu16. Decline
* To update the system, there are two options:
	* I. Launch software updater
	* II. Launch terminal, and use the commands:

        ```
	    sudo apt update
	    sudo apt upgrade
        ```
				
#### 4. Downloading and installing required software for CryptDB

Clone the main repo 
 
    sudo apt install git
    git clone https://github.com/EncryptDB-Research/cryptdb-attacks
    
In terminal, navigate to the cryptdb-attacks folder and run setup.sh

    cd cryptdb-attacks
    sudo ./setup.sh

This will install bison2.7, ruby, git, apache2, php5, download our copy of cryptdb and installs it.

#### 5. (Optional) To install the webview, run 

    sudo cp -r ~/cryptdb-attacks/webview/ /var/www/html/

This will copy the webview directory to the apache root
To use webview, launch the browser, and go to **localhost/webview**
	
## Running Cryptdb

#### 1. Running the server and client

Server

    bash proxy.sh

Client

    bash client.sh 

Each of these commands is required to be ran in two separate terminals. If your computer does not have mysql client, then open a second terminal inside docker  running the following command from your regular computer terminal.

    sudo docker exec -it cryptdb_v1 bash

Then run the client command stated earlier. If you are using a regular VM instead of docker then just run the client command in one of the VM's terminals.    

If you would like to run everything in one terminal then do

    bash proxy &
    bash client.sh

Two separate terminals is highly recommended to see cryptdb's server output.

Note: In order for cryptdb to work with its default configurations, MySQL password should be **letmein**

## Inserting data with python  (Optional)

#### 1. Install python dependencies 

    bash ./data/setup.sh

This will install the necessary python dependencies

#### 2. Run the following commands to insert the data

    cd data
    # regular insertion
    python insert.py
    # sensitive insertion
    python insert_sensitive.py


## Running frequency attacks

We created two insertion scripts, one insert data normally and the other one inserts data using cryptdb sensitive annotations. Using pandas data frame the scripts load up ~5k records of names that get inserted to the database. Some other times we also use ~1.9k unique name records records. Before inserting each data item we create a data set of patient records with 4 diseases, cancer, pneumonia, headache and flu, we then add them to the records about to be inserted with a desired distribution for later comparison after the attack. After all the data is inserted we login through mysql and run a couple queries to test that the insertion step worked. Then we run a query to take off the random layer from the illness to leave it at the DET layer. Then we use `stats.py` to run the frequency analysis on this column. 

To run the attack do the following after the data is inserted. Inside mysql client shell run

    use Medical; # or MedicalS which is created by insert_sensitive.py script
    select * from records where illness='cancer';

This will peel off the random layer from the `illness` column and put it at DET. To confirm this, run the below command, it will show the `illness` column at the DET level.

    set @cryptdb='show';

After this, close mysql client and run the `stats.py` file in the data folder. From here on there's a little bit of guessing, since the table and column names are encrypted, but usually we find what the columns after a following these steps. 

While the script is running: 

1. Select database we which to analyse (Most likely `Medical`)
2. Pick the first encrypted table name. 
3. From the list of encrypted columns, pick one that contains `oEQ` in the name (which stands for equality or DET). Then the script will give a count of distinct values in the column, 
4. If the unique count is equal the total count then the layer still at RND, so we try a different column name that contains `oEQ`.  If we ran out of columns with `oEQ` then go back to the table selection and select a different table.
5. We repeat step 4 until we find the column that has only 4 unique values
6. Then the script will prompt to save the frequencies, select yes and check the file to see the frequencies obtained from the column. 

Note: We know beforehand that we only have 4 unique values but in a real attack, the attacker would stop when the unique count is not equal the total count. 


## Functionalities added to cryptdb

Fake data insertion in the wrapper lua that communicates to cryptdb. We created two main functions to intersect the query from the user
and modify it to insert fake data and mark each data row. Then we also created a filter function that after the results are back from the servers
takes out any fake data. These functions can be found in the lua wrapper file: `create_table_checker` and `lazy_active_smooth`. The filtering happens in the results codeblock on `next_handler`.

## TODOS:

1. Create an annotation for the user to specify which columns should be auto adjusted.
2. Implement Remove and Update queries to not affect the histogram.
3. Look into random insertion instead of keeping the histogram flat, this will create a randomized histogram
4. Store frequencies in the database trough cryptdb with RND layer for maximun security
5. Look into deleting fake data without compromising security
6. Make the query parser more robust
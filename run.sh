# created by Joannier Pinales
if [ -z $(docker ps -a -q -f name=cryptdb_v1) ]
then
    docker run --name cryptdb_v1 --volume $(pwd)/data:/opt/cryptdb/data/ --volume $(pwd)/../cryptdb-seed/mysqlproxy:/opt/cryptdb/mysqlproxy/ -d -p 3306:3306 -p 3307:3307 -e MYSQL_ROOT_PASSWORD='letmein' cryptdb:1.0
else
    docker start cryptdb_v1
fi

sleep 1

docker exec -it cryptdb_v1 bash

docker stop cryptdb_v1
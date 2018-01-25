docker run --name cryptdb_v1 -d --rm -p 3306:3306 -p 3399:3399 -e MYSQL_ROOT_PASSWORD='letmein'  cryptbdb:1.0

sleep 5

docker exec -it cryptdb_v1 bash


# system_log

docker build -t system_log:latest .

docker run --name system_log -e SQL_HOST=192.168.1.161 -e REDIS_HOST=192.168.1.161:6379 -e INFLUXDB_HOST=192.168.1.161 -e NOTIFICATION_HOST=192.168.1.161:59380 -p 9360:9360 -d system_log:latest
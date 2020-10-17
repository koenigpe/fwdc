# Build docker image
docker build -t fwdc:0.1 . 

# List container incl stopped
docker container ls --all

# List images
docker image ls

# Start container
# -dit = detach, interactive, with tty
# --privileged wo be able to mount smb
docker container run -dit --name fwdc --env-file .env -v /tmp/dstmp:/tmp/dstmp fwdc:0.1

# shell
docker exec -it e4455c65df23 /bin/sh

# Remove Docker image
docker image rm -f fwdc:0.1

# Alle laufenden/gestoppten  container löschen
docker rm -f $(docker ps -q -a)

# Debug on startup
docker events&
#command here 
# spit ids
docker logs <<id>>



### ## Build and Deploy on rpi 
# to enable buildx:
<https://thenewstack.io/how-to-enable-docker-experimental-features-and-encrypt-your-login-credentials/>
<https://stackoverflow.com/questions/60080264/docker-cannot-build-multi-platform-images-with-docker-buildx>
<https://www.docker.com/blog/multi-arch-images/>

# copy to tmp

docker build -t fwdc:0.1 .
 
docker container run -dit --name fwdc --env-file /home/pi/.env -v /tmp/dstmp:/tmp/dstmp fwdc:0.1



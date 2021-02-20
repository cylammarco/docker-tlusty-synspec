# docker-tlusty-synspec

Build the docker image with

`docker build -f ./Dockerfile -t tlusty-image`

Then create and run a detached container
`docker run -d -it --name =tlusty-container tlusty-image`

Finally, enter the container with
`docker exec -it tlusty-container /bin/bash`

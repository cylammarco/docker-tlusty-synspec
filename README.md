# docker-tlusty-synspec

Build the docker image with

`docker build -f ./Dockerfile . -t tlusty-image`

Then create and run a detached container
`docker run -d -it --name tlusty-container --mount type=bind,source="$(pwd)"/io_folder,target=/usr/local/bin/tlusty205/io_folder tlusty-image /bin/bash`

Finally, enter the container with
`docker exec -it tlusty-container /bin/bash`


## Run TLUSTY and SYNSPEC

The config files for TLUSTY and SYNSPEC can be supplied in a folder inside the `io_folder`. Then
they should be listed in a plain text file and on the host machine, run:

`docker exec -it tlusty-container run_tlusty.sh`

In the example, `t2000g50/run.list`, four rows are provoided:

> tlusty t20000g50lt
> tlusty t20000g50nc t20000g50lt
> tlusty t20000g50nl t20000g50nc
> synspec t20000g50nl fort.55.lin data/gfall.dat

The first column can be `tlusty` or `synspec`, the second column is the first config file (.5 file), the third column if provided is the starting model (.7 file), and the fourth column (only for synspec) is the line list (all of which reside in the `data` folder).

Then this line can be run to run the computation of the local-thermoequilibrium continuum case, which is used as the starting point for a non-local-thermoequilibrium continuum case, which is used as the starting model for a non-local-thernoequilibrium line-blanketing case. The SYNSPEC will then compute the detail SED based on the final case with the complete line-list.


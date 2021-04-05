FROM ubuntu:latest
LABEL maintainer="MCL <lam@tau.ac.il>"

# Workaround https://unix.stackexchange.com/questions/2544/how-to-work-around-release-file-expired-problem-on-a-local-mirror
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until

# Basic software installation
RUN apt-get update
RUN apt-get install -y wget nano gfortran p7zip-full python3.8 python3-pip
RUN pip3 install scipy numpy matplotlib mpld3

# Compile TLUSTY and SYNSPEC
WORKDIR /usr/local/bin
COPY tlusty205.tar.gz .
RUN tar -xvzf /usr/local/bin/tlusty205.tar.gz -C .
RUN gfortran -std=legacy -fno-automatic -O3 -o tlusty205/tlusty/tlusty.exe tlusty205/tlusty/tlusty205.f
RUN gfortran -std=legacy -fno-automatic -O3 -o tlusty205/synspec/synspec.exe tlusty205/synspec/synspec51.f

# Uncompress the large atomic and line files
WORKDIR /usr/local/bin/tlusty205/data
COPY gf26 .
COPY linelist .
RUN 7z x gf2601.lin.7z
RUN 7z x gf2602.lin.7z
RUN 7z x gf2603.lin.7z
RUN 7z x gf2604.lin.7z
RUN 7z x gf2605.lin.7z
RUN 7z x gfATO.dat.7z
RUN 7z x gfMOL.dat.7z
RUN 7z x gfTiO.dat.7z
RUN 7z x gfall.dat.7z

# Set environmental variables
ENV TLUSTY="/usr/local/bin/tlusty205"

WORKDIR /usr/local/bin/tlusty205

# Create mount points
RUN mkdir io_folder

COPY run_tlusty.sh run_tlusty.sh
COPY plot_spec.py plot_spec.py

RUN awk '{ sub("\r$", ""); print }' run_tlusty.sh > run_tlusty2.sh
RUN mv run_tlusty2.sh run_tlusty.sh
RUN chmod +x run_tlusty.sh

RUN awk '{ sub("\r$", ""); print }' plot_spec.py > plot_spec2.py
RUN mv plot_spec2.py plot_spec.py
RUN chmod +x plot_spec.py

CMD /bin/bash run_tlusty.sh
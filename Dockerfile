FROM ubuntu:latest
LABEL maintainer="MCL <lam@tau.ac.il>"

# Workaround https://unix.stackexchange.com/questions/2544/how-to-work-around-release-file-expired-problem-on-a-local-mirror
RUN echo "Acquire::Check-Valid-Until \"false\";\nAcquire::Check-Date \"false\";" | cat > /etc/apt/apt.conf.d/10no--check-valid-until

# Basic software installation
RUN apt-get update
RUN apt-get install -y wget
RUN apt-get install -y nano gfortran

# Compile TLUSTY and SYNSPEC
COPY tlusty205.tar.gz /usr/local/bin
RUN tar -xvzf /usr/local/bin/tlusty205.tar.gz -C /usr/local/bin/
RUN gfortran -std=legacy -fno-automatic -O3 -o /usr/local/bin/tlusty205/tlusty/tlusty.exe /usr/local/bin/tlusty205/tlusty/tlusty205.f
RUN gfortran -std=legacy -fno-automatic -O3 -o /usr/local/bin/tlusty205/tlusty/synspec.exe /usr/local/bin/tlusty205/synspec/synspec51.f

ENV TLUSTY="/usr/local/bin/tlusty205"

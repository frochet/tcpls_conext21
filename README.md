# TCPLS: Modern Transport Services with TCP and TLS

Links: https://github.com/pluginized-protocols/picotcpls  
       https://github.com/frochet/tcpls_conext21

## Artifact Summary

The main artifact is the TCPLS implementation available as a C
implementation compiling to:

1) A library to embed into an application

2) A Command Line Interpreter for launching a client/server application
directly available from the built process. Many configurations are
possible. All experiments in this paper have been realized with the
client/server tooling.

The source code contains 9k additional lines of C code atop of the
initial picotls library.

Besides the main implementation, there are the following materials:


- Plot scripts to re-generate all of the paper's figures.
- shell scripts to generate the experiments
- Readme information to re-generate the data of several of the paper's
  figures.


## Regenetate the figures

### Requirements

- python3
- pip
- texlive
- texlive-latex-extra
- cm-super
- dvipng
- matplotlib
- pandas

On a debian-based system:

```
apt install python3 pip texlive texlive-latex-extra cm-super dvipng
python3 -m pip install matplotlib
python3 -m pip install pandas
```

```
git clone git@github.com:frochet/tcpls_conext21.git
cd pretty_plotify
./plots.sh <ext> where ext in {pdf, png, eps}
```

All figures should then be in pretty_plotify/plots/

## Regenerate Results

You may want to use docker and ubuntu 20.04 to reproduce those results.
Install docker and pull a ubuntu 20.04. 

```
 docker run -it --rm --privileged -e DISPLAY -v /tmp/.X11-unix:/tmp/.X11-unix <IMAGE>
```

Running it in privileged mode is required by IPMininet.

### Requirements

You will need [IPMininet](https://ipmininet.readthedocs.io/en/latest/)
inside the docker, or in your machine if you don't go with the docker
option.
Your best shot would be doing (inside the docker):


```
pip install --upgrade git+https://github.com/cnp3/ipmininet.git@v1.0
python3 -m ipmininet.install -q
```
You will need a compiling environment, and the following packages:  

- cmake
- pkg-config
- libssl-dev
- sudo (for IPMininet)

```
git clone https://github.com/pluginized-protocols/picotcpls
```

Follow the Readme to compile picotcpls.

### Application-level Migration

Follow the Readme located at

https://github.com/pluginized-protocols/picotcpls/blob/master/t/ipmininet/readme_for_figure_app_migration.md

Following the results obtained, you can place them in
pretty_plotify/results of the tcpls_conext21 repository and execute
./plots.sh


### CC injection

checkout picotcpls's tcpls/bpf branch, and find the readme instructions
in t/ipmininet/readme_for_bpf_cc_test.md

### Raw throughtput

Reproducing the same results requires the same physical setup. However,
you may want to play with picotcpls's CLI to setup client/server and
test the features

you'll find the binary cli at the root of picotcpls's repository after
compilation.

```
cli -h
```

gives you all possibilites. You may want to run some tests in a
pre-configured network. Please read the instructions at the end of
picotcpls's readme to play with a client/server in IPMininet.

### Figures involving MPTCP.

Follow this repository's readme:

https://github.com/frochet/tcpls_mptcp_experiments

It will give you steps to reproduce MPTCP vs TCPLS results inside a
Vagrant box. Eventually the log files obtained, and the timing events
obtained need to be feeded to the plot script within this repository.




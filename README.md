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

```
git clone https://github.com/pluginized-protocols/picotcpls
```

Follow the Readme to compile picotcpls and install IPMininet

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

Notes: One of the repositories required for this part is currently located offline in a different
country from which the main author's location currently is. This part
will be updated when the main author returns (Early December 2021).
Please ignore this part until further notice. If this part is still
missing early december, please open a github issue.

You'll need two more repositories:

https://github.com/frochet/minitopo which contains a TCPLS script to
automatically run a TCPLS experiment between 2 hosts with some
perturbations. E.g., a TCP RST or a blackholing situation. Make sure to
have picotcpls in ~/, or change
https://github.com/frochet/minitopo/blob/minitopo2/experiments/tcpls.py
variables accordingly.





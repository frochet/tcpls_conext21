from __future__ import division
import os
import argparse
import pdb
import matplotlib.pyplot as plt
from utils import *

parser = argparse.ArgumentParser(description="")

parser.add_argument("--trace", type=str, nargs="+", help="all goodput traces")
parser.add_argument("--legend", type=str, nargs="+", help="Graph legend, in the\
                    same ordering than the traces")

parser.add_argument("--breakage_at", type=str, help="Breakage happened at? in\
                    second")
parser.add_argument("-i", type=float, default=0.1, help="Time interval on which each bandwidth datapoint is computed")


def parse_time(timestr):
    tab = timestr.split(":")
    h, m = int(tab[0]), int(tab[1])
    tab2 = tab[2].split(".")
    s, mus = int(tab2[0]), int(tab2[1])
    return h*60*60*1000000 + m*60*1000000+ s*1000000+mus
def parse_file(tcpdump_file, interval):
    x, y = [], []
    min_timing = float("inf")
    pathcounter = 0
    with open(tcpdump_file) as f:
        firstline = f.readline()
        tab = firstline.split()
        min_timing = parse_time(tab[0])
        x = [min_timing+interval]
        y = [int(tab[4])]
        for line in f:
            tab = line.split()
            #  - this timing is inside x+=interval => add the length to the
            #  current list
            #  - this timing is in ]x+=interval, x+=3*interval], we are in
            #  the next interval
            #  - this timing is > x+=3*interval -> add 0s y and increase x
            #  until we're in the next interval
            x_val = x[-1] #take the last value
            this_timing = parse_time(tab[0])
            if abs(this_timing-x_val) <= 2*interval:
                y[-1] += int(tab[4])
            elif abs(this_timing-x_val) <= 3*interval:
                x.append(x[-1]+2*interval)
                y.append(int(tab[4]))
            else:
                while this_timing-x_val > 3*interval:
                    x.append(x[-1]+2*interval)
                    y.append(0)
                    x_val = x[-1] #take the last value
                # We should now be in range for the next interval
                if abs(this_timing-x_val) <= 2*interval:
                    y[-1] += int(tab[4])
                elif abs(this_timing-x_val) <= 3*interval:
                    x.append(x[-1]+2*interval)
                    y.append(int(tab[4]))
                else:
                    raise ValueError("ouch? We should never get here. The trace might be malformed")
    return x, y, min_timing


if __name__ == "__main__":
    args = parser.parse_args()
    if len(args.trace) != len(args.legend):
        raise ValueError("Different numbers of --trace and --legend. We should have one legend for each trace")

    fig, ax = plt.subplots()
    i = 0
    minimum = 10000000000000000000
    linemodify = ["-"]
    markers = ["o", "^", "v", "<", ">", "*", "+", "x"]
    for trace in args.trace:
        x, y, min_timing = parse_file(trace, args.i*1000000)
        minimum = min(min_timing, minimum)
        filter_x = [(fx-min_timing)/1000000 for fx in x[:-1] if fx-min_timing < (7.5*1000000)]
        filter_y = [(yfil*8/1000000)/args.i for yfil in y[0:len(filter_x)]]
        if (filter_x[0] < 7.5):
            ax.plot(filter_x, filter_y, label=legend_label(args.legend[i]),
                    linestyle=linemodify[i%len(linemodify)], marker = markers[i], lw=2)
        i+=1

    ax.set_xlim(2, 7.5)
    ax.set_ylim(-1, 70)

    axis_aesthetic(ax)

    ax.set_xlabel(latex_label('time (s)'), fontsize=20)
    ax.set_ylabel(latex_label('Bandwidth (Mbits)'), fontsize=20)

    breakage = parse_time(args.breakage_at)
    plt.axvline(x=(breakage-minimum)/1000000, color="k", ls='--', lw=2)
    plt.text((breakage-minimum)/1000000, 57, legend_label('Breakage'), rotation=45,
             fontsize=16)

    plt.legend(bbox_to_anchor=(-0.05,0.95,1,0.2), ncol=2, columnspacing=0.2, fontsize=12)
    grid(True, color='gray', linestyle='dashed', which='major')

    savefig('breakage_analysis.pdf', bbox_inches='tight')
    #plt.show()

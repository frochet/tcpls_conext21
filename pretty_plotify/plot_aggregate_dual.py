from __future__ import division
import os
import argparse
import pdb
import matplotlib.pyplot as plt
from utils import *

parser = argparse.ArgumentParser(description="Parse and plot trace experiments\
                                 produced within IP mininet")

parser.add_argument("--goodput", type=str, help="goodput trace produced by the\
                    cli", nargs="+")
parser.add_argument("--tcpdump", type=str, help="tcpdump trace", nargs="+")

parser.add_argument("--oname", type=str, help="Output figure name")
parser.add_argument("--ext", type=str, help="Output file extension (e.g., pdf, png)")

parser.add_argument("-i", type=float, default=0.1, help="Time interval on which each bandwidth datapoint is computed")
parser.add_argument("--event_at", type=str, nargs="+", help="Event happened at? in\
                    second", default=[])
parser.add_argument("--event_text", type=str, nargs="+", help="Event text linked to the event_at")
parser.add_argument("--event_pos", type=int, nargs="+", help="Event text position on the y axis")

def parse_time(timestr):
    """
        timestr: HH:MM:SS.µS
        returns the line timestr in µs
    """
    tab = timestr.split(":")
    h, m = int(tab[0]), int(tab[1])
    tab2 = tab[2].split(".")
    s, mus = int(tab2[0]), int(tab2[1])
    return h*60*60*1000000 + m*60*1000000+ s*1000000+mus

def parse_tcpdump(tcpdump_file, interval):
    x, y = {}, {}
    min_timing = float("inf")
    paths = {}
    pathcounter = 0
    with open(tcpdump_file) as f:
        firstline = f.readline()
        tab = firstline.split()
        paths[tab[1]+tab[3]] = pathcounter
        pathcounter+=1
        min_timing = parse_time(tab[0])
        x[paths[tab[1]+tab[3]]] = [min_timing]
        y[paths[tab[1]+tab[3]]] = [int(tab[4])]
        for line in f:
            tab =  line.split()
            if tab[1]+tab[3] not in paths:
                if tab[3]+tab[1] in paths:
                    paths[tab[1]+tab[3]] = paths[tab[3]+tab[1]]
                else:
                    paths[tab[1]+tab[3]] = pathcounter
                    pathcounter+=1
                this_timing = parse_time(tab[0])
                x[paths[tab[1]+tab[3]]] = [this_timing+interval]
                y[paths[tab[1]+tab[3]]] = [int(tab[4])]
            else:
                # ok, we know this path. Several cases:
                #  - this timing is inside x+=interval => add the length to the
                #  current list
                #  - this timing is in ]x+=interval, x+=3*interval], we are in
                #  the next interval
                #  - this timing is > x+=3*interval -> add 0s y and increase x
                #  until we're in the next interval
                x_val = x[paths[tab[1]+tab[3]]][-1] #take the last value
                this_timing = parse_time(tab[0])
                if abs(this_timing-x_val) <= 2*interval:
                    y[paths[tab[1]+tab[3]]][-1] += int(tab[4])
                elif abs(this_timing-x_val) <= 3*interval:
                    x[paths[tab[1]+tab[3]]].append(x[paths[tab[1]+tab[3]]][-1]+2*interval)
                    y[paths[tab[1]+tab[3]]].append(int(tab[4]))
                else:
                    while this_timing-x_val > 3*interval:
                        x[paths[tab[1]+tab[3]]].append(x[paths[tab[1]+tab[3]]][-1]+2*interval)
                        y[paths[tab[1]+tab[3]]].append(0)
                        x_val = x[paths[tab[1]+tab[3]]][-1] #take the last value
                    # We should now be in range for the next interval
                    if abs(this_timing-x_val) <= 2*interval:
                        y[paths[tab[1]+tab[3]]][-1] += int(tab[4])
                    elif abs(this_timing-x_val) <= 3*interval:
                        x[paths[tab[1]+tab[3]]].append(x[paths[tab[1]+tab[3]]][-1]+2*interval)
                        y[paths[tab[1]+tab[3]]].append(int(tab[4]))
                    else:
                        pdb.set_trace()
                        print("ouch?")
    return paths, x, y, min_timing

def parse_goodput(goodput_file, interval):
    x, y = [], []
    min_timing = float("inf")
    pathcounter = 0
    with open(goodput_file) as f:
        firstline = f.readline()
        tab = firstline.split()
        min_timing = parse_time(tab[0])
        x = [min_timing]
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
    fix, axs = plt.subplots(2, 1, figsize=(15,10))

    min_timing = 100000000000000000
    elem = 0
    x_max = 0
    for ax in axs:
        x_g, y_g, min_timing_g = parse_goodput(args.goodput[elem], args.i*1000000)
        x_max = max(x_max, (x_g[-1]-min_timing_g)/1000000)
        #print("goodput tot : {0} bytes".format(sum(y_g)))

        ax.plot([(x-min_timing_g)/1000000 for x in x_g[:-1]],
                [(y*8/1000000)/(2*args.i) for y in y_g[:-1]], label=legend_label("Goodput"), lw=2)
        paths, x_t, y_t, min_timing_t = parse_tcpdump(args.tcpdump[elem], args.i*1000000)
        counter = 0

        for path in set(paths.values()):
            x_max = max(x_max, (x_t[path][-1]-min_timing_t)/1000000)
            ax.plot([(x-min_timing_t)/1000000 for x in x_t[path][:-1]],
                    [(y*8/1000000)/(2*args.i) for y in y_t[path][:-1]],
                label=legend_label("Throughput subflow Conn {}".format(counter)), lw=2)
            counter+=1

        event = parse_time(args.event_at[elem])
        ax.axvline(x=(event-min_timing_t)/1000000, color="k", lw=2)
        #ax.text((event-min_timing)/1000000, args.event_pos[elem], args.event_text[elem],
        #         color="k")
        ax.annotate(legend_label(args.event_text[elem]),
                    xy=((event-min_timing_t)/1000000, args.event_pos[elem]),
                    xytext=(1, (args.event_pos[elem])),
                    arrowprops=dict(arrowstyle="<|-", color='dimgray'), fontsize=17,
                    color='dimgray')
        elem+=1

    axis_aesthetic(axs[0])
    axis_aesthetic(axs[1])

    for ax in axs:
        ax.legend(loc='upper left', fontsize=17, edgecolor="black", fancybox=False)
        ax.set_xlim(0, x_max)
        ax.set_ylim(0, 65)
        ax.set_xlabel(latex_label("Time (s)"), fontsize=24)
        ax.set_ylabel(latex_label("Bandwidth (Mbits)"), fontsize=24)
        ax.grid(True, color='gray', linestyle='dashed', which='major')

    axs[0].set_title(latex_label('MPTCP 0.94.7'), fontsize=18)
    axs[1].set_title(latex_label('TCPLS'), fontsize=18)
    plt.tight_layout()

    subplots_adjust(hspace=0.4)

    savefig(args.oname+'.'+args.ext, bbox_inches='tight')

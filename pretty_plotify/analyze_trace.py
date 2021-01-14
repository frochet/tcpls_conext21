import os
import argparse
import pdb
import matplotlib.pyplot as plt

parser = argparse.ArgumentParser(description="")
parser.add_argument("-ttcpls", type=str, help="The tcpdump simplified trace output\
                    from convert_tcpdump.py")
parser.add_argument("-tmptcp", type=str, help="The tcpdump simplified trace output\
                    from convert_tcpdump.py")
parser.add_argument("-gtcpls", type=str, help="The ./cli -g output trace that\
                    records the application throughput (goodput)")
parser.add_argument("-gmptcp", type=str, help="The ./cli -g output trace that\
                    records the application throughput (goodput)")
parser.add_argument("-tpquic", type=str, help="The tcpdump simplified trace\
                    output from convert_tcpdump.py")
parser.add_argument("-gpquic", type=str, help="The pquic goodput trace")

parser.add_argument("-i", type=float, default=0.1, help="Time interval on which each bandwidth datapoint is computed")

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

#XXX when ploting, discard the last valua of each path which does not account for a full interval?
def parse_file(tcpdump_file, interval):
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
        x[paths[tab[1]+tab[3]]] = [min_timing+interval]
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

if __name__ == "__main__":
    args = parser.parse_args()
    min_timing = float("inf")
    #fig, [ax1, ax2, ax3] = plt.subplots(3, 1)
    fig, [ax1, ax3] = plt.subplots(2, 1)
    ax1.set(xlabel="time (s)", ylabel="Bandwidth (Mbits)")
    #ax2.set(xlabel="time (s)", ylabel="Bandwidth (Mbits)")
    ax3.set(xlabel="time (s)", ylabel="Bandwidth (Mbits)")
    x_max = 0
    tot_mptcp_throughput = 0
    tot_mptcp_goodput = 0
    tot_tcpls_throughput = 0
    tot_tcpls_goodput = 0
    if args.tmptcp:
        paths_mptcp, x_mptcp, y_mptcp, min_mptcp = parse_file(args.tmptcp, args.i*1000000)
        for path in set(paths_mptcp.values()):
            ax1.plot([(x-min_mptcp)/1000000 for x in x_mptcp[path][:-1]],
                     [(y*8/1000000)/args.i for y in y_mptcp[path][:-1]],
                     label="Throughput Path {0}".format(path))
            tot_mptcp_throughput += sum(y_mptcp[path][:-1])
            x_max_mptcp = x_mptcp[path][-1]
            if x_max_mptcp-min_mptcp > x_max:
                x_max = x_max_mptcp-min_mptcp
        if args.gmptcp:
            paths_mptcp, x_mptcp, y_mptcp, min_mptcp = parse_file(args.gmptcp, args.i*1000000)
            for path in set(paths_mptcp.values()):
                ax1.plot([(x-min_mptcp)/1000000 for x in x_mptcp[path][:-1]],
                         [(y*8/1000000)/args.i for y in y_mptcp[path][:-1]],
                         color='orange', label="Goodput")
                tot_mptcp_goodput += sum(y_mptcp[path][:-1])
    if args.tpquic:
        if args.gpquic:
            paths_pquic, x_pquic, y_pquic, min_pquic = parse_file(args.gpquic,
                                                                   args.i*1000000)
            for path in set(paths_pquic.values()):
                ax2.plot([(x-min_pquic)/1000000 for x in x_pquic[path][:-1]],
                         [(y*8/1000000)/args.i for y in y_pquic[path][:-1]],
                         color='orange', label="Goodput")
        paths_pquic, x_pquic, y_pquic, min_pquic = parse_file(args.tpquic,
                                                               args.i*1000000)
        for path in set(paths_pquic.values()):
            ax2.plot([(x-min_pquic)/1000000 for x in x_pquic[path][:-1]],
                     [(y*8/1000000)/args.i for y in y_pquic[path][:-1]],
                     label="Throughput Path {0}".format(path))
    if args.ttcpls:
        if args.gtcpls:
            paths_tcpls, x_tcpls, y_tcpls, min_tcpls = parse_file(args.gtcpls, args.i*1000000)
            linemodif = [":", "--"]
            for path in set(paths_tcpls.values()):
                ## Hardcode path number to match the tcpdump trace:
                if path == 0:
                    labeline = "Goodput"
                    val = 0
                else:
                    labeline = None
                    val = 3
                ax3.plot([(x-min_tcpls)/1000000 for x in x_tcpls[path][:-1]],
                         [(y*8/1000000)/args.i for y in y_tcpls[path][:-1]],
                         color="orange", linestyle="-",
                         label=labeline)
                tot_tcpls_goodput += sum(y_tcpls[path][:-1])
        paths_tcpls, x_tcpls, y_tcpls, min_tcpls = parse_file(args.ttcpls, args.i*1000000)
        for path in set(paths_tcpls.values()):
            ax3.plot([(x-min_tcpls)/1000000 for x in x_tcpls[path][:-1]],
                     [(y*8/1000000)/args.i for y in y_tcpls[path][:-1]],
                     label="Throughput Path {0}".format(path))
            tot_tcpls_throughput += sum(y_tcpls[path][:-1])
            x_max_tcpls = x_tcpls[path][-1]
            if x_max_tcpls-min_tcpls > x_max:
                x_max = x_max_tcpls-min_tcpls

    if args.gtcpls and args.gmptcp:
        print("Mptcp overhead: {0}".format(tot_mptcp_throughput/tot_mptcp_goodput))
        print("TCPLS overhead: {0}".format(tot_tcpls_throughput/tot_tcpls_goodput))
        print("MPTCP overhead/TCPLS overhead:\
              {0}".format((tot_mptcp_throughput/tot_mptcp_goodput)/(tot_tcpls_throughput/tot_tcpls_goodput)))
    ax1.set_xlim(0, x_max/1000000)

    ax1.text(.5,.9,'MPTCP 0.94.7',
        horizontalalignment='center',
        transform=ax1.transAxes, fontsize="16")
    # ax2.set_xlim(0, x_max/1000000)
    # ax2.text(.5,.9,'PQUIC + multipath_rr.plugin',
        # horizontalalignment='center',
        # transform=ax2.transAxes, fontsize="16")
    ax3.set_xlim(0, x_max/1000000)
    ax3.text(.5,.9,'TCPLS',
        horizontalalignment='center',
        transform=ax3.transAxes, fontsize="16")
    ax1.legend()
    # ax2.legend()
    ax3.legend()
    plt.show()



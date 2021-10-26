from __future__ import division
import os
import argparse
import pdb
import matplotlib.pyplot as plt
from utils import *

parser = argparse.ArgumentParser(description="Parse and plot trace experiments\
                                 comparing vegas and cubic bpf")

parser.add_argument("--goodput", type=str, help="Traffic goodput")
parser.add_argument("--delay", type=str, help="Traffic delay")

parser.add_argument("--cubic", type=str, help="Cubic input file name")
parser.add_argument("--vegas", type=str, help="Vegas input file name")

parser.add_argument("--oname", type=str, help="Output figure name")
parser.add_argument("--ext", type=str, help="Output file extension (e.g., pdf, png)")

if __name__ == "__main__":
    args = parser.parse_args()

    fig, ax = plt.subplots(figsize=(8,6))

    df_vegas = pd.read_csv(args.vegas, sep=";", skipinitialspace=True)
    df_cubic = pd.read_csv(args.cubic, sep=";", skipinitialspace=True)

    df_cubic.plot(kind='line', x='Time', y='Goodput', label=legend_label('CUBIC'), ax=ax, lw=2)
    df_vegas.plot(kind='line', x='Time', y='Goodput', label=legend_label('Vegas then eBPF CUBIC'), ax=ax, lw=2)

    ax.annotate(legend_label('injection of eBPF CUBIC'),
                xy=(117.561356, 12.116826),
                xytext=(150, 12.116826),
                arrowprops=dict(arrowstyle="<|-", color='black'), fontsize=15,
                color='black')

    ax.set_ylim(0, 100)

    axis_aesthetic(ax=ax)

    ax.set_xlabel(latex_label('Time (s)'), fontsize=20)
    ax.set_ylabel(latex_label('Goodput (Mbps)'), fontsize=20)

    plt.legend(loc='upper right', fontsize=15, edgecolor="black", fancybox=False)
    grid(True, color='gray', linestyle='dashed', which='major')

    savefig(args.oname+'.'+args.ext, bbox_inches='tight')

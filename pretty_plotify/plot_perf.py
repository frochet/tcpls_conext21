from __future__ import division
import matplotlib.pyplot as plt
import argparse
import numpy as np
from utils import *
import colorsys

def init_args():
   plt.rc('xtick', labelsize=12)
   plt.rc('text', usetex=True)
   parser = argparse.ArgumentParser(description="")

   parser.add_argument("--trace", nargs="+", required=True)
   parser.add_argument("--label", nargs="+", required=True)
   parser.add_argument("--color", nargs="+")
   parser.add_argument("--oname", type=str, help="Output figure name")
   parser.add_argument("--ext", type=str, help="Output file extension (e.g., pdf, png)")
   return parser.parse_args()


def parse_data(filepath):
    bytes = []
    pps = []
    with open(filepath) as f:
        for line in f:
            tab = line.split('\t')
            bytes.append(max(int(tab[0].split(": ")[1].split("/")[0].split('.')[0]),
                             int(tab[0].split(": ")[1].split("/")[1].split('.')[0])))
            pps.append(max(int(tab[1].split(": ")[1].split("/")[0].split('.')[0]),
                           int(tab[1].split(": ")[1].split("/")[1].split('.')[0])))

    bytes.sort()
    pps.sort()

    return bytes[int(len(bytes)/2)], max(bytes), pps[int(len(pps)/2)], max(pps)

def scale_lightness(rgb, scale_l):
    # convert rgb to hls
    h, l, s = colorsys.rgb_to_hls(*rgb[0:3])
    # manipulate h, l, s values and return as rgb
    return colorsys.hls_to_rgb(h, min(1, l * scale_l), s = s)

def main():

    # data processing
    args = init_args()
    bar_height_bw, bar_height_pps = [], []
    counter = 0
    for file in args.trace:
        bw_median, bw_max, pps_median, pps_max = parse_data(file)
        bar_height_bw.append((args.label[counter], bw_median/1000))
        print("Max bw for {} is {}".format(args.label[counter], bw_max))
        print("Max pps for {} is {}".format(args.label[counter], pps_max))
        bar_height_pps.append((args.label[counter], pps_median))
        counter+=1

    bar_height_bw.sort(key=lambda x: x[1], reverse=True)
    mapping = dict(bar_height_pps)
    bar_height_pps_sorted = [(x[0], mapping[x[0]]) for x in bar_height_bw]
    bar_height_pps = bar_height_pps_sorted
    y_pos = np.arange(len(bar_height_bw))

    #data plotting
    fig, ax = plt.subplots(figsize=(8,6))

    cmap = plt.get_cmap('RdYlGn')(
        np.linspace(0.15, 0.85, 5))
    colors = [cmap[4],cmap[1], cmap[3],cmap[3],
             cmap[4],cmap[1],
             cmap[1],cmap[4],cmap[0],
             cmap[2],cmap[0],
             cmap[1],cmap[4],cmap[0]]
    
    plt.barh(y_pos, [8*height[1]/1000000 for height in bar_height_bw],
             color = colors, alpha=0.7)
    plt.yticks(y_pos)
    # * o x d v
    markers=["v","o","*","*","v","o","o","v","P","x","P","o","v","P"]
    for i in range(len(colors)):
        ax.plot(0, y_pos[i], marker=markers[i], linestyle="", color=scale_lightness(colors[i], .65), 
        clip_on=False)
        
    for i, p in enumerate(ax.patches):
        left, bottom, width, height = p.get_bbox().bounds
        ax.annotate(legend_label(r" $\textbf{"+str(bar_height_pps[i][1])+"}$ pps"), xy=(left+0.5+width/2, bottom+height/2),
                    ha='center', va='center', color='black', weight='bold', fontsize=12)

    axis_aesthetic(ax)
    
    # align & pad labels
    ax.set_yticklabels([height[0] for height in bar_height_bw], ha="left")
    yax = ax.get_yaxis()
    yax.set_tick_params(pad=225)

    plt.xlabel(latex_label("Throughput in Gbps"), fontsize=20)
    grid(True, color='gray', linestyle='dashed', which='major')

    #axhline(y=3.5, lw=2, color='k')
    #axhline(y=5.5, lw=2, color='k')
    #axhline(y=8.5, lw=2, color='k')
    #axhline(y=10.5, lw=2, color='k')

    savefig(args.oname+'.'+args.ext, bbox_inches='tight')
    
main()

import matplotlib.pyplot as plt
import argparse
import numpy as np

parser = argparse.ArgumentParser(description="")

parser.add_argument("--trace", nargs="+", required=True)
parser.add_argument("--label", nargs="+", required=True)
parser.add_argument("--color", nargs="+")

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

if __name__ == "__main__":

    args = parser.parse_args()
    bar_height_bw, bar_height_pps = [], []
    counter = 0
    for file in args.trace:
        bw_median, bw_max, pps_median, pps_max = parse_data(file)
        bar_height_bw.append((args.label[counter], bw_median))
        print("Max bw for {} is {}".format(args.label[counter], bw_max))
        print("Max pps for {} is {}".format(args.label[counter], pps_max))
        bar_height_pps.append((args.label[counter], pps_median))
        counter+=1
    
    bar_height_bw.sort(key=lambda x: x[1], reverse=True)
    mapping = dict(bar_height_pps)
    bar_height_pps_sorted = [(x[0], mapping[x[0]]) for x in bar_height_bw]
    bar_height_pps = bar_height_pps_sorted
    y_pos = np.arange(len(bar_height_bw))
    plt.barh(y_pos, [height[1]/1000000 for height in bar_height_bw])
    plt.yticks(y_pos, [height[0] for height in bar_height_bw])
    for i, bw in enumerate(bar_height_bw):
        plt.text(bw[1]/1000000 - 50, i-0.15, str(bar_height_pps[i][1])+" pps")
    plt.xlabel("Download in MB/s")
    plt.subplots_adjust(left=0.35)
    plt.show()

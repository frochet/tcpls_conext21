###########################################
# Scripts for plotting the various graphs #
# for TCPLS analysis                      #
#                                         #
# Usage:                                  #
# ./plots.sh <ext>                        #
# where ext == {pdf, png, eps}            #
#                                         #
# Version 1.O                             #
# Date: 19/01/2021                        #
###########################################

input="results"
output="plots"

echo "Plotting MPTCP-TLS comparison..."
python3 analyze_trace.py -tmptcp $input/mptcp_pruned_2paths -gmptcp $input/mptcp_cli_trace -gtcpls $input/tcpls_cli_trace -ttcpls $input/tcpls_pruned_2paths -i 0.1 --ext $1 --oname $output/tcpls_mptcp

echo "Plotting multipath aggregate..."
python3 plot_aggregate.py --goodput $input/tcpls_aggregation_goodput.log --tcpdump $input/tcpls_aggregation_pruned_tcpdump.log --oname $output/multipath_aggregate --ext $1 -i 0.1 --event_at 20:16:54.698002 --event_text "New stream attached" --event_pos 3

echo "Plotting migration..."
python3 plot_aggregate.py --goodput $input/tcpls_migration_goodput --tcpdump $input/tcpls_migration_pruned.log --oname $output/migration --ext $1 -i 0.1 --event_at 14:55:28.854711 14:55:30.142117 14:55:33.569810 14:55:34.752775 --event_text "New Stream on Path 1" "Stream closed and Path 0 Closed" "0-RTT Conn + New Stream on Path 0" "Stream Closed and Path 1 closed" --event_pos 2 7 2 7

echo "Plotting breakage analysis..."
python3 plot_breakage.py --trace $input/mptcp_client_goodput_drop.log $input/mptcp_client_goodput_rst.log $input/mptcp_client_goodput_ifupdown.log $input/tcpls_client_goodput_drop.log $input/tcpls_client_goodput_rst.log --legend "MPTCP; breakage drop" "MPTCP; breakage rst" "MPTCP; breakage IF down" "TCPLS Failover; breakage drop" "TCPLS Failover; breakage rst" --breakage_at 11:33:51.815470 --ext $1 --oname $output/breakage_analysis

echo "Plotting vegas vs. cubic..."
python3 cubic_vegas.py --cubic $input/cubic.csv --vegas $input/vegas_bpf_cubic.csv --goodput 100 --delay 60 --ext $1 --oname $output/vegas_cubic

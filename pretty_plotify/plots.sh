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

echo "Plotting performance analysis..."
python3 plot_perf.py --trace $input/tcpls_jumbo_aes128gcmsha256.log $input/tcpls_default_mtu_aes128gcmsha256.log $input/tcpls_jumbo_failoveron_aes128gcmsha256.log $input/tcpls_mtu1500_failoveron_aes128gcmsha256.log $input/tcpls_mtu1500_aggregation.log $input/tls_jumbo_aes128gcmsha256.log $input/mptcp_client_dualip4_default_scheduler.log $input/tls_default_mtu_aes128gcmsha256.log $input/quicly_gso_default_mtu.log $input/quicly_jumbo_pmtu1460.log $input/quicly_default_mtu.log $input/msquic_jumbo_aes128gcmsha256.log $input/msquic_default_mtu.log $input/mvfst_gso_default_mtu.log $input/mvfst_jumbo_pmtu1460.log $input/mvfst_default_mtu.log --label "TCPLS \large{\textbf{tso} on \textbf{mtu} 9000}" "TCPLS \large{\textbf{tso} on}" "TCPLS \large{\textbf{tso} on \textbf{mtu} 9000 \textbf{failover} on}" "TCPLS \large{\textbf{tso} on \textbf{failover} on}"  "TCPLS \large{\textbf{tso} on \textbf{aggregation} on}" "TLS/TCP \large{\textbf{tso} on \textbf{mtu} 9000}" "TLS/TCP \large{\textbf{tso} on \textbf{aggregation} on}" "TLS/TCP \large{\textbf{tso} on}" "Quicly \large{\textbf{gso} on}" "Quicly \large{\textbf{gso} on \textbf{mtu} 9000}" "Quicly" "Msquic \large{\textbf{mtu} 9000}" "Msquic" "mvfst \large{\textbf{gso} on \textbf{pacing} on}" "mvfst \large{\textbf{gso} on \textbf{mtu} 9000 \textbf{pacing} on}" "mvfst \large{\textbf{pacing} on}" --oname $output/perf_analysis --ext $1

echo "Plotting aggregate dual..."
python3 plot_aggregate_dual.py --goodput $input/mptcp_client_goodput_aggregation.log $input/tcpls_client_goodput_aggregation.log --tcpdump $input/mptcp_client_tcpdump_pruned_aggregation.log $input/tcpls_client_tcpdump_pruned_aggregation.log --event_at 18:42:08.472578 18:23:38.244172 --event_text "Interface UP" "APP decision to use new path" --event_pos 15 5 -i 0.05 --oname $output/aggregate_dual --ext $1

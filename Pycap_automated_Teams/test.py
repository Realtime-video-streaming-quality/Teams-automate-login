import os
import signal
import subprocess
import multiprocessing
import threading
import sys
import traceback

interface = "Wi-Fi"
pcap_output_file = "pcaps/record.pcap"

try:
    # Full path to the Tshark executable
    # tshark_path = r'C:\Program Files\Wireshark\tshark'

    command = ["tshark", '-i', "Wi-Fi", '-w', pcap_output_file, '-f', 'tcp', '-V', "-T", "json"]
    with open("tshark_output_file", "w") as f:
        subprocess.run(command, check=True, stdout=f)
except Exception as e:
    print("Error running Tshark:", e)  # Print the exception message

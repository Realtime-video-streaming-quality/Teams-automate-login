import os
import signal
import subprocess
import multiprocessing
import sys
import shutil

from JsonKeysGrabber import JsonKeysGrabber
from JsonStripper import JsonStripper

# Define your functions here
def runSelenium():
    try:
        command = ['java', '-jar', "Silenume.jar"]
        subprocess.run(command, check=True)
    except Exception as e:
        print("Something wrong with selenium process:", e)

def runTshark():
    try:
        # Specify the SSL key log file using the SSLKEYLOGFILE environment variable
        os.environ["SSLKEYLOGFILE"] = r"C:\Program Files\Wireshark\ssl-keys.log"

        # Ensure the SSL key log file exists and is accessible
        if not os.path.isfile(os.environ["SSLKEYLOGFILE"]):
            raise FileNotFoundError(f"SSL key log file not found: {os.environ['SSLKEYLOGFILE']}")

        # Command to run Tshark with decryption options
        command = [
            'tshark',
            '-i', 'Wi-Fi',
            '-o', f'tls.keylog_file:{os.environ["SSLKEYLOGFILE"]}',  # Specify the TLS key log file correctly
            '-f', 'tcp',
            '-V',
            '-T', 'json'
        ]

        # Start capturing packets and splitting output into multiple files
        file_index = 1
        lines_per_file = 10000
        line_count = 0

        staging_dir = "staging"
        os.makedirs(staging_dir, exist_ok=True)
        current_output_file = os.path.join(staging_dir, f"{base_filename}_{file_index}.txt")

        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True, encoding='utf-8', errors='replace')

        with open(current_output_file, 'w', encoding='utf-8', errors='replace') as f:
            while True:
                line = process.stdout.readline()
                if line == '' and process.poll() is not None:
                    break
                if line:
                    f.write(line)
                    line_count += 1

                    if line_count >= lines_per_file:
                        f.flush()
                        f.close()
                        file_index += 1
                        current_output_file = os.path.join(staging_dir, f"{base_filename}_{file_index}.txt")
                        line_count = 0
                        f = open(current_output_file, 'w', encoding='utf-8', errors='replace')

    except Exception as e:
        print("Something went wrong with the tshark process:", e)


def runJsonStripper():
    try:
        stripper = JsonStripper(base_filename, json_stripper_output_file, "staging")
        stripper.run()
    except Exception as e:
        print("Something wrong with the json stripper --", e)


def runJsonKeysGrabber():
    try:
        keysGrabber = JsonKeysGrabber(json_stripper_output_file)
        keysGrabber.start()
    except Exception as e:
        print("Something wrong with Json key grabber process:", e)


# Update the output file names
base_filename = "tshark_output"
json_stripper_output_file = "json_stripper_output.txt"
pcap_output_file = "pcaps/record.pcap"
interface = "Wi-Fi"

# Your __name__ == '__main__' block starts here
if __name__ == '__main__':
    # Define your multiprocessing.Process instances here
    seleniumProcess = multiprocessing.Process(target=runSelenium)
    tsharkProcess = multiprocessing.Process(target=runTshark)
    jsonStripperProcess = multiprocessing.Process(target=runJsonStripper)
    jsonKeysGrabberProcess = multiprocessing.Process(target=runJsonKeysGrabber)
    processes = [seleniumProcess, tsharkProcess, jsonStripperProcess, jsonKeysGrabberProcess]

    def start():
        for process in processes:
            process.start()
        for process in processes:
            process.join()

    def shutdown():
        for process in reversed(processes):
            process.terminate()

    def sigint_handler(sig, frame):
        print("SIGINT received. Exiting gracefully.")
        # Terminate all the child processes first
        shutdown()
        # Terminate the main process last
        sys.exit(0)

    signal.signal(signal.SIGINT, sigint_handler)
    start()
    shutdown()

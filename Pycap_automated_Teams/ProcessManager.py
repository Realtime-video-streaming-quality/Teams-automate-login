import os
import signal
import subprocess
import multiprocessing
import sys

from JsonKeysGrabber import JsonKeysGrabber
from JsonStripper import JsonStripper


# Define your functions here
def runSelenium():
    try:
        command = ['java', '-jar', "Silenume.jar"]
        subprocess.run(command, check=True)
    except Exception as e:
        print("Something wrong with selenium process")

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
            '-w', pcap_output_file,
            '-o', f'tls.keylog_file:{os.environ["SSLKEYLOGFILE"]}',  # Specify the TLS key log file correctly
            '-f', 'tcp',
            '-V',
            '-T', 'json'
        ]

        # Run Tshark subprocess with the specified command
        with open(tshark_output_file, "w") as f:
            subprocess.run(command, check=True, stdout=f, stderr=subprocess.PIPE, env=os.environ.copy())

    except Exception as e:
        print("Something went wrong with the tshark process: ", e)


def runJsonStripper():
    try:
        global stripper
        stripper = JsonStripper(tshark_output_file, json_stripper_output_file)
        stripper.run()
    except Exception as e:
        print("Something wrong with the json stripper -- ", e)


def runJsonKeysGrabber():
    try:
        keysGrabber = JsonKeysGrabber(json_stripper_output_file)
        keysGrabber.start()
    except Exception as e:
        print("Something wrong with Json key grabber process")

tshark_output_file = "tshark_output.txt"
json_stripper_output_file = "json_stripper_output.txt"
pcap_output_file = "pcaps/record.pcap"
interface = "Wi-fi"
# Your __name__ == '__main__' block starts here
if __name__ == '__main__':

    files = [tshark_output_file, json_stripper_output_file, pcap_output_file]

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


    def create_files():
        for file in files:
            with open(file, 'w'):
                pass


    def cleanup():
        for file in files:
            os.remove(file)


    # Define your signal handler here
    main_pid = os.getpid()


    def sigint_handler(sig, frame):
        print("SIGINT received. Exiting gracefully.")
        # Terminate all the child processes first
        shutdown()
        # cleanup()
        # Terminate the main process last
        sys.exit(0)


    signal.signal(signal.SIGINT, sigint_handler)
    create_files()
    start()
    shutdown()

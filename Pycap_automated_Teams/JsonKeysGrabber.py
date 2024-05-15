import logging
import string
from time import sleep

class JsonKeysGrabber:
    def __init__(self, input_file):
        self.input_file = input_file
        self.isRunning = False

    def stop(self):
        self.isRunning = False

    def start(self):
        self.isRunning = True
        foundPairs = list()
        current_val = None
        with open(self.input_file, 'r', encoding='utf-8') as file:
            while self.isRunning:
                try:
                    line = file.readline()
                    if not line:
                        sleep(0.1)  # Sleep for a short while to avoid busy waiting
                        continue

                    if isValueLine(line):
                        current_val = extractKey(line)
                    elif isKeyLine(line):
                        if current_val is None:
                            logging.error(f"Key without a matching value: {extractKey(line)}")
                        else:
                            foundPairs.append((extractKey(line), current_val))
                            print(foundPairs.pop(len(foundPairs) - 1))
                            current_val = None
                except Exception as e:
                    logging.error(f"Error processing line: {e}")
                    sleep(0.1)  # Sleep for a short while to avoid busy waiting

def isKeyLine(line):
    return "json.key" in line

def isValueLine(line):
    return "json.value" in line

def extractKey(line: string):
    value_start_index = line.find('"', line.find('"', line.find('"') + 1) + 1) + 1
    value_end_index = line.rfind('"')
    return line[value_start_index:value_end_index]

def runJsonKeysGrabber():
    try:
        keysGrabber = JsonKeysGrabber(json_stripper_output_file)
        keysGrabber.start()
    except Exception as e:
        print(f"Something wrong with Json key grabber process: {e}")

# Ensure that json_stripper_output_file is defined before calling runJsonKeysGrabber
json_stripper_output_file = 'path_to_your_json_stripper_output_file'
runJsonKeysGrabber()

import json
import string
import traceback
from time import sleep

class JsonStripper:
    def __init__(self, input_file, output_file):
        self.input_file = input_file
        self.output_file = output_file
        self.__isRunning = False

    def run(self):
        self.__isRunning = True
        self.analyze()

    def shutdown(self):
        self.__isRunning = False

    def analyze(self):
        json_started = False
        json_lines = []
        json_indentation = 0
        with open(self.output_file, 'w', encoding='utf-8') as jsonsFile:
            with open(self.input_file, 'rb') as file:  # Open input file in binary mode
                while self.__isRunning:
                    try:
                        line = file.readline()
                        if not line:
                            sleep(0.1)  # Sleep for a short while to avoid busy waiting
                            continue

                        try:
                            line = line.decode('utf-8')  # Decode the line as UTF-8
                        except UnicodeDecodeError as e:
                            print("Error decoding line: ", e)
                            continue  # Skip this line if it can't be decoded

                    except Exception as e:
                        print("Error reading line: ", e)
                        traceback.print_exc()
                        sleep(0.1)  # Sleep for a short while to avoid busy waiting
                        continue

                    # Count leading whitespace characters to determine indentation level
                    indentation = len(line) - len(line.lstrip())

                    # Strip whitespace from the beginning and end of the line
                    stripped_line = line.strip()

                    # Check if the line contains '"json": {'
                    if stripped_line == '"json": {':
                        print("Found JSON start")
                        json_started = True
                        json_lines.append(line)
                        json_indentation = indentation
                        continue  # Skip to the next line

                    # If JSON parsing has started, append the line to json_lines
                    if json_started:
                        json_lines.append(line)
                        # Check if the line contains a closing '}'
                        if stripped_line == '}' or stripped_line == '},':
                            # Check if the indentation level is the same as the opening '"json": {'
                            if indentation == json_indentation:
                                # Join the json_lines and write the result
                                json_string = ''.join(json_lines)
                                jsonsFile.write(json_string)
                                # Reset variables for the next JSON block
                                json_started = False
                                json_lines = []

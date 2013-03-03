#!/usr/bin/env python
#
# Copyright (C) 2013 Christopher Hewitt
#
# Permission is hereby granted, free of charge, to any person obtaining a 
# copy of this software and associated documentation files (the "Software"), 
# to deal in the Software without restriction, including without limitation 
# the rights to use, copy, modify, merge, publish, distribute, sublicense, 
# and/or sell copies of the Software, and to permit persons to whom the 
# Software is furnished to do so, subject to the following conditions:
#
# The above copyright notice and this permission notice shall be included in 
# all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND, EXPRESS OR 
# IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF MERCHANTABILITY, 
# FITNESS FOR A PARTICULAR PURPOSE AND NONINFRINGEMENT. IN NO EVENT SHALL 
# THE AUTHORS OR COPYRIGHT HOLDERS BE LIABLE FOR ANY CLAIM, DAMAGES OR OTHER 
# LIABILITY, WHETHER IN AN ACTION OF CONTRACT, TORT OR OTHERWISE, ARISING 
# FROM, OUT OF OR IN CONNECTION WITH THE SOFTWARE OR THE USE OR OTHER 
# DEALINGS IN THE SOFTWARE.

import sys
import argparse
import time
import serial
import serial.tools.list_ports
import PIL

class TDSGrab:

    def __init__(self, port, baudrate, timeout, hardware_flagging, software_flagging):
        self.port = port
        self.baudrate = baudrate
        self.timeout = timeout
        self.hardware_flagging = hardware_flagging
        self.software_flagging = software_flagging
        self.serial = serial.Serial()

    def connect(self):
        """Connect to serial device"""
        try:
            if not self.serial.isOpen():
                self.serial = serial.Serial(self.port, self.baudrate, timeout=self.timeout, rtscts=self.hardware_flagging, xonxoff=self.software_flagging)
                print("Connected to %s") % (self.port)
        except serial.SerialException, msg:
            print("Unable to connect to serial device: %s") % (msg)

    def disconnect(self):
        """Disconnect from serial device"""
        try:
            if self.serial.isOpen():
                self.serial.close()
                print("Disconnected from %s") % (self.port)
        except serial.SerialException, msg:
            print("Unable to disconnect from serial device: %s") % (msg)

    def grab_image(self, filename):
        """Wait for an image and save to file"""
        try:
            if self.serial.isOpen():
                self.serial.flushInput()

                data_file = None
                try:
                    data_file = open(filename, "w")
                except IOError, msg:
                    print("Error opening '" + filename + "' for writing: %s") % (msg)

                print("Waiting for data")
                while True:
                    data = self.serial.read(8)
                    if data != "":
                        print("Receiving data")
                        data_file.write(data)
                        while True:
                            data = self.serial.read(8)
                            if data != "":
                                data_file.write(data)
                            else:
                                break
                        break

                print("Data written to '%s'") % (filename)
                data_file.close()
                    
        except serial.SerialException, msg:
            print("Error reading image from serial device: %s") % (msg)

class ListPorts(argparse.Action):
    def __call__(self, parser, namespace, action, option_string):
        print("available ports:")
        for port in serial.tools.list_ports.comports():
            print(port[0])
        parser.exit()

def main():
    # runtime argument parsing
    epilog = """\
additional information:
  BAUD is expected to be one of the following:
     300, 600, 1200, 2400, 4800, 9600, 19200
  A nonstandard baud rate will produce a warning

  FLOW is expected to be one of the following:
     hw                 hardware flow control
     sw                 software flow control
     none               no flow control
  Using both hardware and software flow control together is not supported
"""
    parser = argparse.ArgumentParser(description="Download images from Tektronix TDS oscilloscopes over RS-232 link.", epilog=epilog, formatter_class=argparse.RawDescriptionHelpFormatter)
    parser.add_argument("-v", "--version", action="version", version="%(prog)s 0.1")
    parser.add_argument("-l", "--list", action=ListPorts, nargs=0, help="list available serial ports")
    parser.add_argument("-p", "--port", help="serial device to connect to (default: %(default)s)", default="/dev/ttyS0")
    parser.add_argument("-b", "--baud", help="baudrate for connection (default: %(default)s)", default=9600)
    parser.add_argument("-f", "--flow", help="select flow control method (default: %(default)s)", default="hw")
    parser.add_argument("filename", help="filename to write to")
    args = parser.parse_args()

    # verify baudrate
    if args.baud not in (300, 600, 1200, 2400, 4800, 9600, 19200):
        print("Strange baudrate! Proceeding anyway.")
    baudrate = args.baud

    timeout = 0.250

    # verify flow control method
    hardware_flagging = False
    software_flagging = False
    if args.flow == "hw":
        hardware_flagging = True
    elif args.flow == "sw":
        sofware_flagging = True

    tdsgrab = TDSGrab(port=args.port, baudrate=args.baud, timeout=timeout, hardware_flagging=hardware_flagging, software_flagging=software_flagging)
    try:
        try:
            tdsgrab.connect()
            tdsgrab.grab_image(args.filename)
        finally:
            tdsgrab.disconnect()
    except KeyboardInterrupt:
        pass

if __name__ == "__main__":
    main()

# vim: autoindent tabstop=4 shiftwidth=4 expandtab softtabstop=4 filetype=python

tdsgrab
=======

Receive hardcopy images from old Tektronix TDS oscilloscopes over RS-232 in an automated way.

Tested with python 2.7.3 and Tektronix TDS684A.

    usage: tdsgrab.py [-h] [-v] [-l] [-p PORT] [-b BAUD] [-f FLOW] filename

    Download images from Tektronix TDS oscilloscopes over RS-232 link.

    positional arguments:
      filename              filename to write to

    optional arguments:
      -h, --help            show this help message and exit
      -v, --version         show program's version number and exit
      -l, --list            list available serial ports
      -p PORT, --port PORT  serial device to connect to (default: /dev/ttyS0)
      -b BAUD, --baud BAUD  baudrate for connection (default: 9600)
      -f FLOW, --flow FLOW  select flow control method (default: hw)

    additional information:
      BAUD is expected to be one of the following:
         300, 600, 1200, 2400, 4800, 9600, 19200
      A nonstandard baud rate will produce a warning

      FLOW is expected to be one of the following:
         hw                 hardware flow control
         sw                 software flow control
         none               no flow control
      Using both hardware and software flow control together is not supported

![Image](gfx/tdsgrab.png?raw=true)
![Image](gfx/hardcopy.png?raw=true)


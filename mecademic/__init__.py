import sys
import socket

from threading import Thread
from time import sleep
import re

message_pattern = re.compile("\[(\d+)\]\[(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+),(-?\d+\.\d+)\]")

class MecaRobot:
    """Robot class for programming Mecademic robots"""

    def __init__(self,
                 host="192.168.0.100",
                 control_port=10000,
                 monitor_port=10001):

        self.BUFFER_SIZE = 512  # bytes
        self.TIMEOUT = 999999  # seconds

        self._control_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._control_sock.settimeout(self.TIMEOUT)

        self._monitor_sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

        self.__log('Connecting to robot %s:%i' % (host, control_port))

        self._control_sock.connect((host, control_port))
        self._monitor_sock.connect((host, monitor_port))

        self.monitor_thread = Thread(target=self.recv_feedback)
        self.monitor_thread.start()

        self.monitor_handler = None

        self.__log('Waiting for welcome message...')
        self.__log(self.__recv_str())

        # Reset errors, send activate robot and read confirmation
        self._control_sock.settimeout(10)
        self.run('ResetError', sync=True)
        self.run('ActivateRobot', sync=True)
        self._control_sock.settimeout(30)
        self.run('Home', sync=True)

    def recv_feedback(self):
        while True:
            data = self._monitor_sock.recv(512).decode('ascii')

            for result in message_pattern.finditer(data):
                code = result.groups()[0]
                value1 = float(result.groups()[1])
                value2 = float(result.groups()[2])
                value3 = float(result.groups()[3])
                value4 = float(result.groups()[4])
                value5 = float(result.groups()[5])
                value6 = float(result.groups()[6])

                if self.monitor_handler:
                    self.monitor_handler(code, [value1, value2, value3, value4, value5, value6])


    def __log(self, *args):
        print('[MecaRobot]', *args)
        sys.stdout.flush()

    def __send_str(self, msg):
        sent = self._control_sock.send(bytes(msg + '\0', 'ascii'))
        if sent == 0:
            raise RuntimeError("Robot connection broken")

    def __recv_str(self):
        bdata = self._control_sock.recv(self.BUFFER_SIZE)
        if bdata == b'':
            raise RuntimeError("Robot connection broken")
        return bdata.decode('ascii')

    def run(self, cmd, values=None, sync=False):
        if isinstance(values, list):

            str_send = cmd + '(' + (','.join(format(vi, ".6f") for vi in values)) + ')'
        elif values is None:
            str_send = cmd
        else:
            str_send = cmd + '(' + str(values) + ')'

        # self.__log('out', str_send)
        sys.stdout.flush()

        # send command to robot
        self.__send_str(str_send)
        if sync:
            recv = self.__recv_str()
            self.__log('--> %s' % recv)
            sys.stdout.flush()
            return recv

    def get_joints(self):
        recv = self.run('GetJoints', sync=True)
        return [float(angle) for angle in recv[7:-2].split(',')]

    def monitor(self, handler):
        self.monitor_handler = handler

    def log(self, handler):
        self.log_handler = handler

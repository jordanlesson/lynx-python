from account import Account
from message import Message
import socket
import traceback
import threading


def display_debug(msg):
    """Prints a message to the screen with the name of the current thread"""
    print("[%s] %s" % (str(threading.currentThread().getName()), msg))


class PeerConnection:

    # ------------------------------------------------------------------------------
    def __init__(self, peer_id, host, port, sock=None, debug=False) -> None:
        # --------------------------------------------------------------------------
        """Any exceptions thrown upwards"""

        self.id = peer_id
        self.debug = debug

        if sock is None:
            self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.s.connect((host, int(port)))
        else:
            self.s = sock

    # ------------------------------------------------------------------------------
    def __debug(self, message) -> None:
        # --------------------------------------------------------------------------
        if self.debug:
            display_debug(message)

    # ------------------------------------------------------------------------------
    def __make_message(self, message_type, message_flag, message_data) -> Message:
        # --------------------------------------------------------------------------
        """Packs the message into a Message object and then signs it using the 
        provided Account object.

        For more information about packing visit: https://docs.python.org/3/library/struct.html
        """

        message = Message(type=message_type,
                          flag=message_flag, data=message_data)
        return message

    # ------------------------------------------------------------------------------
    def send_data(self, message_type: str, message_flag: int, message_data: dict = None) -> bool:
        # --------------------------------------------------------------------------
        """Send a message through a peer connection. Returns True on success or 
        False if there was an error.
        """

        try:
            message = self.__make_message(
                message_type, message_flag, message_data)
            message_JSON = message.to_JSON()
            message_binary = message_JSON.encode()
            self.s.send(message_binary)
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                self.__debug('Unable to send data: {}'.format(message_data))
                traceback.print_exc()
            return False
        return True

    # ------------------------------------------------------------------------------
    def receive_data(self) -> Message:
        # --------------------------------------------------------------------------
        """Receive a message from a peer connection. Returns an None if there was 
        any error.
        """
        self.__debug('Attempting to receive data...')

        try:
            message_JSON = self.s.recv(1024).decode()
            message = Message.from_JSON(message_JSON)
            return message
        except KeyboardInterrupt:
            raise
        except:
            if self.debug:
                # traceback.print_exc()
                print()
            return None

    # ------------------------------------------------------------------------------
    def close(self) -> None:
        # --------------------------------------------------------------------------
        """Close the peer connection. The send and receive methods will not work
        after this call.
        """

        self.__debug('Closing peer connection with %s' % self.id)
        self.s.close()
        self.s = None
        self.sd = None

    # ------------------------------------------------------------------------------
    def __str__(self) -> str:
        # --------------------------------------------------------------------------
        """"""

        return "|%s|" & id

# end PeerConnection class

"""
There are two main types of equipment one can have in the lab:


"""
import abc
import zmq
import hepbasestack.logger as log
import skippylab

Logger = log.get_logger(skippylab.LOGLEVEL)

class AbstractBaseInstrument(object):

    METADATA = { "name"     : "RaspberryPiDHT22-4Channel",
                 "twinax"   : True,
                 "units"    : ["C", "\%"],
                 "channels" : 4}
    

    def __init__(self,
                 controller=None,
                 loglevel=20,\
                 publish=False,
                 publish_port=9876):
        """
        Constructor needs read and write access to
        the port

        Keyword Args:
            publish_port (str): The port on which data will be published 
                                in case publish = True
            loglevel (int): 10: debug, 20: info, 30: warnlng....
            publish (bool): publish data on port
            publish_port (int): use this port if publish = True
        """
        self.controller = controller # default settings are ok
        self.logger = Logger
        self.logger.debug("Instrument initialized")
        self.publish = publish
        self.port = publish_port
        self._socket = None
        self.axis_label = None

    def identify(self):
        """
        Tell the user what type of instrument it is and 
        how many channels, units etc...
        """
        return self.METADATA


    def _setup_port(self):
        """
        Setup the port for publishing

        Returns:
            None
        """
        context = zmq.Context()
        self._socket = context.socket(zmq.PUB)
        self._socket.bind("tcp://0.0.0.0:%s" % int(self.port))
        return


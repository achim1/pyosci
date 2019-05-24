#! /usr/bin/env python3

import numpy as np
from skippylab.instruments import RaspberryPiGPIODHT22Thermometer
from skippylab.controllers import ZMQController


if __name__ == "__main__":

    controller = ZMQController(ip="168.105.246.157",topicfilter="FREEZER", encoder=RaspberryPiGPIODHT22Thermometer.encode_payload)
    thermo = RaspberryPiGPIODHT22Thermometer(controller=controller)
    for k in thermo.measure_continuously(measurement_time=np.inf):
        print (k)


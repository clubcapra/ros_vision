from ..filter import Filter
from ..filter_descriptor import FilterDescriptor
from ..parameter_descriptor import ParameterDescriptor
from ..io_descriptor import IODescriptor
from ...IO.image import Image
import cv2
import numpy as np


class HSVThresholdFilter(Filter):
    descriptor = FilterDescriptor("HSVThreshold", "Thresholds an HSV image",
                                  inputs=[IODescriptor("input", "BGR image.", Image)],
                                  outputs=[IODescriptor("output", "HSV image.", Image)],
                                  parameters=[ParameterDescriptor("min_hue", "Minimum hue", int, 0, 0, 180),
                                              ParameterDescriptor("max_hue", "Maximum hue", int, 180, 0, 180),
                                              ParameterDescriptor("min_saturation", "Minimum saturation", int, 0, 0, 255),
                                              ParameterDescriptor("max_saturation", "Maximum saturation", int, 255, 0, 255),
                                              ParameterDescriptor("min_value", "Minimum value", int, 0, 0, 255),
                                              ParameterDescriptor("max_value", "Maximum value", int, 255, 0, 255)
                                              ])

    def initialize(self):
        print "Init %s" % self.name

    def execute(self, time=0):
        im = self.get_input("input")
        if im:
            min_hsv = np.array([self.get_param("min_hue"), self.get_param("min_saturation"), self.get_param("min_value")], np.uint8)
            max_hsv = np.array([self.get_param("max_hue"), self.get_param("max_saturation"), self.get_param("max_value")], np.uint8)

            im2 = Image(cv2.inRange(im.get_image(), min_hsv, max_hsv))
            im.copy_header(im2)
            self.set_output("output", im2)
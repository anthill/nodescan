import matplotlib
matplotlib.use('Agg')

# import the necessary packages
from scanner import core
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2
import pylab as plt
import matplotlib.cm as cm
import shutil
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image to be scanned")
ap.add_argument("-o", "--out", default= "./", required = False, help = "Path to the output image.")
ap.add_argument("-n", "--name", default= "out", required = False, help = "Name of the resulting file image.")
ap.add_argument("-k", "--koriginal", default= "fasle", required = False, help = "Whether to keep original image.")
ap.add_argument("-b", "--bw", required = False, help = "Black and white: true or false")
ap.add_argument("-f", "--format", default="pdf", required = False, help = "Specify the format.")
ap.add_argument("-p", "--dpi", default=300, required = False, help = "Specify the dpi resolution.")
ap.add_argument("-a", "--a4", default="false", required = False, help = "Format to A4 paper.")
args = vars(ap.parse_args())

core.processImage(args)
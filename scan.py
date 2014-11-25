# USAGE
# python scan.py --image images/page.jpg

import matplotlib
matplotlib.use('Agg')

# import the necessary packages
from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
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

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])

ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

edged = cv2.Canny(image, 75, 200)

# res = np.hstack((gray,eqgray))

# find the contours in the edged image, keeping only the
# largest ones, and initialize the screen contour
(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)


# take the biggest contour
perimeters = map(lambda x: cv2.arcLength(x, False), cnts)
index = np.argmax(perimeters)
contour = cnts[index]

def removeInlier(points, closeLine=False):
	initial_area = cv2.contourArea(points);
	new_contour = points
	ratios = []
	for i in range(len(points)):
		# new_contour = points.pop(i)
		new_contour = np.delete(new_contour,i,0)
		new_area = cv2.contourArea(new_contour);
		ratios+=[new_area/initial_area]
		new_contour = points
	index = np.argmax(ratios)
	return np.delete(points,index,0)


# approximate the contour
peri = cv2.arcLength(contour, True)
approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
approx = cv2.convexHull(approx)
approx = approx.reshape((len(approx),2))
while len(approx)>4 :
	approx = removeInlier(approx)



# apply the four point transform to obtain a top-down
# view of the original image
warped = four_point_transform(orig, approx.reshape(4, 2) * ratio)

if args["bw"] == "true":
	warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
	warped = threshold_adaptive(warped, 40, offset = 7)
	warped = warped.astype("uint8") * 255
else:
	b,g,r = cv2.split(warped)       # get b,g,r
	warped = cv2.merge([r,g,b])     # switch it to rgb

final = imutils.resize(warped, height = 650)


fig = plt.figure(frameon=False)
if str(args["a4"]) == "true":
	fig.set_size_inches(8.27, 11.69)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)
else:
	fig.set_size_inches(3, 3*ratio)
	ax = plt.Axes(fig, [0., 0., 1., 1.])
	ax.set_axis_off()
	fig.add_axes(ax)

if args["bw"] == "true":
	ax.imshow(final, aspect='normal', cmap = plt.get_cmap('gray'))
else:
	ax.imshow(final, aspect='normal')

format = str(args["format"])
path = str(args["out"])
plt.savefig(path + str(args["name"]) + "." + format, format=format, dpi=int(args["dpi"]))

if args["koriginal"]:
	orig_path = args["image"]
	orig_format = orig_path.split(".")[-1]
	shutil.copyfile(orig_path, path + str(args["name"]) + "." + orig_format )


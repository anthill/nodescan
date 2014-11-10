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
# construct the argument parser and parse the arguments
ap = argparse.ArgumentParser()
ap.add_argument("-i", "--image", required = True, help = "Path to the image to be scanned")
args = vars(ap.parse_args())

# load the image and compute the ratio of the old height
# to the new height, clone it, and resize it
image = cv2.imread(args["image"])

b,g,r = cv2.split(image)       # get b,g,r
image = cv2.merge([r,g,b])     # switch it to rgb

ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

# convert the image to grayscale, blur it, and find edges
# in the image
# gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
# gray = cv2.GaussianBlur(image, (5, 5), 0)

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

# convert the warped image to grayscale, then threshold it
# to give it that 'black and white' paper effect
# warped = cv2.cvtColor(warped, cv2.COLOR_BGR2GRAY)
# warped = threshold_adaptive(warped, 250, offset = 10)
# warped = warped.astype("uint8") * 255

final = imutils.resize(warped, height = 650)


fig = plt.figure(frameon=False)
fig.set_size_inches(8.27, 11.69)
ax = plt.Axes(fig, [0., 0., 1., 1.])
ax.set_axis_off()
fig.add_axes(ax)
ax.imshow(final, aspect='normal')
plt.savefig("out.pdf", format='pdf')
# plt.show()

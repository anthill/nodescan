from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2
import pylab as plt
import matplotlib.cm as cm

image = cv2.imread("/Users/vallette/Desktop/photo.JPG")
# image = cv2.imread("/Users/vallette/Desktop/IMG_2827.JPG")

b,g,r = cv2.split(image)       # get b,g,r
image = cv2.merge([r,g,b])     # switch it to rgb

ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

edged = cv2.Canny(image, 75, 200)

(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = cv2.contourArea, reverse = True)



fig = plt.figure(frameon=False)


plt.imshow(image)
# plt.savefig("out.pdf", format='pdf')
for contour in cnts:
	peri = cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
	print len(approx)
	cntr = np.array(map(lambda x: x[0], approx)).T
	plt.plot(cntr[0], cntr[1])
plt.show()
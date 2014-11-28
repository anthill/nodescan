from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2
import pylab as plt
import matplotlib.cm as cm

image = cv2.imread("/Users/vallette/Desktop/IMG_4879.JPG")

b,g,r = cv2.split(image)       # get b,g,r
image = cv2.merge([r,g,b])     # switch it to rgb

ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

edged = cv2.Canny(image, 75, 200)

(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
cnts = sorted(cnts, key = lambda x: cv2.arcLength(x, False), reverse = True)[:2]
cnts = sorted(cnts, key = lambda x: cv2.contourArea(x, False), reverse = True)[:1]
# perimeters = map(lambda x: cv2.arcLength(x, False), cnts)
# index = np.argmax(perimeters)
# cnts = [cnts[index]]

# fig = plt.figure(frameon=False)

# plt.imshow(image)
# for i in range(len(cnts)):
# 	A=cnts[i].T
# 	print A
# 	plt.plot(A[0][0], A[1][0])


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

# fig = plt.figure(frameon=False)
# plt.imshow(image)

# for contour in cnts:
# 	peri = cv2.arcLength(contour, True)
# 	approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
# 	approx = cv2.convexHull(approx)
# 	approx = approx.reshape((len(approx),2))
# 	while len(approx)>4 :
# 		approx = removeInlier(approx)

# 	cntr = np.array(approx).T
# 	plt.plot(cntr[0], cntr[1], '-')
# 	for x,y in zip(cntr[0], cntr[1]):
# 		plt.plot(x,y,"o")
plt.show()
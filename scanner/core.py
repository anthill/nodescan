
import matplotlib
matplotlib.use('Agg')

from transform import four_point_transform
import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2
import pylab as plt
import matplotlib.cm as cm
import shutil


def processImage(args):
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

	# sort by perimeter first and then area
	cnts = sorted(cnts, key = lambda x: cv2.arcLength(x, False), reverse = True)[:3]
	contour = sorted(cnts, key = lambda x: cv2.contourArea(x, False), reverse = True)[0]

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
	sheet_ratio = final.shape[0]/float(final.shape[1])

	fig = plt.figure(frameon=False)
	if str(args["a4"]) == "true":
		fig.set_size_inches(8.27, 11.69)
		ax = plt.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)
	else:
		fig.set_size_inches(3, 3/sheet_ratio)
		ax = plt.Axes(fig, [0., 0., 1., 1.])
		ax.set_axis_off()
		fig.add_axes(ax)

	if args["bw"] == "true":
		ax.imshow(final, aspect='auto', cmap = plt.get_cmap('gray'))
	else:
		ax.imshow(final, aspect='auto')

	format = str(args["format"])
	path = str(args["out"])
	plt.savefig(path + str(args["name"]) + "./" + format, format=format, dpi=int(args["dpi"]))

	if args["koriginal"] == "true":
		orig_path = args["image"]
		orig_format = orig_path.split(".")[-1]
		shutil.copyfile(orig_path, path + str(args["name"]) + "." + orig_format )


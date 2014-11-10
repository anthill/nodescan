from pyimagesearch.transform import four_point_transform
from pyimagesearch import imutils
from skimage.filter import threshold_adaptive
import numpy as np
import argparse
import cv2
import pylab as plt
import matplotlib.cm as cm

image = cv2.imread("/Users/vallette/Desktop/photo2.JPG")

b,g,r = cv2.split(image)       # get b,g,r
image = cv2.merge([r,g,b])     # switch it to rgb

ratio = image.shape[0] / 500.0
orig = image.copy()
image = imutils.resize(image, height = 500)

edged = cv2.Canny(image, 75, 200)

(cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)
# cnts = sorted(cnts, key = lambda x: cv2.arcLength(x, False), reverse = True)[:1]
perimeters = map(lambda x: cv2.arcLength(x, False), cnts)
index = np.argmax(perimeters)
cnts = [cnts[index]]

fig = plt.figure(frameon=False)

def removeInlier(points, closeLine=False):

	def getPermut(l, pos, delta):
		if pos+delta <0:
			return l[len(l)+(pos+delta)]
		elif pos+delta>len(l)-1:
			reste = (pos+delta) % len(l)
			return l[reste]
		else:
			return l[pos+delta]

	point2edges = {}
	for i in range(len(points)):
		point = points[i]
		p2 = getPermut(points, i, -1)
		p3 = getPermut(points, i, +1)
		d2 = np.sqrt((point[0]-p2[0])**2 + (point[1]-p2[1])**2)
		d3 = np.sqrt((point[0]-p3[0])**2 + (point[1]-p3[1])**2)
		print point, p2,p3
		print d2, d3
		point2edges[i] = [d2, d3]

	minVal = min(np.array(point2edges.values()).flatten())
	candidates = []
	for k,v in point2edges.items():
		if minVal in v:
			candidates += [k]
	print minVal
	print point2edges
	print candidates
	a = point2edges[candidates[0]]
	a.remove(minVal)
	b = point2edges[candidates[1]]
	b.remove(minVal)
	if a[0] > b[0]:
		index = candidates[0]
	else:
		index = candidates[1]
	print "index", index
	if not closeLine:
		points = np.delete(points, index, 0)
		return points
	else:
		pp1 = getPermut(points, index-1, -1)
		pp2 = getPermut(points, index-1, -2)
		pp3 = getPermut(points, index-1, +1)
		pp4 = getPermut(points, index-1, +2)

		X = float(pp3[1]-pp1[1] + (pp2[1]-pp1[1])/(pp2[0]-pp1[0])*pp1[0] - float(pp4[1]-pp3[1])/(pp4[0]-pp3[0])*pp3[0])/(float(pp2[1]-pp1[1])/(pp2[0]-pp1[0]) - float(pp4[1]-pp3[1])/(pp4[0]-pp3[0]))
		Y = float(pp2[1]-pp1[1])/(pp2[0]-pp1[0])*(X-pp1[0])+pp1[1]
		points[index-1] = [X,Y]
		return points

def removeInlier2(points, closeLine=False):
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

plt.imshow(image)

for contour in cnts:
	peri = cv2.arcLength(contour, True)
	approx = cv2.approxPolyDP(contour, 0.02 * peri, True)
	approx = cv2.convexHull(approx)
	approx = approx.reshape((len(approx),2))
	while len(approx)>4 :
		approx = removeInlier2(approx)

	cntr = np.array(approx).T
	plt.plot(cntr[0], cntr[1], '-')
	for x,y in zip(cntr[0], cntr[1]):
		plt.plot(x,y,"o")
plt.show()
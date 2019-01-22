import cv2
from matplotlib import pyplot as plt
import numpy as np
from math import cos, sin

green = (0, 255, 0)
red = (255,0,0)

def overlay_mask(mask, image):
    rgb_mask = cv2.cvtColor(mask, cv2.COLOR_GRAY2RGB)
    img = cv2.addWeighted(rgb_mask, 0.5, image, 0.5, 0)
    return img


def find_contour(image):
	image = image.copy()
	cont = list()
	coord = list()
	_, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)	
	mask = np.zeros(image.shape, np.uint8)
	for contour in contours:
		if(cv2.contourArea(contour)>250):
			cont.append(contour)
			coord.append((contour[1]+contour[2])/2)
	cv2.drawContours(mask, cont, -1, 255, -1)
	return cont, mask,coord

def find_contour2(image):
	image = image.copy()
	cont = list()
	coord = list()
	_, contours, hierarchy = cv2.findContours(image, cv2.RETR_LIST, cv2.CHAIN_APPROX_SIMPLE)	
	mask = np.zeros(image.shape, np.uint8)
	for contour in contours:
		if(cv2.contourArea(contour)>450):
			cont.append(contour)
			coord.append((contour[1]+contour[2])/2)
	cv2.drawContours(mask, cont, -1, 255, -1)
	return cont, mask, coord

def circle_plane(image, contour):
    image_with_ellipse = image.copy()
    ellipse = cv2.fitEllipse(contour)
    cv2.ellipse(image_with_ellipse, ellipse, green, 2, cv2.LINE_AA)
    return image_with_ellipse


def circle_plane2(image, contour):
    image_with_ellipse = image.copy()
    ellipse = cv2.fitEllipse(contour)
    cv2.ellipse(image_with_ellipse, ellipse, red, 2, cv2.LINE_AA)
    return image_with_ellipse


def find_RedPlane(image):
	count=0
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	max_dimension = max(image.shape)
	scale = 700 / max_dimension
	image = cv2.resize(image, None, fx=scale, fy=scale)
	image1 = image.copy()
	image_blur = cv2.GaussianBlur(image, (7, 7),0)
	image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
	min_red = np.array([0, 100, 80])
	max_red = np.array([10, 256, 256])
	mask1 = cv2.inRange(image_blur_hsv, min_red, max_red)
	min_red2 = np.array([170, 100, 80])
	max_red2 = np.array([180, 256, 256])
	mask2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)
	mask = mask1 + mask2
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
	mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
	plane_contour, mask_plane,coords = find_contour(mask_clean)
	overlay = overlay_mask(mask_clean, image)
	for contour in plane_contour:
		circled = circle_plane(overlay, contour)
		image1 = circle_plane(image1, contour)
		count+=1
	bgr = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)
	

	return bgr,count,coords

def find_GrayPlane(image):
	count=0
	image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
	max_dimension = max(image.shape)
	scale = 700 / max_dimension
	image = cv2.resize(image, None, fx=scale, fy=scale)
	image1 = image.copy()
	image_blur = cv2.GaussianBlur(image, (7, 7),0)
	image_blur_hsv = cv2.cvtColor(image_blur, cv2.COLOR_RGB2HSV)
	min_red2 = np.array([0, 0, 0])
	max_red2 = np.array([128, 128, 128])
	mask2 = cv2.inRange(image_blur_hsv, min_red2, max_red2)
	mask = mask2
	kernel = cv2.getStructuringElement(cv2.MORPH_ELLIPSE, (15, 15))
	mask_closed = cv2.morphologyEx(mask, cv2.MORPH_CLOSE, kernel)
	mask_clean = cv2.morphologyEx(mask_closed, cv2.MORPH_OPEN, kernel)
	plane_contour, mask_plane, coords = find_contour2(mask_clean)
	overlay = overlay_mask(mask_clean, image)
	for contour in plane_contour:
		circled = circle_plane2(overlay, contour)
		image1 = circle_plane2(image1, contour)
		count+=1
	bgr = cv2.cvtColor(image1, cv2.COLOR_RGB2BGR)

	return bgr,count, coords

try:	
	t = int(input("No. of test cases: "))
	for i in range(t):
		s = input("Name of image(if it is in same directory, or full path): ")
		image = cv2.imread(s+".jpg")
		resultR,countR, coordsR= find_RedPlane(image)
		resultG,countG,coordsG = find_GrayPlane(resultR)
		cv2.imwrite('circled_'+s+".jpg", resultG)
		print("No. of Red plane/planes: ",countR)
		if(countR!=0):
			print("Coordinates of Red Plane/Planes are as follows: ")
		for j in range(countR):
			print(j+1,coordsR[j])
		print("No. of Gray plane/planes: ", countG)
		if(countG!=0):
			print("Coordinates of Gray Plane/Planes are as follows: ")
		for j in range(countG):
			print(j+1,coordsG[j])
		
except ValueError:
	print('Oops! Something really wrong happened :/ ')
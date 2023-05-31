import json
import cv2
import numpy as np

#some parameters for lighting etc.
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)
detectorParams = cv2.aruco.DetectorParameters_create()

#function to save data to a file
def saveJSON(filename, data):
  out = json.dumps(data)
  with open(filename, 'w') as f:
    f.write(out)

#function to load a file into a data variable
def loadJSON(filename):
  with open(filename, 'r') as f:
    data = json.loads(f.read())
    return data

#function to detect an arucocode
def detectAruco(gray):
  markerCorners, markerIds, rejected = cv2.aruco.detectMarkers(gray, dictionary)
  return markerCorners, markerIds

#function that finds the center and up direction of an arucocode.
def centerAndUp(corners):
  corners = np.squeeze(corners)
  center = (corners[0] + corners[1] + corners[2] + corners[3]) / 4.0
  up = (corners[0] + corners[1]) / 2.0

  return center, up
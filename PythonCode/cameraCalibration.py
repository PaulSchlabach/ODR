import cv2
import util as u
import objectTracking as ObT

#CameraCalibration script will create a distortion matrix using an Arucoboard
                                                   
dictionary = cv2.aruco.getPredefinedDictionary(cv2.aruco.DICT_5X5_50)           #Sets which Aruco board is used


board = cv2.aruco.CharucoBoard_create(5,7,.1,.05, dictionary)                   #Creates Arucoboard according to dimensions and dictionary
#img = board.draw((200*3,200*3))
#cv2.imwrite("charuco.png", img)

REQUIRED_COUNT = 25                                                             #How many images are needed for calibration

allCorners = [] 
allIds = [] 


frameIdx = 0                                                                     #Only update few frames so we get more diverse data
frameSpacing = 5
success = False

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)
if not (cap.isOpened()):
    print("Could not open video device")
while True:
  ret, frame = cap.read()
  gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
  markerCorners, markerIds, = u.detectAruco(gray)

  if len(markerCorners) > 0 and frameIdx % frameSpacing == 0:
    ret, charucoCorners, charucoIds = cv2.aruco.interpolateCornersCharuco(markerCorners, markerIds, gray, board)
    if charucoCorners is not None and charucoIds is not None and len(charucoCorners) > 3:
      allCorners.append(charucoCorners)
      allIds.append(charucoIds)

    cv2.aruco.drawDetectedMarkers(gray, markerCorners, markerIds)

  cv2.imshow('frame',gray)

  if cv2.waitKey(1) & 0xFF == ord('q'):
    break

  frameIdx += 1
  print("Found: " + str(len(allIds)) + " / " + str(REQUIRED_COUNT))

  if len(allIds) >= REQUIRED_COUNT:
    success = True
    break

if success:
  print('Done collecting data, computing...')

  try:
    err, cameraMatrix, distCoeffs, rvecs, tvecs = cv2.aruco.calibrateCameraCharuco(allCorners, allIds, board, ObT.resolution, None, None)
    print('Calibrated with err', err)

    newCameraMatrix, validPixROI = cv2.getOptimalNewCameraMatrix(cameraMatrix, distCoeffs, ObT.resolution, 0)

    u.saveJSON(r"C:\Users\pschl\Desktop\UTwente\Thesis\ODR\PythonCode\CalibrationData\distortionMatrix.json", {
      'cameraMatrix': cameraMatrix.tolist(),
      'distCoeffs': distCoeffs.tolist(),
      'newCameraMatrix': newCameraMatrix.tolist(),
      'validPixROI': validPixROI,
    })
    print('...done!')

  except Exception as err:
    print(err)
    success = False

cap.release()
cv2.destroyAllWindows()


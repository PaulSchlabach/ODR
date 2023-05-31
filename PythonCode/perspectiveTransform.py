import cv2
import numpy as np
import util as u
from objectTracking import undistort

def four_point_transform(rect):
    # obtain a consistent order of the points and unpack them
    # individually
    (tl, tr, br, bl) = rect
    # compute the width of the new image, which will be the
    # maximum distance between bottom-right and bottom-left
    # x-coordiates or the top-right and top-left x-coordinates
    widthA = np.sqrt(((br[0] - bl[0]) ** 2) + ((br[1] - bl[1]) ** 2))
    widthB = np.sqrt(((tr[0] - tl[0]) ** 2) + ((tr[1] - tl[1]) ** 2))
    maxWidth = max(int(widthA), int(widthB))
    # compute the height of the new image, which will be the
    # maximum distance between the top-right and bottom-right
    # y-coordinates or the top-left and bottom-left y-coordinates
    heightA = np.sqrt(((tr[0] - br[0]) ** 2) + ((tr[1] - br[1]) ** 2))
    heightB = np.sqrt(((tl[0] - bl[0]) ** 2) + ((tl[1] - bl[1]) ** 2))
    maxHeight = max(int(heightA), int(heightB))
    # now that we have the dimensions of the new image, construct
    # the set of destination points to obtain a "birds eye view",
    # (i.e. top-down view) of the image, again specifying points
    # in the top-left, top-right, bottom-right, and bottom-left
    # order
    dst = np.array([
        [0, 0],
        [maxWidth - 1, 0],
        [maxWidth - 1, maxHeight - 1],
        [0, maxHeight - 1]], dtype="float32")
    # compute the perspective transform matrix and then apply it
    M = cv2.getPerspectiveTransform(np.float32(rect), dst)
    return M, maxWidth, maxHeight

perspectiveTransform = None

cap = cv2.VideoCapture(1, cv2.CAP_DSHOW)  # video capture source camera (Here webcam of laptop)

ret, frame = cap.read()  # return a single frame in variable `frame`

gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
undist = undistort(gray)

while (True):
    cv2.imshow('img1', gray)  # display the captured image
    if cv2.waitKey(1) & 0xFF == ord('y'):  # save on pressing 'y'
        cv2.imwrite('images/c1.png', gray)
        cv2.destroyAllWindows()
        break

cap.release()

#saves corners of the markers with its id
markerCorners, markerIds = u.detectAruco(gray)

#makes the rectangle between the 4 points
if len(markerIds) == 4:
    upLeftCorner = np.squeeze(markerCorners[int(np.where(markerIds == [23])[0])])[2]
    upRightCorner = np.squeeze(markerCorners[int(np.where(markerIds == [24])[0])])[3]
    downLeftCorner = np.squeeze(markerCorners[int(np.where(markerIds == [25])[0])])[1]
    downRightCorner = np.squeeze(markerCorners[int(np.where(markerIds == [26])[0])])[0]

    rect = [upLeftCorner, upRightCorner, downRightCorner, downLeftCorner]


    transform_matrix, maxWidth, maxHeight = four_point_transform(rect)
    print(transform_matrix)
    u.saveJSON(r"C:\Users\pschl\Desktop\UTwente\Thesis\ODR\PythonCode\CalibrationData\transformationMatrix.json",
               dict(transform_matrix=transform_matrix.tolist(), maxWidth=maxWidth, maxHeight=maxHeight))

else:
    print("Not all ArUco codes where found!")
    print(markerIds)

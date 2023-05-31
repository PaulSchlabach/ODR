import cv2
import numpy as np
import util as u
from robotMovement import Movement
from robotCommunication import SendSignals, EstablishConnection
import time
import threading

robotCenter = None
robotUp = None
resolution = (3840, 2160)

goalcoordinates= [0,0]

cap = cv2.VideoCapture(1,cv2.CAP_DSHOW)
font = cv2.FONT_HERSHEY_SIMPLEX

def mouse_callback(event, x, y,flags,param):
    if event == cv2.EVENT_LBUTTONDOWN:
        goalcoordinates[0] = x
        goalcoordinates[1] = y
        
def transform(gray):
    transformData = u.loadJSON(r"C:\Users\pschl\Desktop\UTwente\Thesis\ODR\PythonCode\CalibrationData\transformationMatrix.json")
    warped = cv2.warpPerspective(gray, np.float32(transformData["transform_matrix"]), (transformData["maxWidth"], transformData["maxHeight"]))
    return warped

def undistort(gray):
    distortionData = u.loadJSON(r"C:\Users\pschl\Desktop\UTwente\Thesis\ODR\PythonCode\CalibrationData\distortionMatrix.json")
    dst = cv2.undistort(gray, np.float32(distortionData["cameraMatrix"]), np.float32(distortionData["distCoeffs"]),
                        None, np.float32(distortionData["newCameraMatrix"]))

    x, y, w, h = distortionData["validPixROI"]
    dst = dst[y:y + h, x:x + w]
    return dst

def arucocenterupfind(warped):
    robotCorners, robotId = u.detectAruco(warped)

    robotCenter = [0, 0]
    robotUp = [0, 0]
    if robotId == [30]:
        robotCenter, robotUp = u.centerAndUp(robotCorners)

        return robotCenter, robotUp
    

def Interface():
    con = threading.Thread(target=EstablishConnection)
    con.start()
    while True:
        ret, frame = cap.read()
        gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
        dst = undistort(gray)
        warped = transform(gray)    
        
        cv2.circle(warped, (int(goalcoordinates[0]),int(goalcoordinates[1])), 4, (255, 0, 0), -1)
        cv2.putText(warped, "XGoal: " + str(goalcoordinates[0]) + "   " + "YGoal: " + str(goalcoordinates[1]), (270,320),font,0.5,(255,0,0),1)
        if arucocenterupfind(warped) is not None:
            robotCenter, robotUp = arucocenterupfind(warped)
            cv2.putText(warped, "X: " + str(robotCenter[0]) + "   " + "Y: " + str(robotCenter[1]), (50,320),font,0.5,(255,0,0),1)
            cv2.circle(warped, (int(robotCenter[0]), int(robotCenter[1])), 4, (0, 255, 255), -1)
            cv2.arrowedLine(warped, (int(robotCenter[0]),int(robotCenter[1])), (int(robotUp[0]),int(robotUp[1])), (255, 255, 0), 4)
            PWM = Movement(robotCenter, goalcoordinates)
            t = threading.Thread(target=SendSignals, args=PWM)
            t.start()
        else:
            cv2.putText(warped, "X: " + str(0) + "   " + "Y: " + str(0), (50,320),font,0.5,(255,0,0),1) 
        cv2.imshow("transform", warped)
        cv2.setMouseCallback('transform', mouse_callback) 
        if cv2.waitKey(1) & 0xFF == ord("q"):
            break   
        time.sleep(0.01)
    cap.release()
    cv2.destroyAllWindows()
   
InterfaceThread = threading.Thread(target=Interface)
InterfaceThread.start()
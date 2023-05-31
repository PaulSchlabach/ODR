# Robot Positioning using Camera Location Tracking
This project is my bachelor thesis which utilizes omnidirectional robots and camera location tracking in order to enable rapid prototyping with a VR interface.

Disclaimer: Some of this code is taken and adapted from Jacco Reuling.

## Installation Guide on Windows

1. Create new folder named "ODR"

2. Paste project files into folder

3. In CMD change directory to ODR

```bash
cd C:\change\this\to\your\file\path\ODR
```

4. Create a new virtual enivronment using venv

```bash
python -m venv yourvenvname
```

5. Activate virtual enivronment

```bash
yourvenvname\Scripts\activate
```
6. Install libraries used in the project using pip

```bash
pip install -r requirements.txt
```
7. Print Arucocodes in folder Arucocodes

8. Execute cameraCalibration.py and move Arucoboard in front of camera until finished

9. Place Arucocodes on the corners of the camera FOV, (DL DownLeft, DR DownRight, UL UpLeft, UR UpRight) and execute perspectiveTransform.py if Arucocodes are positioned correctly press y

10. Place Arucocode robot1.png on the robot and place within FOV of camera

11. Turn on robot and wait until it is connected with the Wi-Fi

12. Execute main.py, the robots location should be tracked and attempt to move towards goal location, goal location can be set to desired location by leftclicking the camera image

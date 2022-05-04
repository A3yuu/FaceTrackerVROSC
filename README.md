# FaceTrackerVROSC

You will be able to move your mouth from the camera with VRChat OSC

Uses Wireless M5 Camera X

*It works with a webcam with a slight change in code.

## How install

### Requests
■M5

ESP32 on ArduinoIDE

https://docs.espressif.com/projects/arduino-esp32/en/latest/installing.html

■PC

Python and some requirements

### 1.M5
*No need for a webcam

Open the WirelessCam.ino

Change each of the following to an appropriate value
```
String networkName = "YourSSID";
String networkPswd = "YourPW";
String networkAddress = "192.168.your.PCIP";
```

Write to M5CameraX

Attach to HMD

![施工](https://user-images.githubusercontent.com/21051958/166640802-634926ee-599e-4ed6-ae7c-dbf08758499d.jpg)

### 2.Download

Download 300w image dataset

https://ibug.doc.ic.ac.uk/resources/facial-point-annotations/

Place the "01_Indoor" folder in the downloaded file in the FaceTracker folder

### 3.Learning

Run data.bat

Run learn.bat

### 4.Run

Turn on the camera

Run run.bat

### 5.Avatar

Copy "Assets"

Set the VRC Avatar Descriptor following 2

・Playable Layers - FX → Animator_FX

・Expressions → VRCExpressionsMenu, VRCExpressionParameters

Face mesh rename "Body" and create follow blend shapes

にやり：Mouth smaile

お：Mouth open

口右：Move mouth to the right

口左：Move mouth to the left

口すぼみ：Mouth dent

口広：Stretch mouth sideways

## Donate

https://a3s.booth.pm/items/3837150

## Twitter

https://twitter.com/A3_yuu
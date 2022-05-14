import socket
import threading
import numpy
import cv2
from tensorflow.python.keras.models import load_model
from pythonosc import udp_client
import os
import sys

#CPU
os.environ['CUDA_VISIBLE_DEVICES'] = '-1'

#NetWorkDNL
model = load_model('t.h5py')
model.load_weights('t.weights')
model.compile(loss='categorical_crossentropy',optimizer='rmsprop',metrics=['accuracy'])

cameraDev = int(sys.argv[1])

#WebCam
if(cameraDev>=0):
	cap = cv2.VideoCapture(cameraDev)
	cap.set(cv2.CAP_PROP_FRAME_WIDTH, 240)
	cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 240)
	cameraW = int(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
	cameraH = int(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))
	cropLen = int((cameraW-cameraH)/2)

#NetworkCam
else:
	imageBuf= []
	def network():
		print("start")
		HOST = ''   
		PORT = 3333
		s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)
		s.bind((HOST, PORT))
		nowid=-1
		frag = 1024
		packet=-1
		while True:
			msg, address = s.recvfrom(1500)
			id = msg[0]
			size = msg[1] + msg[2]*256
			num = msg[3]
			packet+=1
			if(nowid!=id):
				nowid = id
				data = [0] * size
				packet = 0
			data[num*frag:num*frag+len(msg)-4] = msg[4:]
			if(packet == int(size/frag)):
				if(len(imageBuf)<2):
					imageBuf.append(numpy.array(data, dtype=numpy.uint8))
	threading.Thread(target=network).start()

#NetworkOSC
ipOSC = "127.0.0.1"
portOSC = 9000
client = udp_client.SimpleUDPClient(ipOSC, portOSC)
#Landmark:Left,Right,Down,Up:x,y
WideC = 0.2
WideS = 1.5
LRC = 0.5
LRS = 1
OpenC = 0
OpenS = 3
SmileC = 0
SmileS = 8
SmileOpen = 0.2
def networkOSC(landmarks):
	Wide = (landmarks[1][0] - landmarks[0][0] - WideC)*WideS
	LR = (landmarks[0][0] + landmarks[1][0] - LRC)*LRS
	Open = (landmarks[3][1] - landmarks[2][1] - OpenC)*OpenS
	middle = landmarks[0][1] + landmarks[1][1]
	Smile = (landmarks[3][1] + landmarks[2][1] - middle - SmileC - Open * SmileOpen)*SmileS
	client.send_message("/avatar/parameters/FaceWide", Wide)
	client.send_message("/avatar/parameters/FaceLR", LR)
	client.send_message("/avatar/parameters/FaceOpen", Open)
	client.send_message("/avatar/parameters/FaceSmile", Smile)

while True:
	#WebCam
	if(cameraDev>=0):
		ret, image = cap.read()
		image = image[0:cameraH, cropLen:cameraW-cropLen, :]
	#NetworkCam
	else:
		if(len(imageBuf)==0):
			continue
		image = imageBuf.pop()
		#yuv
		#image = cv2.cvtColor(data.reshape(120, 160, 2), cv2.COLOR_YUV2BGR_YUYV)
		#jpeg
		image = cv2.imdecode(image, cv2.IMREAD_COLOR)
		#image
		image = numpy.clip(1.5 * image -64, 0, 255).astype(numpy.uint8)
		image = cv2.rotate(image, cv2.ROTATE_90_COUNTERCLOCKWISE)
	resizedImage = cv2.resize(image,dsize=(96, 96))
	#predict
	resizedImage = resizedImage.reshape((1,96,96,3))
	landmarks = model.predict(resizedImage, verbose=0)
	landmarks = landmarks.reshape((4,2))
	#SendOSC
	threading.Thread(target=networkOSC,args=[landmarks]).start()
	#show
	for landmark in landmarks:
		print(landmark)
		pos = landmark * 240
		pos = [int(i) for i in pos]
		cv2.drawMarker(image, pos, (0, 255, 0))
	cv2.imshow("video frame", image)
	if cv2.waitKey(25) & 0xFF == ord('q'):
		break
s.close()

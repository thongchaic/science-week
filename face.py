import cv2
from datetime import date
import calendar
import time

camera = cv2.VideoCapture(0)# Camera-0


def grabVideoFeed():
	grabbed, frame = camera.read()
	return frame if grabbed else None

def capture():
	while True:
		frame = grabVideoFeed()
		if frame is None:
			raise SystemError('Video frame error')

		#frame = cv2.resize(frame, (500, 350), interpolation=cv2.INTER_CUBIC)
		# insert your code here 
		# ...
		# ..
		# . 



		cv2.imshow('CS-SRRU', frame)
		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
	camera.release()
	cv2.destroyAllWindows()



if __name__ == "__main__":
	capture()


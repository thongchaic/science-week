import cv2
from datetime import date
import calendar
import time

camera = cv2.VideoCapture(0)
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')
global imgsave
imgsave = False

global time1
global time2
time1 = calendar.timegm(time.gmtime())
time2 = calendar.timegm(time.gmtime())

def grabVideoFeed():
	grabbed, frame = camera.read()
	return frame if grabbed else None

def capture():
	while True:
		frame = grabVideoFeed()
		if frame is None:
			raise SystemError('Video frame error')
		frame = cv2.resize(frame, (500, 350), interpolation=cv2.INTER_CUBIC)		
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
                faces = face_cascade.detectMultiScale(gray, 1.3, 5)

                sx = 0
                sy = 0
                sw = 0
                sh = 0
                for (x,y,w,h) in faces:
                        if w > sw:
                                sw = w
                                sh = h
                                sx = x
                                sy = y
                if sw > 0:
                        if imgsave == True:
                                croped = frame[sy:sy+sh, sx:sx+sw]
                                cv2.imwrite('frontalface_image.png',croped)
                                cv2.imwrite('full_image.png',frame)
                                global imgsave
                                imgsave = False
                        cv2.rectangle(frame,(sx,sy),(sx+sw,sy+sh),(0,0,255),2)
                        
                time2 = calendar.timegm(time.gmtime())
                delta = time2-time1
                if delta > 2:
                        global time1
                        time1 = calendar.timegm(time.gmtime())
                        global imgsave
                        imgsave = True
                        
                cv2.putText(frame,"Face ["+str(delta)+"]", (10,320), cv2.FONT_HERSHEY_SIMPLEX, 1, (104, 244, 66), 2)
                cv2.imshow('CS-SRRU', frame)
    		
    		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		
	camera.release()
	cv2.destroyAllWindows()



if __name__ == "__main__":
	capture()


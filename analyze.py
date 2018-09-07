import cv2

camera = cv2.VideoCapture(0)

def grabVideoFeed():
	grabbed, frame = camera.read()
	return frame if grabbed else None
def capture():
	while True:
		frame = grabVideoFeed()
		if frame is None:
			raise SystemError('Video frame error')
		
		frame = cv2.resize(frame, (500, 350), interpolation=cv2.INTER_CUBIC)
                canny = cv2.Canny(frame,100,200)
		gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
		corner = cv2.cornerHarris(gray,2,3,0.04)
                corner = cv2.dilate(corner,None)
                frame[corner>0.01*corner.max()]=[0,0,255]
                canny_rgb = cv2.cvtColor(canny, cv2.COLOR_GRAY2BGR)
                frame = frame & canny_rgb
                            		
                cv2.putText(frame,"Analyse", (10,320), cv2.FONT_HERSHEY_SIMPLEX, 1, (104, 244, 66), 2)
    		cv2.imshow('CS-SRRU', frame)
    		
    		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		

	camera.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	capture()



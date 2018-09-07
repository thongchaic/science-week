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
		bhist = cv2.calcHist([frame], [0], None, [256], [0,256])
		ghist = cv2.calcHist([frame], [1], None, [256], [0,256])
		rhist = cv2.calcHist([frame], [2], None, [256], [0,256])
		BMAX = max(bhist)
		GMAX = max(ghist)
		RMAX = max(rhist)
		for i in range(255):
                        bx1 = 4*i
                        bx2 = 4*(i+1)
                        by1 = bhist[i]*512/BMAX
                        by2 = bhist[i+1]*512/BMAX

                        gx1 = 4*i
                        gx2 = 4*(i+1)
                        gy1 = ghist[i]*512/GMAX
                        gy2 = ghist[i+1]*512/GMAX

                        rx1 = 4*i
                        rx2 = 4*(i+1)
                        ry1 = rhist[i]*512/RMAX
                        ry2 = rhist[i+1]*512/RMAX

                        cv2.line(frame, (bx1,by1), (bx2,by2), ( 255, 0, 0 ), 2)
                        cv2.line(frame, (gx1,gy1), (gx2,gy2), ( 0, 255, 0 ), 2)
                        cv2.line(frame, (rx1,ry1), (rx2,ry2), ( 0, 0, 255), 2)
    		
                cv2.putText(frame,"Original (RGB)", (10,320), cv2.FONT_HERSHEY_SIMPLEX, 1, (104, 244, 66), 2)
    		cv2.imshow('CS-SRRU', frame)
    		
    		if cv2.waitKey(1) & 0xFF == ord('q'):
			break
		

	camera.release()
	cv2.destroyAllWindows()

if __name__ == "__main__":
	capture()


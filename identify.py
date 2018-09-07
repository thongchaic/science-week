import cv2
from numpy import genfromtxt
import face_recognition
import time
import numpy as np
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')

camera = 0#cv2.VideoCapture(0)
known_faces = []
known_names = []
known_images = []
frame = np.zeros([400, 500, 3],dtype=np.uint8)

def grabVideoFeed():
	grabbed, frame = camera.read()
	return frame if grabbed else None

def start_identify():
	while True:
		identify_faces()
    		time.sleep(1)
                if cv2.waitKey(1) & 0xFF == ord('q'):
                        break
	cv2.destroyAllWindows()
	
def identify_faces():
        try:
                print("Identifying faces....")
                frame.fill(255)
                frontalface_image = cv2.imread("frontalface_image.png")
                input_image=face_recognition.face_encodings(frontalface_image)[0]
                matches=face_recognition.compare_faces(known_faces,input_image)
                print(matches)
                #for face in matches:
                #       print(face)
                distances=face_recognition.face_distance(known_faces,input_image)
                distances = 100 - (distances * 100)
                print(distances)
                owner = cv2.resize(frontalface_image, (150, 100))
                frame[0:100,0:150,:] = owner
                cv2.putText(frame,"You.....", (160,65), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                
                max_dist = distances[0]
                max_idx = -1
                max_img = 'tc.png'
                max_name = 'Unknown'
                nn = 100
                for i in range(3):
                        #print(distances)
                        max_dist = distances[0]
                        for j, x in enumerate(distances):
                                if x > max_dist:
                                        max_dist = x
                                        max_img = known_images[j]
                                        max_name = known_names[j]
                                        max_idx = j
                                #print(j,x)
                        
                        print(max_dist,max_name,max_img)
                        distances[max_idx] = -1
                        s1 = cv2.imread(max_img)
                        s1 = cv2.resize(s1, (150, 100))
                        frame[nn:nn+100,0:150,:] = s1
                        max_dist=np.round(max_dist)
                        cv2.putText(frame,max_name+" : "+str(max_dist)+"%", (160,nn+60), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 0), 2)
                        nn = nn+100
                        print(nn)

                cv2.imshow('CS-SRRU', frame)
        except:
                print("face not found....")
    	
def load_known_faces():
        lines = open("label.txt","r")
        for line in lines:
                field = line.split(",")
                print(field[0],"=>",field[1].rstrip('\n'))
                image_path = "data/"+field[1].rstrip('\n')
                image = cv2.imread(image_path)
                #print("loading .. .", field[0],"=>", field[1].rstrip('\n'))
                #print(image)
                
                gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
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
                        crop_img = image[sy:sy+sh, sx:sx+sw]
                        cv2.imwrite("test.jpg",crop_img)
                        encoded = face_recognition.face_encodings(crop_img)[0]
 #                       print(encoded.shape)
                        
                        known_faces.append(encoded)
                        known_names.append(field[0])
                        known_images.append(image_path)
                        
        print("Known faces => ",len(known_faces))

           
if __name__ == "__main__":
        load_known_faces()
        start_identify()
#        identify_faces()
#       test()
#       capture()


import face_recognition
import cv2
import requests
import wget
import os
import numpy as np

URL="https://smart.srru.ac.th/api/ping"
face_cascade = cv2.CascadeClassifier('haarcascade_frontalface_default.xml')


def download_img(img_url):
	if img_url is not None:
		wget.download(img_url)
		print("\ndownload .... ok")
		file_name=img_url.rpartition('/')
		print("finisned......",file_name)
		return file_name[2]
	else:
		return None

def fetch_mis_faces():
	response = requests.get(URL)
	jsfaces = response.json()
	for i in range(len(jsfaces)):
		#print(i,", ",len(faces[i]))
		#print(faces[i]['id'])

		face_url = jsfaces[i]['img']
		face_id = jsfaces[i]['id']
		file_name=download_img(face_url)

		if file_name is not None:
			try:

				image = cv2.imread(file_name)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
				faces = face_cascade.detectMultiScale(gray, 1.3, 5)
				for (x,y,w,h) in faces:
					crop_img = image[y:y+h, x:x+w]
					face_encoded=face_recognition.face_encodings(crop_img)[0]
					face_array = np.array(face_encoded)
					str_face = np.array2string(face_array)
					put_url = 'https://smart.srru.ac.th/api/ping/'+str(face_id)
					print(put_url)
					r_put_face = requests.put(put_url, data = {'t':'update_identity','img_identity':str_face})
					print(r_put_face," ",file_name," .. OK!!")

				os.remove(file_name)
			except:
				print("Err:", file_name, " cannot be further proceess!!")
		else:
			print(file_name," not found!!")

def cvtColorTest():
		response = requests.get(URL)
	jsfaces = response.json()
	for i in range(len(jsfaces)):
		#print(i,", ",len(faces[i]))
		#print(faces[i]['id'])
		face_url = jsfaces[i]['img']
		face_id = jsfaces[i]['id']
		file_name=download_img(face_url)

		if file_name is not None:
			try:
				image = cv2.imread(file_name)
				gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
			except:
				print("Err:", file_name, " cannot be further proceess!!")
		else:
			print(file_name," not found!!")
def test():
	img_url = "https://mis.srru.ac.th/uploads/images/profile/b31aeee0a6cfa8f539f8dc1ff7f1c0cc1997d5c5.jpg";
	file_name=download_img(img_url)

	if file_name is not None:
		print(file_name)
		image = cv2.imread(file_name)
		gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
		faces = face_cascade.detectMultiScale(gray, 1.3, 5)

		for (x,y,w,h) in faces:
			#f=cv2.rectangle(image,(x,y),(x+w,y+h),(255,0,0),2)
			crop_img = image[y:y+h, x:x+w]
			i=face_recognition.face_encodings(crop_img)[0]
			a = np.array(i)
			st = np.array2string(a)
			#ping/{id}?t=update_identity&img_identity=.......
			r = requests.put('https://smart.srru.ac.th/api/ping/4', data = {'t':'update_identity','img_identity':st})
			print(r)

			# j=face_recognition.face_encodings(crop_img)[0]
			
			# a = np.array(i)
			# b = np.array(j)
			# print(a.shape)
			# print(b.shape)
			# st = np.array2string(a)


			# print(st)
			

			# z = np.fromstring(st)
			# know =[z]
			# print(z.shape)
			# print(b.shape)

			#matches=face_recognition.compare_faces(know,b)
			#print(matches)
			#print(e)
			#print(b)

			#st = np.array2string(a)
			#print(st)


			#b = np.fromstring(st)#DB

			#ff=face_recognition.compare_faces(b,e)
			#print(ff)
			#e=face_recognition.face_encodings(crop_img)

			#print(a.shape)
			#print("---")
			#print(e)

			#cv2.imwrite('id-'+file_name,crop_img)

			#os.remove(file_name)
			#roi_gray = gray[y:y+h, x:x+w]


		#raw_face = face_recognition.load_image_file(file_name)#opencv 
		#print(raw_face.shape)
		#os.remove(file_name)
		#fae_id = face_recognition.face_encodings(raw_face)[0]
		#print(fae_id)
		#os.remove(file_name)
	else:
		print(file_name," not found!!")

	#face_id = face_recognition.load_image_file("https://mis.srru.ac.th/uploads/images/profile/b31aeee0a6cfa8f539f8dc1ff7f1c0cc1997d5c5.jpg")
	#face_encoded = face_recognition.face_encodings(face_id)[0]
	#print("xxxx------>")
	#print(file_name[2])

if __name__ == '__main__':
	fetch_mis_faces()
	#test()
	#testrecog()
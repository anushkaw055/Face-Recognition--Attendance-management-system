# If the number of students are more or if you wish to store the encoded values to reduce run time,
# you can append this to the main code 

import pickle
PIK = "pickle.dat"

#For storing the encoded values:
for i in range(0, no_of_stds):
	image.append(face_recognition.load_image_file("database/image"+str(i)+".jpg"))
	encoding.append(face_recognition.face_encodings(image[i])[0])
	with open(PIK, "wb") as f:
		pickle.dump(len(encoding), f)
		for value in encoding:
			pickle.dump(value, f)

#For reading the encoded values:
with open(PIK, "rb") as f:
    for _ in range(pickle.load(f)):
        encoding.append(pickle.load(f))


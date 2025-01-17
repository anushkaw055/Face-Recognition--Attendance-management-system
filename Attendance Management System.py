# Face Recognition based Attendance Management System built using Python and deep learning.
# A Web camera/ USB camera is needed in this example.
    
#     AUTHOR  : Nevil Pooniwala
#     EMAIL   : nevilpooniwala1997@gmail.com

import face_recognition
import cv2
import xlwt
import os
import time
import numpy as np
from Tkinter import *


root_main=Tk()
root_main.configure(background="#80D8FF")

DATA = []
for i in range(0,100):
	DATA.append([])

DATA = [["ROLL NO.", "NAME", "ATTENDANCE"],
	["01", "Ruchi Shah" , "Absent"],
	["02", "Akash Upadhayay" , "Absent"],
	["03", "Anushka Waingankar" , "Absent"],
	["04", "Nevil Pooniwala" , "Absent"],
	["05", "Viraj Parikh" , "Absent"],[]] # Add student details

no_of_stds = 5 #Can use something like instead of this len(DATA)

image = []
encoding = []
face_locations = []
face_encodings = []
face_names = []
frame_number = 0


def function1(): 	#Function to update database
	root_1=Tk()
	root_1.title("ENTER DETAILS")
	root_1.configure(bg="#795548")
	camera = cv2.VideoCapture(1)

	def enter_the_value():
    		global no_of_stds, DATA
    		usn = int(e2_1.get())
    		std_name = e1_1.get()
    		print("Taking image...")
    		_, camera_capture = camera.read()
		time.sleep(0.2)
    		cv2.imwrite("database/image" + str(usn-1) +".jpeg", camera_capture) #check face
    		time.sleep(0.3)
    		no_of_stds = no_of_stds + 1
		DATA[usn].append(str(usn))
		DATA[usn].append(str(std_name))
		DATA[usn].append("Absent")
    		print "image captured, resized and renamed successfully"
    		#img = cv2.imread("/database/image"+str(usn)+".png")
    		#cv2.imshow('user_image',img)
    		camera.release()
    		cv2.destroyAllWindows()

	Label(root_1,text="ENTER STUDENT DETAILS", font=("helvatica",40),bg="#F44336", fg="#0a0800").grid(rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

	Label(root_1, text="Enter Student name: ",fg="#42A5F5",bg="#795548",font=("chiller",16)).grid(row=3,padx=5,pady=5,sticky=E)
	Label(root_1, text="Enter Roll No.: ",fg="#42A5F5",bg="#795548",font=("chiller",16)).grid(row=5,padx=5,pady=5,sticky=E)
	Label(root_1,text="(ENTER DETAILS AND PRESS 'c' TO CAPTURE IMAGE)", fg="#42A5F5",bg="#795548",font=("chiller",10)).grid(rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

	e1_1=Entry(root_1)
	e1_1.grid(row=3,rowspan=2,column=1)
	e2_1=Entry(root_1)
	e2_1.grid(row=5,rowspan=2,column=1)

	Button(root_1,text="CLEAR",bg="#00695C",font=("times new roman",25), command=root_1.quit).grid(row=8,columnspan=2,stick=E+W+N+S, pady=4)
	Button(root_1,text="SUBMIT",bg="#00695C",font=("times new roman",25), command=enter_the_value).grid(row=9,columnspan=2,stick=W+E+N+S, pady=4)

	root_1.mainloop()


    
def start_attendance(): 	#Function to mark attendance in the list
	video_capture = cv2.VideoCapture(1)
	global no_of_stds, frame_number
	while True:
	    # Grab a single frame of video
	    ret, frame = video_capture.read()
	    frame_number += 1
	    # Find all the faces and face enqcodings in the frame of video
	    face_locations = face_recognition.face_locations(frame)
	    face_encodings = face_recognition.face_encodings(frame, face_locations)
	    face_names = []

	    for face_encoding in face_encodings:
		# See if the face is a match for the known face(s)
		match = face_recognition.compare_faces(encoding, face_encoding, tolerance=0.50)

		name = "Unknown"
		for i in range(0, no_of_stds):
	       		if match[i]:
		   		name = DATA[i+1][1]+ "_" + str(i)
				DATA[i+1][2] = "present"
		face_names.append(name)

	    # Label the results
	    for (top, right, bottom, left), name in zip(face_locations, face_names):
		if not name:
		    continue

		# Draw a box around the face
		cv2.rectangle(frame, (left, top), (right, bottom), (0, 0, 255), 2)

		# Draw a label with a name below the face
		cv2.rectangle(frame, (left, bottom - 25), (right, bottom), (0, 0, 255), cv2.FILLED)
		font = cv2.FONT_HERSHEY_DUPLEX
		cv2.putText(frame, name, (left + 6, bottom - 6), font, 0.5, (255, 255, 255), 1)


	    # Display the resulting image
	    cv2.imshow('Video', frame)

	    # Hit 'q' on the keyboard to quit!
	    if cv2.waitKey(1) & 0xFF == ord('q'):
		break
	# Release handle to the webcam
	video_capture.release()
	cv2.destroyAllWindows()



def function2(): 	#Function to mark attendance in the spreadsheet
	root_2=Tk()
	root_2.title("ENTER DETAILS")
	root_2.configure(bg="#795548")
	for i in range(0, no_of_stds):
		image.append(face_recognition.load_image_file("database/image"+str(i)+".jpeg"))
		encoding.append(face_recognition.face_encodings(image[i])[0])
	
	def save_attendance():
		wb = xlwt.Workbook()
		ws = wb.add_sheet("My Sheet")
		for i, row in enumerate(DATA):
		    for j, col in enumerate(row):
			ws.write(i, j, col)
		wb.save(e2_2.get()+"_"+e1_2.get()+".xls")

	Label(root_2,text="ENTER SUBJECT DETAILS", font=("helvatica",40),bg="#F44336", fg="#0a0800").grid(rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

	Label(root_2, text="Enter date and time: ",fg="#42A5F5",bg="#795548",font=("chiller",16)).grid(row=3,padx=5,pady=5,sticky=E)
	Label(root_2, text="Enter subject: ",fg="#42A5F5",bg="#795548",font=("chiller",16)).grid(row=5,padx=5,pady=5,sticky=E)
	Label(root_2,text="(PRESS 'q' ONCE ATTENDANCE IS TAKEN)", fg="#42A5F5",bg="#795548",font=("chiller",10)).grid(rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)
	e1_2=Entry(root_2)
	e1_2.grid(row=3,rowspan=2,column=1)
	e2_2=Entry(root_2)
	e2_2.grid(row=5,rowspan=2,column=1)

	Button(root_2,text="CLEAR",bg="#00695C",font=("times new roman",25), command=root_2.quit).grid(row=8,columnspan=2,stick=E+W+N+S, pady=4)
	Button(root_2,text="START ATTENDANCE",bg="#00695C",font=("times new roman",25), command=start_attendance).grid(row=9,columnspan=2,stick=W+E+N+S, pady=4)
	Button(root_2,text="SUBMIT",bg="#00695C",font=("times new roman",25), command=save_attendance).grid(row=10,columnspan=2,stick=W+E+N+S, pady=4)

	root_2.mainloop()


root_main.title("FACE RECOGNITION ATTENDANCE MANAGEMENT SYSTEM")

Label(root_main, text="SELECT YOUR OPTION",font=("helvatica",40),fg="white",bg="#00BFA5",height=2).grid(row=0,rowspan=2,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

Button(root_main,text="UPDATE DATABASE",font=("times new roman",30),bg="#3F51B5",fg='white',command=function1).grid(row=3,columnspan=2,sticky=W+E+N+S,padx=5,pady=5)

Button(root_main,text="MARK ATTENDANCE",font=("times new roman",30),bg="#3F51B5",fg='white',command=function2).grid(row=4,columnspan=2,sticky=N+E+W+S,padx=5,pady=5)

root_main.mainloop()

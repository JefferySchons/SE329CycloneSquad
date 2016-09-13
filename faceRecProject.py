from Tkinter import *
import cv2, os
import numpy as np
from PIL import Image
import tkMessageBox

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)

# For face recognition we will the the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer()

#This will be triggered on the Recognize button click
def Recognize(event):
    path = './yalefaces'
    # Call the get_images_and_labels function and get the face images and the
    # corresponding labels
    images, labels = get_images_and_labels(path)
    cv2.destroyAllWindows()

    # Perform the tranining
    recognizer.train(images, np.array(labels))

    # Attempt to recognize the given image.
    #image_path = txtBox.text
    image_path = "./yalefaces/subject01.sad"
    new_image = Image.open(image_path).convert('L')
    predict_image = np.array(new_image, 'uint8')
    faces = faceCascade.detectMultiScale(predict_image)
    for (x, y, w, h) in faces:
        label_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
        name_actual = os.path.split(image_path)[1].split(".")[0]
        if name_actual == label_predicted:
            tkMessageBox.showinfo("Success", "{} is correctly recognized with confidence {}.".format(name_actual, conf))
        else:
            tkMessageBox.showinfo("Failure", "Subject with label {} was not found.".format(label_predicted))

#Get the images to train the recognizer
def get_images_and_labels(path):
    # Append all the absolute image paths in a list image_paths
    # We will not read the image with the .sad extension in the training set
    # Rather, we will use them to test our accuracy of the training
    image_paths = [os.path.join(path, f) for f in os.listdir(path) ] #if not f.endswith('.sad')]
    # images will contains face images
    images = []
    # labels will contains the label that is assigned to the image
    labels = []
    for image_path in image_paths:
        # Read the image and convert to grayscale
        image_pil = Image.open(image_path).convert('L')
        # Convert the image format into numpy array
        image = np.array(image_pil, 'uint8')
        # Get the label of the image
        nbr = int(os.path.split(image_path)[1].split(".")[0].replace("subject", ""))
        # Detect the face in the image
        faces = faceCascade.detectMultiScale(image)
        # If face is detected, append the face to images and the label to labels
        for (x, y, w, h) in faces:
            images.append(image[y: y + h, x: x + w])
            labels.append(nbr)
            #cv2.imshow("Adding faces to traning set...", image[y: y + h, x: x + w])
            cv2.waitKey(50)
    # return the images list and labels list
    return images, labels

def Save(event):
    print "TODO"

root = Tk()
input = Entry()
button1 = Button(text="Recognize")
button1.bind('<Button-1>', Recognize)

label = Label(text="Name")
image = Label()
text = Text()
button2 = Button(text="Save")
button2.bind('<Button-1>', Save)

input.pack()
button1.pack()
label.pack()
image.pack()
text.pack()
button2.pack()

root.mainloop()

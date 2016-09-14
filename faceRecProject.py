from Tkinter import *
import tkFileDialog
import cv2, os
import numpy as np
import PIL.Image
import tkMessageBox
from DialogBox import *
from CSVIndex import *

# For face detection we will use the Haar Cascade provided by OpenCV.
cascadePath = "haarcascade_frontalface_default.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
# For face recognition we will the the LBPH Face Recognizer
recognizer = cv2.createLBPHFaceRecognizer()
myIndex = CSVIndex()

class FaceRecApp(Tk):
    def __init__(self):
        Tk.__init__(self)
        self.input = Entry()
        self.button1 = Button(text="Recognize")
        self.button1.bind('<Button-1>', self.Recognize)

        self.label = Label(text="Name")
        self.image = Label()
        self.text = Text()
        self.button2 = Button(text="Save New Image")
        self.button2.bind('<Button-1>', self.saveButtonPressed)

        self.input.pack()
        self.button1.pack()
        self.label.pack()
        self.image.pack()
        self.text.pack()
        self.button2.pack()

        #self.nameEntered = text.get('0.0', END)


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
            image_pil = PIL.Image.open(image_path).convert('L')
            # Convert the image format into numpy array
            image = np.array(image_pil, 'uint8')
            # Get the label of the image
            nbr = int(os.path.split(image_path)[1].split(".")[0])
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

    path = './yalefaces'
    # Call the get_images_and_labels function and get the face images and the
    # corresponding labels

    # Perform the tranining
    print "Training the recognizer..."
    images, labels = get_images_and_labels(path)
    cv2.destroyAllWindows()

    recognizer.train(images, np.array(labels))

    #This will be triggered on the Recognize button click
    def Recognize(self, event):

        # Attempt to recognize the given image.
        #image_path = txtBox.text
        image_name = self.input.get() #text.get('0.0', END)
        #image_file = tkFileDialog.askopenfilename(initialdir='C:/')
        image_path = "./new faces/" + image_name
        tkMessageBox.showinfo("image_path", image_path)
        #image_path = os.path.split(image_file)[0]
        new_image = PIL.Image.open(image_path).convert('L')
        predict_image = np.array(new_image, 'uint8')
        faces = faceCascade.detectMultiScale(predict_image)
        print "CP 1"
        for (x, y, w, h) in faces:
            label_predicted, conf = recognizer.predict(predict_image[y: y + h, x: x + w])
            #label_actual = int(os.path.split(image_path)[1].split(".")[0])
            if conf < 100:
                name_actual = myIndex.getNameFromID(label_predicted)
                tkMessageBox.showinfo("Success", "{} is correctly recognized with confidence {}.".format(name_actual, conf))
            else:
                tkMessageBox.showinfo("Failure", "Subject was not recognized with enough confidence.  Please save the image with the correct name.")


    def saveButtonPressed(self, event):
       inputDialog = DialogBox(root, "Enter Name", "Submit")
       root.wait_window(inputDialog.top)
       givenName = inputDialog.value
       curLabel = myIndex.getIDFromName(givenName)
       if curLabel == -1:
            curLabel = myIndex.addName(givenName)
       imageNumber = countLabelImages(curLabel)
       cv2.imwrite(path + "/" + curLabel + "." + imageNumber)

    def countLabelImages(self, label):
        imgCount = 0
        for row in myIndex.index:
            if row['id'] == label:
                imgCount += 1

        return imgCount

root = FaceRecApp()
root.mainloop()

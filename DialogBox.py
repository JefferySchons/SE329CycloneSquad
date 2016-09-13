# creates a dialog box
# init with obj = DialogBox(tkRoot, "Label Text", "Submit Button Text"
# then wait for its completion with root.wait_window(obj.top)
# returns it's value to obj.value
from Tkinter import *

class DialogBox:
    def __init__(self, parent, labelText, submitText):
        top = self.top = Toplevel(parent)
        self.myLabel = Label(top, text=labelText)
        self.myLabel.pack()

        self.myEntryBox = Entry(top)
        self.myEntryBox.pack()

        self.mySubmitButton = Button(top, text=submitText, command=self.send)
        self.mySubmitButton.pack()

    def send(self):
        self.value = self.myEntryBox.get()
        self.top.destroy()

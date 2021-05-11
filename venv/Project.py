from tkinter import *
from PIL import Image, ImageTk
import flask
import requests
import response
import json

def submit_img():
    print("Do a thing!")
    user_url = url.get()
    api_address = "http://flip2.engr.oregonstate.edu:6224/?url="
    api_address+= user_url
    r = requests.get(api_address)
    result = r.content
    temp = str(result, "UTF-8")
    print(temp)
    final = json.loads(temp)

    #display photo
    image = Image.open("./images/pic.jpg")
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)

    label.image = photo
    label.grid(row=5, sticky=W)

    #display data
    row_count = 4
    i = 1
    temp_data = ""

    for item in final.items():
        temp_data = str(temp_data) + str(item[0]) + " : " + str(item[1]) +"\n"
    temp_label = Label(root, text=temp_data, anchor=W, justify=LEFT)
    temp_label.grid(row=i+row_count, column= 1, sticky=W)
        #i+=1

def reset_app():
    print("Reset it!")

root = Tk()
root.title("MetaData Viewer")
root.geometry("1250x625")


title = Label(root, text="Photo Metadata", font="Arial 40 bold")
title.grid(row=0, sticky=W)

info1 = Label(root, text="Does your photo have metadata attached sharing information you'd like to keep private?")
info1.grid(row=1, sticky=W)

info2 = Label(root, text="Submit the url address of a photo below to see what information is attached.")
info2.grid(row=3, sticky=W)

input_frame = Frame(root)

url_label = Label(input_frame, text="Enter URL Address:")
url_label.pack(side=LEFT)

url = StringVar()
input = Entry(input_frame, textvariable = url, width=40)
input.pack(side=LEFT, padx=2)

submit_button = Button(input_frame, text="Submit", command=submit_img)
submit_button.pack(side=LEFT, padx=2)

reset_button = Button(input_frame, text="Reset", command=reset_app)
reset_button.pack(side=LEFT)

input_frame.grid(row=4, sticky=W)

root.mainloop()
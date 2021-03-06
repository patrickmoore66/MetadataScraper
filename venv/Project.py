#361 Patrick Moore
from tkinter import *
from tkinter import messagebox
from PIL import Image, ImageTk
from functools import partial
import flask
import urllib
import requests
import response
import json
import os
import sys

def display_advanced(final, gps_text, root):
    temp_data = gps_text

    for item in final.items():
        if item[0] != 'XResolution' and item[0] != 'YResolution':
            print(type(item[1]))

            temp_data = str(temp_data) + str(item[0]) + " : " + str(item[1]) + "\n"
    print(temp_data)
    try:
        if final['Metadata'] == 'None':
            temp_label = Label(root, text=temp_data, anchor=W, justify=LEFT)
            temp_label.grid(row=6, column=1, sticky=W)
    except:
        temp_label = Label(root, text=temp_data, anchor=W, justify=LEFT)
        temp_label.grid(row=6, column=1, sticky=W)
        # i+=1

    return

def submit_img(url, root, input_frame):
    user_url = url.get()
    api_address = "http://flip2.engr.oregonstate.edu:6224/?url="
    api_address+= user_url
    r = requests.get(api_address)
    result = r.content
    temp = str(result, "UTF-8")
    print(temp)
    final = json.loads(temp)

    #display photo

    #call photo border service
    payload = {'imageUrl':user_url}
    API_ENDPOINT = 'http://flip2.engr.oregonstate.edu:13700/addBorder'
    r = requests.post(url=API_ENDPOINT, data=payload)
    border_url = r.text

    urllib.request.urlretrieve(border_url, "border.jpg")
    image = Image.open("border.jpg")
    photo = ImageTk.PhotoImage(image)
    label = Label(root, image=photo)

    label.image = photo
    label.grid(row=6, sticky=W)

    #display data
    row_count = 5
    i = 2

    #display GPS data first
    if final.get('GPSInfo', False) != False:
        gps_data = final.pop('GPSInfo')
        gps_text = "GPSInfo: " + str(gps_data) + "\n"
        gps_label = Label(root, text=gps_data, anchor=W, justify=LEFT)
        gps_label.grid(row=6, column=1, sticky=W)

    else:
        gps_data = "GPSInfo: None" + "\n"
        gps_text = gps_data
        gps_label = Label(root, text=gps_data, anchor=W, justify=LEFT)
        gps_label.grid(row=6, column=1, sticky=W)

    #display advanced info button
    advanced_button = Button(input_frame, text="Display Advanced Info", bg='red', command=partial(display_advanced, final, gps_text, root))
    advanced_button.pack(side=LEFT, padx=2)


def reset_app(self):
    print("Reset it!")
    if messagebox.askokcancel(title="Reset App", message="Clicking OK will reset the app, losing all data. Are you sure you'd like to reset?"):
        self.destroy()
        start()
    return

def start():
    # Main Loop
    root = Tk()
    root.title("MetaData Viewer")
    root.geometry("1250x650")

    title = Label(root, text="Photo Metadata", font="Arial 40 bold")
    title.grid(row=0, sticky=W)

    # Intro Text
    info1 = Label(root, text="Does your photo have metadata attached sharing information you'd like to keep private?")
    info1.grid(row=1, sticky=W)
    info2 = Label(root, text="Submit the url address of a photo below to see what information is attached.")
    info2.grid(row=3, sticky=W)
    info3 = Label(root, text="This process is quick and easy, and should take less than 10 seconds to load.")
    info3.grid(row=4, sticky=W)

    # Input field
    input_frame = Frame(root)
    url_label = Label(input_frame, text="Enter URL Address:")
    url_label.pack(side=LEFT)
    url = StringVar()
    input = Entry(input_frame, textvariable=url, width=40)
    input.pack(side=LEFT, padx=2)

    # Submit Button
    submit_button = Button(input_frame, text="Submit", command=partial(submit_img, url, root, input_frame))
    submit_button.pack(side=LEFT, padx=2)

    # Reset Button
    reset_button = Button(input_frame, text="Reset", command=partial(reset_app, root))
    reset_button.pack(side=LEFT)

    input_frame.grid(row=5, sticky=W)

    root.mainloop()

if __name__ == "__main__":
    start()
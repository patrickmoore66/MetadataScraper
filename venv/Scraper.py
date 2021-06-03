from flask import Flask, make_response, jsonify, request
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests
import jsonpickle
import urllib.request

#configuration

app=Flask(__name__)

app.config['SEND_FILE_MAX_AGE_DEFAULT'] = 0


def label_data(labeled, exifdata):
    for (key,val) in exifdata.items():
        labeled[TAGS.get(key)] = val

    #unpack GPS info using get_gps function
    gps = get_gps()
    if labeled.get('GPSInfo', False) != False:
        latitude = "Latitude: " + str(gps['GPSLatitude'])
        longitutde = "Longitude: "+ str(gps['GPSLongitude'])
        labeled['GPSInfo'] = latitude + " , " + longitutde
    return

def get_gps():
    gps_info = {}
    gps_image = Image.open('temp.jpg')
    gps_exif = gps_image._getexif()

    gps_labeled = {}
    for (key,val) in gps_exif.items():
        gps_labeled[TAGS.get(key)] = val

    gps_final = {}
    if gps_labeled.get('GPSInfo', False) != False:
        for key in gps_labeled['GPSInfo'].keys():
            decode = GPSTAGS.get(key,key)
            gps_final[decode] = gps_labeled['GPSInfo'][key]


    return gps_final

#Routes

@app.route("/", methods = ['GET'])
def root():
    result = {}

    #get image url from request
    headers = {"Content-Type": "application/json"}
    image_url = request.args.get('url')
    print("IMAGE URL")
    print(image_url)

    #check if image_url was successfully received
    if image_url == None:
        print("Bad Url")
        return make_response('Invalid URL', 400)

    #open image and create file using write()
    try:
        urllib.request.urlretrieve(image_url, 'temp.jpg')
    except:
        return make_response('Unable to open jpg at url given, please check the provided url is correct', 400)

    # read image data using PIL
    image = Image.open('temp.jpg')
    exifdata = image.getexif()
    print('EXIF DATA')
    print(exifdata)

    #Label image data
    labeled = {}
    if exifdata == {}:
        response = {'Metadata': 'None'}
        return jsonpickle.encode(response)

    label_data(labeled, exifdata)

    return jsonpickle.encode(labeled)

#routes
@app.route('/', methods = ['POST', 'HEAD', 'PUT', 'DELETE'])
def base():
    return jsonpickle.encode({'Please use a GET request to provide the url of a jpg'})

@app.errorhandler(400)
def bad_request(error):
    return "Bad request", 400

@app.errorhandler(500)
def server_error(error):
    return "Something went wrong on our end, sorry!", 500

#listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6224))
    app.run(port=port, debug=True)
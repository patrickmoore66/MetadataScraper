from flask import Flask, make_response, jsonify, request
import os
from PIL import Image
from PIL.ExifTags import TAGS, GPSTAGS
import requests
import jsonpickle

#configuration

app=Flask(__name__)

def get_gps():
    gps_info = {}
    gps_image = Image.open('temp.jpg')
    gps_exif = gps_image._getexif()

    gps_labeled = {}
    for (key,val) in gps_exif.items():
        gps_labeled[TAGS.get(key)] = val

    gps_final = {}
    for key in gps_labeled['GPSInfo'].keys():
        decode = GPSTAGS.get(key,key)
        gps_final[decode] = gps_labeled['GPSInfo'][key]


    return gps_final

#Routes

@app.route("/", methods = ['GET'])
def root():
    #get image url from request
    if request.method != 'GET':
        return make_response('Incorrect query', 400)
    headers = {"Content-Type": "application/json"}
    image_url = request.args.get('url')
    temp = requests.get(image_url, allow_redirects=True)
    f = open('temp.jpg', 'wb').write(temp.content)
    print(f)

    #read image data using PIL
    image = Image.open('temp.jpg')
    exifdata = image.getexif()
    print('EXIF DATA')
    print(exifdata)

    labeled = {}
    for (key,val) in exifdata.items():
        labeled[TAGS.get(key)] = val

    #unpack GPS info
    gps = get_gps()
    labeled['GPSInfo'] ="Latitude: " + str(gps['GPSLatitude']) + " , " + "Longitude: "+ str(gps['GPSLongitude'])

    print("Result")
    print(labeled)

    return jsonpickle.encode(labeled)

#listener

if __name__ == "__main__":
    port = int(os.environ.get('PORT', 6224))
    app.run(port=port, debug=True)
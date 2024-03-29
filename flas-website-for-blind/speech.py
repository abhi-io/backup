from flask import Flask,Response
from flask import send_file,send_from_directory
from gtts import gTTS
import subprocess
import numpy as np
import argparse
import time,random
import cv2
import os
items_found=[]
UPLOAD_FOLDER = '/home/abc/abhi/flask'

app = Flask(__name__)
app.secret_key = "secret key"
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
import os,sys
#import magic
import urllib.request
# from app import app
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename

ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'gif'])
# ALLOWED_EXTENSIONS = set(['txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'])
###########################################################################
###########################################################################
###########################################################################
###########################################################################
def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/download_img')
def downloadFile ():
    #For windows you need to use drive name [ex: F:/Example.pdf]
    path = png_path+".png"
    return send_file(path, as_attachment=True)


@app.route('/')
def upload_form():
    os.system("rm *.jpg")

    # return songname.play()
    flash(items_found)
    # items_found.clear()
    # global items_found
    return render_template('liveReport.html')

@app.route('/s')
def streamwav():
    def generate():
        print("---------audio section !!!!!!!!")
        with open("m.mp3", "rb") as fwav:
            data = fwav.read(1024)
            while data:
                yield data
                data = fwav.read(1024)
    return Response(generate(), mimetype="audio/x-wav")

@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part << python server')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            print(file.filename)

            flash('No file selected for uploading << python server')
            return redirect(request.url)

        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            flash('File successfully uploaded  /// img processing /// << python server ')
            # os.system("x.py")
            print("---------",filename)
            items_found=[]

            # from PIL import Image
            import glob
            have_img=0
            while(have_img!=1):
                a=glob.glob("*.jpg")
                if(a==''):
                    have_img=0
                    print("---------]>>  we have NO img")
                else:
                    print(a[0],">> we have img---------")
                    have_img=1
                    img_name=a[0]


            #python yolo.py --image images/living_room.jpg --yolo yolo-coco
            #python3 speech.py --image q.jpg --yolo yoloNN/



            aa=1

            # construct the argument parse and parse the arguments
            ap = argparse.ArgumentParser()
            # ap.add_argument("-i", "--image", required=True,help="path to input image")
            # ap.add_argument("-y", "--yolo", required=True,help="base path to YOLO directory")
            ap.add_argument("-c", "--confidence", type=float, default=0.5,help="minimum probability to filter weak detections")
            ap.add_argument("-t", "--threshold", type=float, default=0.3,help="threshold when applying non-maxima suppression")
            args = vars(ap.parse_args())
            # load the COCO class labels our YOLO model was trained on
            labelsPath = "yoloNN/coco.names"
            # labelsPath = os.path.sep.join([args["yolo"], "coco.names"])
            LABELS = open(labelsPath).read().strip().split("\n")

            # initialize a list of colors to represent each possible class label
            np.random.seed(42)
            COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
            # load the COCO class labels our YOLO model was trained on
            labelsPath = "yoloNN/coco.names"
            # labelsPath = os.path.sep.join([args["yolo"], "coco.names"])

            LABELS = open(labelsPath).read().strip().split("\n")

            # initialize a list of colors to represent each possible class label
            np.random.seed(42)
            COLORS = np.random.randint(0, 255, size=(len(LABELS), 3),dtype="uint8")
            # derive the paths to the YOLO weights and model configuration
            weightsPath = "yoloNN/yolov3.weights"
            configPath = "yoloNN/yolov3.cfg"
            # weightsPath = os.path.sep.join([args["yolo"], "yolov3.weights"])
            # configPath = os.path.sep.join([args["yolo"], "yolov3.cfg"])

            # load our YOLO object detector trained on COCO dataset (80 classes)
            print("---------[INFO] loading YOLO from disk...")
            net = cv2.dnn.readNetFromDarknet(configPath, weightsPath)
            # load our input image and grab its spatial dimensions
            image = cv2.imread(img_name)
            # image = cv2.imread(args["image"])
            (H, W) = image.shape[:2]

            # determine only the *output* layer names that we need from YOLO
            ln = net.getLayerNames()
            ln = [ln[i[0] - 1] for i in net.getUnconnectedOutLayers()]

                # construct a blob from the input image and then perform a forward
                # pass of the YOLO object detector, giving us our bounding boxes and
                # associated probabilities
            blob = cv2.dnn.blobFromImage(image, 1 / 255.0, (416, 416),swapRB=True, crop=False)
            net.setInput(blob)
            start = time.time()
            layerOutputs = net.forward(ln)
            end = time.time()

            # show timing information on YOLO
            print("---------[INFO] YOLO took {:.6f} seconds".format(end - start))
            # initialize our lists of detected bounding boxes, confidences, and
            # class IDs, respectively
            boxes = []
            confidences = []
            classIDs = []
            one_time=1

            # loop over each of the layer outputs
            for output in layerOutputs:
                # loop over each of the detections
                for detection in output:
                        # extract the class ID and confidence (i.e., probability) of
                        # the current object detection
                    scores = detection[5:]
                    classID = np.argmax(scores)
                    confidence = scores[classID]

                        # filter out weak predictions by ensuring the detected
                        # probability is greater than the minimum probability
                    if confidence > args["confidence"]:
                            # scale the bounding box coordinates back relative to the
                            # size of the image, keeping in mind that YOLO actually
                            # returns the center (x, y)-coordinates of the bounding
                            # box followed by the boxes' width and height
                        box = detection[0:4] * np.array([W, H, W, H])
                        (centerX, centerY, width, height) = box.astype("int")

                            # use the center (x, y)-coordinates to derive the top and
                            # and left corner of the bounding box
                        x = int(centerX - (width / 2))
                        y = int(centerY - (height / 2))

                        # update our list of bounding box coordinates, confidences,
                        # and class IDs
                        boxes.append([x, y, int(width), int(height)])
                        confidences.append(float(confidence))
                        classIDs.append(classID)
                        # apply non-maxima suppression to suppress weak, overlapping bounding
                        # boxes

                idxs = cv2.dnn.NMSBoxes(boxes, confidences, args["confidence"],args["threshold"])
                # ensure at least one detection exists
                if len(idxs) > 0:
                # loop over the indexes we are keeping
                    count=0


                    for i in idxs.flatten():
                    # extract the bounding box coordinates
                        count=count+1

                        # print(count)

                        (x, y) = (boxes[i][0], boxes[i][1])
                        (w, h) = (boxes[i][2], boxes[i][3])

                        # draw a bounding box rectangle and label on the image
                        color = [int(c) for c in COLORS[classIDs[i]]]
                        cv2.rectangle(image, (x, y), (x + w, y + h), color, 2)
                        text = "{}: {:.4f}".format(LABELS[classIDs[i]], confidences[i])
                        c_name = "{}".format(LABELS[classIDs[i]])
                        cv2.putText(image, text, (x, y - 5), cv2.FONT_HERSHEY_SIMPLEX,0.5, color, 2)


                        if(count>=aa):
                            items_found.append(c_name)
                            # print(items_found,"<",aa)
                            aa=aa+1
                        else:
                            # print("[[[[]]]]over pass")
                            pass

            # items_found.clear()
            items_found = "{} items found: {}".format(aa-1, items_found)
            # global items_found
            # flash(items_found)
###########################################################################
###########################################################################
##############             sound engine                   #################
###########################################################################
###########################################################################
            print("---------sound engin acctive")
            print("--------->>",items_found)
            mytext=items_found

            language = 'en'
            myobj = gTTS(text=mytext, lang=language, slow=False)
            myobj.save("m.mp3")
            # Playing the converted file
            # os.system("mpg321 welcome.mp3")
            print("---------saved as m.mp3")
###########################################################################
###########################################################################
            os.system("rm *.png")
            #to DELETE old saved png files
            # show the output image
            # cv2.imshow("Image", image)
            png_path=random.choice("abcdefghijklmnoqrstuvwxyz")
            global png_path
            cv2.imwrite(png_path + '.png',image)
            cv2.waitKey(0)

            print("---------","to home")
            return redirect('/s')
            # NO CODE WILL WORKE BELOW HEAR !!
        else:
            flash('Allowed file types are png,jpg,jpeg,gif !! << python server')
            return redirect(request.url)
if __name__ == "__main__":
    # app.run(debug = True)
    app.run(host = '0.0.0.0',port=5001,debug = True)

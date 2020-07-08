# stream.py
# Send captions from Web Captioner to Zoom Meeting.

import os, sys, json, logging, requests
from flask import Flask, request, make_response
from datetime  import datetime

# russfeld
from queue import PriorityQueue
import time, atexit
from apscheduler.schedulers.background import BackgroundScheduler

# global constants/flags
DEBUG = False
PORT = 9999
LINE_LENGTH = 80
ZOOM_API_TOKEN = "https://wmcc.zoom.us/closedcaption?id=94803649358&ns=Q0lTIDUyNyAtIFJpY2hhcmQ&expire=86400&sparams=id%2Cns%2Cexpire&signature=8eOpjksiKROqbO8qyTKegEtcidJGJCrNoNbYUZZStak.EwEAAAFzMEmsvQABUYAYODFkZFc0MlpoQ0JPVWxrN2NGRXFCQT09IHREb29TdmlpRFJVd0g3TDlOdUVxckdTbkhzbEszOG0x"
LANGAUGE = "en-US"  # Language code - ISO country code, e.g. de-DE.
counter = 0

#russfeld
sequenceout = 0

if not DEBUG:
    # if we're not debugging hide requests
    logging.getLogger('werkzeug').setLevel(logging.ERROR)

# clear function
def clear_output():
    os.system('cls' if os.name == 'nt' else 'clear')

# define a flask app
flask_app = Flask(__name__)

# russfeld
# make priority queue
pqueue = PriorityQueue()
scheduler = BackgroundScheduler()

@flask_app.route('/')
def home():
    return "Hello world!"

@flask_app.route('/transcribe', methods=['GET'])
def transcribe_get():
    return make_response("Can access /transcribe just fine", 200,
    {"Access-Control-Allow-Origin": "https://webcaptioner.com"})

# main post request handler
@flask_app.route('/transcribe', methods=['POST', 'PUT'])
def transcribe_post():
    # for some reason, response.get_json won't parse right
    # so we'll make json ourselves
    data = json.loads(request.get_data(as_text=True))
    reqText = data['transcript']
    sequence = data['sequence']

    # russfeld
    pqueue.put((sequence, reqText), True, 1)

    '''
    # send captions to zoom
    url = ZOOM_API_TOKEN \
        + "&seq=" + str(sequence) \
        + "&lang=" + LANGAUGE
    content = reqText + ' '
    headers = {'content-type': 'text/plain'}

    r = requests.post(url=url, data=content.encode('utf-8'), headers=headers)
    '''

    # print the request
    # print(url)
    if DEBUG:
        print(sequence, reqText)
        sys.stdout.flush()

    '''
    # break every 80 characters
    global counter
    if counter >= LINE_LENGTH:
        print('')
        counter = 0
    else:
        counter += (len(reqText) + 1)
    '''

    # return a correct response
    return make_response(json.dumps({"message": "recieved"}), 200,
    {"Content-Type": 'application/json',
     "Access-Control-Allow-Origin": "https://webcaptioner.com"
    })

def send_zoom():
    output = ""
    size = pqueue.qsize()
    for i in range(0, size):
        seq, text = pqueue.get(True, 1)
        output += text + " " 
        print("queue: ", seq, text)
 
    if len(output) > 0:
        global sequenceout
        sequenceout += 1

        # send captions to zoom
        url = ZOOM_API_TOKEN \
            + "&seq=" + str(sequenceout) \
            + "&lang=" + LANGAUGE
        content = output
        headers = {'content-type': 'text/plain'}

        # print the request
        if DEBUG:
            print(url)
            print("to zoom: {}".format(output))
            sys.stdout.flush()

        r = requests.post(url=url, data=content.encode('utf-8'), headers=headers)
    else:
        if DEBUG:
            print("queue empty")
            sys.stdout.flush()


if __name__ == "__main__":
    scheduler.add_job(func=send_zoom, trigger="interval", seconds=2)
    scheduler.start()
    atexit.register(lambda: scheduler.shutdown())
    flask_app.run(host='0.0.0.0', debug=DEBUG, port=PORT, ssl_context=('cert.pem', 'key.pem'))

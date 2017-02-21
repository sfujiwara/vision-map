# -*- coding: utf-8 -*-

import base64
import logging

import flask
import cloudstorage as gcs
from google.cloud import vision

app = flask.Flask(__name__)


@app.route("/")
def main():
    with gcs.open("/vision-map-mynavi.appspot.com/img/IMG_5861o.jpg") as f:
        img = f.read()
        img_base64 = base64.b64encode(img)
    # Detect landmarks with Cloud Vision API
    vision_client = vision.Client()
    landmarks = vision_client.image(content=img).detect_landmarks()
    logging.debug(landmarks[0].description)
    return flask.render_template("index.html", img_base64=img_base64, description=landmarks[0].description)

# -*- coding: utf-8 -*-

import base64
import logging

import flask
import cloudstorage as gcs
from google.cloud import vision

app = flask.Flask(__name__)


@app.route("/", methods=["GET", "POST"])
def main():
    if flask.request.method == "POST" and flask.request.files["file"]:
        logging.debug("use uploaded image")
        f = flask.request.files["file"]
        img = f.read()
    else:
        logging.debug("use default image")
        with gcs.open("/vision-map-mynavi.appspot.com/img/DSC00776o.jpg") as f:
            img = f.read()
    img_base64 = base64.b64encode(img)
    # Detect landmarks with Cloud Vision API
    vision_client = vision.Client()
    landmarks = vision_client.image(content=img).detect_landmarks()
    if landmarks:
        res = flask.render_template(
            "index.html",
            img_base64=img_base64,
            description=landmarks[0].description,
            latitude=landmarks[0].locations[0].latitude,
            longitude=landmarks[0].locations[0].longitude
        )
    else:
        res = flask.render_template(
            "index.html",
            img_base64=img_base64,
            description="",
            latitude=None,
            longitude=None
        )
    return res

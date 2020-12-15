from app import app
from flask import render_template
from flask import request, redirect
import os
import subprocess
import json
import base64


@app.route("/", methods=["GET", "POST"])
def upload_image():

    if request.method == "POST":

        if request.data:
            imgdata = base64.b64decode(request.data)
            filename = os.getcwd() + '/app/IO/input/input.png'
            with open(filename, 'wb') as f:
                f.write(imgdata)

            if os.path.exists(os.getcwd() + "/app/IO/output/predictions.jpg"):
                os.remove(os.getcwd() + "/app/IO/output/predictions.jpg")

            batcmd = "cd app/darknet/ && ./darknet detect cfg/yolov3.cfg yolov3.weights ../IO/input/input.png && cp predictions.jpg ../IO/output/predictions.jpg"

            result = subprocess.check_output(batcmd, shell=True)

            to_json = result.decode(
                "utf-8").split("seconds.", 1)[1]

            a = '{'

            for n in range(to_json.count("%")):
                el = to_json.split("%", -1)[n]

                a = a + "" + el.split(":", -1)[0].replace('\n', '') + ":" + el.split(
                    ":", -1)[1].replace('\n', '') + ", "
            json_data = a + '}'
            # n = json.dumps(a)
            # json_data = json.loads(n)

            if os.path.exists(os.getcwd() + "/app/IO/input/input.png"):
                os.remove(os.getcwd() + "/app/IO/input/input.png")

            with open(os.getcwd() + "/app/IO/output/predictions.jpg", "rb") as image_file:
                encoded_string = base64.b64encode(image_file.read())
                base_image = encoded_string.decode("utf-8")

            combine_result = {
                "json_data": json_data, "base_image": base_image}
            return combine_result

            # return redirect(request.url)
    return render_template("public/upload_image.html")
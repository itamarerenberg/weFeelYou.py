from flask import Flask, request
from main import fit_playlist


app = Flask(__name__)

app.run(host="0.0.0.0", port=8080)

@app.route("/", methods=['GET', 'POST'])
def getPlaylist():
    img = request.args.get("img")
    # base64 decode (str --> jpg)
    # jpg to ndarray
    img = convert_from_xxx_to_ndarray(img)
    return fit_playlist(img)


def convert_from_xxx_to_ndarray(img):
    return img  # as ndarray
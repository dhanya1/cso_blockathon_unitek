from flask import Flask, request, render_template, jsonify
from werkzeug.utils import secure_filename
import os
from file_hash import hash_doc


app = Flask(__name__, static_url_path="/static", static_folder="static")
APP_ROOT = os.path.dirname(os.path.abspath(__file__))


@app.route("/")
def index():
    return render_template("upload_file.html")


@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST':
        f = request.files['file']
        filename = os.path.join('static/', secure_filename(f.filename))
        f.save(filename)
        txn_hash = hash_doc(filename, action='store')
        res = jsonify({'txn_id':txn_hash})
        res.status_code = 200
        return render_template("block_new.html", hash_value=txn_hash, inputfilename=f.filename)

@app.route("/verify", methods=["POST"])
def verify():
    if request.method == 'POST':
        f = request.files['file']
        filename = os.path.join('static/', secure_filename(f.filename))
        f.save(filename)
        ntxn_id = request.form['hvalue']
        print(ntxn_id)
        verification = hash_doc(filename, action='verify', txn_id=ntxn_id)
        print(verification)
        res = jsonify({'verification': verification})
        res.status_code = 200
        return  render_template("verify_File.html", ver_value=verification)


if __name__ == '__main__':
    app.run()
import os
from flask import Flask, flash, request, redirect, send_file, render_template
from werkzeug.utils import secure_filename
import shortuuid
import nvidia_wrapper


ALLOWED_EXTENSIONS = {"wav"}

app = Flask(__name__)
app.config["UPLOAD_FOLDER"] = "uploads/"
app.config["OUT_FOLDER"] = "out/"


def allowed_file(filename):
    return "." in filename and filename.rsplit(".", 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route("/api", methods=["GET", "POST"])
def upload_file():
    if request.args.get("apikey") != os.environ["APIKEY"]:
        flash("Unauthorized")
        return redirect("https://zhaw.ch")

    if request.method != "POST":
        return render_template("upload.html")

    if "file" not in request.files:
        flash("No file part")
        return redirect(request.url)

    file = request.files["file"]
    if file.filename == "":
        flash("No selected file")
        return redirect(request.url)

    if not file and not allowed_file(file.filename):
        flash("File not allowed")
        return redirect(request.url)

    filename_out = process_request(file, request.args)
    return send_file(filename_out, as_attachment=True)


def process_request(file, args):
    input_file_path, output_file_path = get_in_out_filepath(file.filename)
    file.save(input_file_path)

    config_path = nvidia_wrapper.write_config(input_file_path, output_file_path, args)
    nvidia_wrapper.run_enhancer(config_path)

    # Cannot cleanup before sending
    # nvidia_wrapper.cleanup(input_file_path, output_file_path, config_path)

    return output_file_path


def get_in_out_filepath(filename):
    file_id = shortuuid.uuid()
    input_file_path = os.path.abspath(
        os.path.join(
            app.config["UPLOAD_FOLDER"], file_id + "_" + secure_filename(filename)
        )
    )

    output_file_path = os.path.abspath(
        os.path.join(
            app.config["OUT_FOLDER"], file_id + "_" + secure_filename(filename)
        )
    )

    return input_file_path, output_file_path


if __name__ == "__main__":
    app.debug = True
    app.run(host="127.0.0.1", port=8080, debug=True)

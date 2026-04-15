from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
import os
from utils.image_compress import compress_image
from utils.pdf_compress import compress_pdf
import re

app = Flask(__name__)
CORS(app)
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
UPLOAD_FOLDER = os.path.join(BASE_DIR, "uploads")
OUTPUT_FOLDER = os.path.join(BASE_DIR, "output")

os.makedirs(UPLOAD_FOLDER, exist_ok=True)
os.makedirs(OUTPUT_FOLDER, exist_ok=True)

def get_extension(filename):
    return filename.rsplit(".", 1)[-1].lower()

def sanitize_filename(filename):
    return re.sub(r'[^a-zA-Z0-9.]', '_', filename)

@app.route("/upload", methods=["POST"])

def upload_file():
    file = request.files.get("file")
    compression = request.form.get("compression", "Recommended Compression")
    if not file:
        return jsonify({"error": "No file uploaded"}), 400
    clean_name = sanitize_filename(file.filename)
    input_path = os.path.join(UPLOAD_FOLDER, clean_name)
    file.save(input_path)
    ext = get_extension(file.filename)
    output_filename = f"compressed_{clean_name}"
    output_path = os.path.join(OUTPUT_FOLDER, output_filename)   
    if ext in ["jpg", "jpeg", "png"]:
        compress_image(input_path, output_path, compression)
    elif ext == "pdf":
        compress_pdf(input_path, output_path, compression)
    else:
        return jsonify({"error": "Unsupported file type"}), 400

    return jsonify({
        "message": f"{ext.upper()} processed successfully",
        "downloadUrl": f"http://127.0.0.1:5000/download/{output_filename}"
    })

@app.route("/download/<filename>")
def download_file(filename):
    path = os.path.join(OUTPUT_FOLDER, filename)
    return send_file(path, as_attachment=True)

if __name__ == "__main__":
    app.run(debug=True)
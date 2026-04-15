import os
import re
import uuid
import boto3
from flask import Flask, request, jsonify
from flask_cors import CORS
from botocore.exceptions import NoCredentialsError, ClientError
from utils.image_compress import compress_image
from utils.pdf_compress import compress_pdf

app = Flask(__name__)
CORS(app)

BUCKET_NAME = os.environ.get("S3_BUCKET_NAME", "your-localshrink-bucket")
TEMP_DIR = "/tmp" 

s3_client = boto3.client('s3')

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

    job_id = str(uuid.uuid4())
    clean_name = sanitize_filename(file.filename)
    input_filename = f"in_{job_id}_{clean_name}"
    output_filename = f"compressed_{job_id}_{clean_name}"
    input_path = os.path.join(TEMP_DIR, input_filename)
    output_path = os.path.join(TEMP_DIR, output_filename)

    try:
        file.save(input_path)
        ext = get_extension(file.filename)
        if ext in ["jpg", "jpeg", "png"]:
            compress_image(input_path, output_path, compression)
        elif ext == "pdf":
            compress_pdf(input_path, output_path, compression)
        else:
            return jsonify({"error": "Unsupported file type"}), 400

        content_type = "application/pdf" if ext == "pdf" else f"image/{ext}"
        s3_client.upload_file(
            output_path, 
            BUCKET_NAME, 
            output_filename,
            ExtraArgs={'ContentType': content_type}
        )

        download_url = s3_client.generate_presigned_url(
            'get_object',
            Params={'Bucket': BUCKET_NAME, 'Key': output_filename},
            ExpiresIn=900 
        )

        if os.path.exists(input_path): os.remove(input_path)
        if os.path.exists(output_path): os.remove(output_path)
        return jsonify({
            "message": f"{ext.upper()} processed and stored for 15 minutes",
            "downloadUrl": download_url,
            "expiresIn": "15 minutes"
        })
    except ClientError as e:
        print(f"AWS S3 Error: {e}")
        return jsonify({"error": "Cloud storage failure"}), 500
    except Exception as e:
        print(f"Processing Error: {e}")
        return jsonify({"error": "Internal server error"}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=int(os.environ.get("PORT", 5000)))
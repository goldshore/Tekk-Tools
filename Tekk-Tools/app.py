from flask import Flask, request, redirect, flash, render_template
from werkzeug.utils import secure_filename
import os
from dotenv import load_dotenv
import whisper

# Load environment variables
load_dotenv()

app = Flask(__name__)
app.secret_key = 'arthurgpt'

# Configure upload folder
UPLOAD_FOLDER = os.getenv("UPLOAD_DIR", "./uploads")
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Allowed file extensions
ALLOWED_FORMATS = os.getenv("ALLOWED_FORMATS", "mp3,wav,flac,m4a").split(",")
MAX_FILE_SIZE_MB = int(os.getenv("MAX_FILE_SIZE", "20"))

def allowed_file(filename):
    """Check if the file has an allowed extension."""
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_FORMATS

@app.route("/", methods=["GET", "POST"])
def upload_file():
    """Handle file uploads and transcription."""
    if request.method == "POST":
        if 'file' not in request.files:
            flash("No file part")
            return redirect(request.url)

        file = request.files['file']
        if file.filename == '':
            flash("No selected file")
            return redirect(request.url)

        if file and allowed_file(file.filename):
            # Check file size
            file.seek(0, os.SEEK_END)
            file_size_mb = file.tell() / (1024 * 1024)
            file.seek(0)
            if file_size_mb > MAX_FILE_SIZE_MB:
                flash(f"File size exceeds the maximum limit of {MAX_FILE_SIZE_MB} MB.")
                return redirect(request.url)

            # Save the file
            filename = secure_filename(file.filename)
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            file.save(file_path)

            # Transcribe the audio
            try:
                model_name = os.getenv("WHISPER_MODEL", "base")
                model = whisper.load_model(model_name)
                result = model.transcribe(file_path)
                transcription = result.get("text", "No transcription available.")
                return render_template("result.html", transcription=transcription)
            except Exception as e:
                flash(f"Error during transcription: {e}")
                return redirect(request.url)
        else:
            flash("Invalid file format")
            return redirect(request.url)

    return render_template("index.html")

if __name__ == "__main__":
    app.run(debug=True, port=int(os.getenv("PORT", 3000)))
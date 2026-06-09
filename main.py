from flask import Flask, render_template, request
import uuid
from werkzeug.utils import secure_filename
import os

UPLOAD_FOLDER = 'user_uploads'
ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg'}

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/create", methods=["GET", "POST"])
def create():
    myid = uuid.uuid1()
    if request.method == "POST":
        print(request.files.keys())
        rec_id = request.form.get("uuid")
        desc = request.form.get("text")
        input_files = []
        
        # Safely establish the folder structure for this specific record
        record_dir = os.path.join(app.config['UPLOAD_FOLDER'], rec_id)
        os.makedirs(record_dir, exist_ok=True)

        # Process and save all uploaded files securely
        for key, file in request.files.items():
            print(key, file)
            if file and file.filename:
                filename = secure_filename(file.filename)
                file.save(os.path.join(record_dir, filename))
                input_files.append(filename)
                print(filename)

        # Write text description only one time per submission request
        if desc:
            with open(os.path.join(record_dir, "desc.txt"), "w") as f:
                f.write(desc)
        
        # Generate the ffmpeg playlist input file smoothly
        if input_files:
            with open(os.path.join(record_dir, "input.txt"), "w") as f:
                for fl in input_files:
                    f.write(f"file '{fl}'\nduration 1\n")

    return render_template("create.html", myid=myid)


@app.route("/gallery")
def gallery():
    reels = os.listdir("static/reels")
    print(reels)
    return render_template("gallery.html", reels=reels)


if __name__ == "__main__":
    # Ensure mandatory baseline directories exist before launching server
    os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)
    os.makedirs(os.path.join('static', 'reels'), exist_ok=True)
    
    app.run(debug=True)
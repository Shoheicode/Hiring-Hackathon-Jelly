import os
from flask import Flask, jsonify, request, send_file
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
global cas
cas = ""
# Configure upload folder
UPLOAD_FOLDER = "uploads"
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER

# Ensure the upload folder exists
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

@app.route("/members", methods=['GET'])
def return_home():
    return "Hello" + str(cas)

@app.route('/login', methods=["POST"])
def login():
    try:
        print("IHIHIHI")
        #print("RUNNINg" + request.get_json().get("hello"))
        first_name = request.get_json().get("name")
        print(first_name)
        cas = first_name
        #cas +=1
        return jsonify({"message": "User created!"}), 201
    except Exception as e:
        return jsonify({"message: ": str(e)}), 400

@app.route('/upload', methods=["POST"])
def gamer():
    if not os.path.exists('files'):
        os.makedirs('files')
    #print(request.get_data())
    if 'video' not in request.files:
        print("AM NOT HERE BOIII")
        return 'No video file', 400
    
    video = request.files['video']
    
    if video.filename == '':
        return 'No selected file', 400
    
    if video and video.filename.endswith('.mp4'):
        filename = video.filename
        video.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))
        return 'Video uploaded successfully', 200
    
    return 'Invalid file type', 400

@app.route('/uploads/<filename>', methods=['GET'])
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    if os.path.exists(file_path):
        return send_file(file_path, as_attachment=True)
    else:
        return "File not found", 404

if __name__ == "__main__":
    app.run(debug=True)
import os
from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

app = Flask(__name__)
cors = CORS(app)
app.config['CORS_HEADERS'] = 'Content-Type'
global cas
cas = ""

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

@app.route('/gam', methods=["POST"])
def gamer():
    if not os.path.exists('files'):
        os.makedirs('files')
    print(request.files.__len__())
    if 'video' not in request.files:
        print("AM NOT HERE BOIII")
        return 'No video file', 400
    
    video = request.files['video']
    
    if video.filename == '':
        return 'No selected file', 400
    
    if video and video.filename.endswith('.mp4'):
        filename = video.filename
        video.save(os.path.join('uploads', filename))
        return 'Video uploaded successfully', 200
    
    return 'Invalid file type', 400

if __name__ == "__main__":
    app.run(debug=True)
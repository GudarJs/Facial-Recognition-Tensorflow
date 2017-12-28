from flask import Flask, render_template, request, jsonify, abort
from src.recognition import recognize_faces
from src.face import Recognition

app = Flask(__name__, static_url_path='', static_folder='statics')
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024 # 16 MB

@app.route('/')
def home():
    return render_template('home.html')

@app.route('/recognize/faces', methods=['POST'])
def face_recognizer():
    try:
        encoded_image = request.files['file']
    except:
        abort(422)

    image, faces = recognize_faces(encoded_image, face_recognition)

    return jsonify({ 'image': image, 'faces': faces }), 200

if __name__ == '__main__':
    face_recognition = Recognition()
    app.run(host= '0.0.0.0')

from keras.models import load_model
from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS
import numpy as np
import cv2
import os

app = Flask(__name__)
CORS(app)
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'uploads')

@app.route("/api/hello", methods=["POST"])
def hello():
    test = "HALOOOOO"

    return jsonify({'status': test})

@app.route('/api/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    
    # load image
    file = request.files['image']
    filename = file.filename
    image_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    file.save(image_path)

    # image prepocessing
    img_prepocessed = image_prepocessing(image_path)
    test_img_ex = np.expand_dims(img_prepocessed, axis=0)

    # classification
    vgg16_result = vgg16_model(test_img_ex)

    return jsonify({'classify': vgg16_result})

# vgg16 predict
def vgg16_model(test_img_ex):
    classes = ['Penyakit Bercak', 'Penyakit Hawar', 'Penyakit Karat', 'Daun Sehat']
    model = load_model('api/vgg16.h5')
    vgg16_predicts = model.predict(test_img_ex)
    predicted_class_index = np.argmax(vgg16_predicts[0])
    vgg16_classify = classes[predicted_class_index]

    return vgg16_classify

# image prepocessing
def image_prepocessing(image_path):
    new_image = cv2.imread(image_path, cv2.IMREAD_COLOR)
    new_image = cv2.resize(new_image, (224, 224))
    test_img = np.array(new_image) / 255

    return test_img

# image uploads
@app.route('/uploads/<path:filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

if __name__ == "__main__":
    app.run()
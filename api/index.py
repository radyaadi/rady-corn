from keras.models import load_model
from flask import Flask, request, jsonify
from flask_cors import CORS
import numpy as np
import cv2

from PIL import Image
from io import BytesIO

app = Flask(__name__)
CORS(app)

@app.route("/api/hello", methods=["POST"])
def hello():
    test = "HALOOOOO"

    return jsonify({'status': test})

@app.route('/api/classify', methods=['POST'])
def classify():
    if 'image' not in request.files:
        return jsonify({'error': 'No image uploaded'})
    
    # load image
    image_data = request.files['image'].read()
    image = Image.open(BytesIO(image_data))

    # image prepocessing
    new_image = np.array(image)
    new_image = cv2.resize(new_image, (224, 224))
    test_img = np.array(new_image) / 255
    test_img_ex = np.expand_dims(test_img, axis=0)

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

if __name__ == "__main__":
    app.run()
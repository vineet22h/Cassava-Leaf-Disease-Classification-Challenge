from flask import Flask, render_template, flash, redirect, url_for, request, jsonify
from werkzeug.utils import secure_filename
import numpy as np
from PIL import Image
import os
from model.main import create_model_b4, create_model_b5, create_model_b7

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
all_imgs = []
predictions = []
curr_index = 0
leaf_count = {}
label_map = ["Cassava Bacterial Blight (CBB)", "Cassava Brown Streak Disease (CBSD)", "Cassava Green Mottle (CGM)", "Cassava Mosaic Disease (CMD)", "Healthy"]

import tensorflow as tf
# gpus = tf.config.experimental.list_physical_devices('GPU')
# tf.config.experimental.set_memory_growth(gpus[0], True)

# model_1 = create_model_b7()
# model_2 = create_model_b4()
model_3 = create_model_b5()

# model_1.load_weights('model/weights/EffNetB7_512_8.h5')
# model_2.load_weights('model/weights/EffNetB4_380_8.h5')
model_3.load_weights('model/weights/EffNetB5_456_8.h5')

## Just a hack to make changes in css 
@app.context_processor
def override_url_for():
    return dict(url_for=dated_url_for)

def dated_url_for(endpoint, **values):
    if endpoint == 'static':
        filename = values.get('filename', None)
        if filename:
            file_path = os.path.join(app.root_path,
                                 endpoint, filename)
            values['q'] = int(os.stat(file_path).st_mtime)
    return url_for(endpoint, **values)

@app.route('/')
def upload_form():
    print('in upload_form')
    return render_template('main.html')

@app.route('/file', methods=['POST'])
def upload_image():
    print('in upload_image')
    global curr_index
    imgs = request.files
    if len(imgs) == 0:
        response = jsonify({'response': False})
        return response

    for img in imgs:
        file = imgs[img]
        filename = file.filename
        print(filename)
        filename = secure_filename(filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        all_imgs.append(filename)
    curr_image = all_imgs[curr_index]
    pred = predict(curr_image)

    return jsonify({'filename': curr_image,
                    'pred':pred})

@app.route('/next')
def next():
    global curr_index 
    print('in next')
    curr_index+=1
    curr_image = all_imgs[curr_index]
    if curr_index == len(all_imgs)-1:
        pred = predict(curr_image)
        return jsonify({'response':False, 
                        'pred': pred,
                        'filename': all_imgs[curr_index]})
    if not os.path.exists(all_imgs[curr_index]):
        pred = predict(curr_image)
    return jsonify({'response':True, 
                    'pred': pred,
                    'filename': all_imgs[curr_index]})

@app.route('/previous')
def previous():
    global curr_index
    print('in previous') 
    curr_index-=1
    print(curr_index)
    curr_image = all_imgs[curr_index]
    if curr_index == 0:
        pred = predict(curr_image)
        return jsonify({'response':False, 
                        'pred': pred,
                        'filename': all_imgs[curr_index]})

    if not os.path.exists(all_imgs[curr_index]):
        pred = predict(curr_image)
    return jsonify({'response':True, 
                    'pred': pred,
                    'filename': all_imgs[curr_index]})

@app.route('/reload')
def reload():
    global all_imgs
    global curr_index
    models = ['eff', 'res','deep']
    print("in reload")
    for img in all_imgs:
    
        os.unlink('static/uploads/'+img)
    all_imgs = []
    curr_index = 0
    return jsonify({'response': True})

def predict(img_filename):
    mid = []
    image = Image.open('static/uploads/'+img_filename)
    # image_1 = image.resize((600, 600))
    # image_2 = image.resize((380, 380))
    image_3 = image.resize((456, 456))
    # image_1 = np.expand_dims(image_1, axis = 0)
    # image_2 = np.expand_dims(image_2, axis = 0)
    image_3 = np.expand_dims(image_3, axis = 0)
    # pred_1 = model_1.predict(image_1)
    # pred_2 = model_2.predict(image_2)
    pred_3 = model_3.predict(image_3)
    # mid.append(pred_1)
    # mid.append(pred_2)
    # mid.append(pred_3)
    # result = np.array(mid).reshape(3, 5).mean(axis = 0)
    return label_map[int(np.argmax(pred_3))]

if __name__ == "__main__":
    app.run(host = "0.0.0.0", port = 5000)
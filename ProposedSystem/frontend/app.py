import os
import sqlite3
from flask import Flask, render_template, request, redirect, session, url_for, flash
from werkzeug.utils import secure_filename
import pickle
from tensorflow.keras.models import load_model
from tensorflow.keras.preprocessing.sequence import pad_sequences
from tensorflow.keras.preprocessing.image import load_img, img_to_array
import numpy as np
from datetime import datetime

app = Flask(__name__)
app.secret_key = 'secret_key'
UPLOAD_FOLDER = 'static/uploads'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# SQLite setup
def get_db():
    conn = sqlite3.connect('app.db')
    conn.row_factory = sqlite3.Row
    return conn

# Load sentiment model and tokenizer
with open("tokenizer.pkl", "rb") as f:
    tokenizer = pickle.load(f)
text_model = load_model("sentiment_model.h5")
max_sequence_length = 100

# Load image model
image_model = load_model("model_v1.h5")
img_height = 128
img_width = 128

def predict_text(text):
    seq = tokenizer.texts_to_sequences([text])
    padded = pad_sequences(seq, maxlen=max_sequence_length)
    pred = text_model.predict(padded)[0][0]
    return "Fake" if pred < 0.5 else "Real"

def predict_image(img_path):
    my_image = load_img(img_path, target_size=(img_height, img_width))
    my_image = img_to_array(my_image)
    my_image = np.expand_dims(my_image, 0)
    out = np.round(image_model.predict(my_image)[0][0], 2)
    return "Fake" if out > 0.5 else "Real"

@app.route('/')
def index():
    return redirect(url_for('login'))

@app.route('/register', methods=['GET', 'POST'])
def register():
    if request.method == 'POST':
        name = request.form['name']
        mobile = request.form['mobile']
        email = request.form['email']
        password = request.form['password']

        db = get_db()
        user_id = db.execute("SELECT MAX(id) FROM user").fetchone()[0]
        next_id = (user_id + 1) if user_id else 1

        db.execute("INSERT INTO user (id, name, mobile, email, password) VALUES (?, ?, ?, ?, ?)",
                   (next_id, name, mobile, email, password))
        db.commit()
        return redirect('/login')
    return render_template('register.html')

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        db = get_db()
        user = db.execute("SELECT * FROM user WHERE email=? AND password=?", (email, password)).fetchone()
        if user:
            session['user_id'] = user['id']
            return redirect('/feed')
        flash("Invalid credentials")
    return render_template('login.html')
@app.route('/feed', methods=['GET', 'POST'])
def feed():
    if 'user_id' not in session:
        return redirect('/login')

    db = get_db()
    prediction_data = None

    if request.method == 'POST':
        content = request.form.get('content', '').strip()
        image = request.files.get('image')

        if not content and (not image or image.filename == ''):
            flash("Please provide either text or an image.")
            return redirect('/feed')

        text_label = None
        image_label = None
        filename = None
        is_fake = 0

        if content:
            text_label = predict_text(content)
            if text_label == "Fake":
                is_fake = 1

        if image and image.filename != '':
            filename = secure_filename(image.filename)
            filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
            image.save(filepath)

            image_label = predict_image(filepath)
            if image_label == "Fake":
                is_fake = 1

        feed_id = db.execute("SELECT MAX(fid) FROM feed").fetchone()[0]
        next_fid = (feed_id + 1) if feed_id else 1

        db.execute(
            "INSERT INTO feed (fid, content, images, fake, trans, uid) VALUES (?, ?, ?, ?, ?, ?)",
            (next_fid, content, filename, is_fake, datetime.now(), session['user_id'])
        )
        db.commit()

        prediction_data = {
            "text": text_label,
            "image": image_label,
            "image_file": filename,
            "fake": is_fake
        }
        flash("Feed added successfully.")

    # Fetch all posts with user details, ordered by datetime descending
    posts = db.execute(
        "SELECT f.*, u.name, u.email FROM feed f JOIN user u ON f.uid = u.id ORDER BY f.trans DESC"
    ).fetchall()

    # Calculate credibility for each user
    post_data_with_credibility = []
    for post in posts:
        user_id = post['uid']
        user_posts = db.execute(
            "SELECT * FROM feed WHERE uid = ?", (user_id,)
        ).fetchall()
        total_posts = len(user_posts)
        fake_posts = sum(1 for p in user_posts if p['fake'] == 1)
        credibility = round(100 * (total_posts - fake_posts) / total_posts, 2) if total_posts > 0 else 100

        post_data_with_credibility.append({
            **post,
            "credibility": credibility
        })

    return render_template('feed.html', prediction=prediction_data, posts=post_data_with_credibility)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    return redirect('/login')

if __name__ == '__main__':
    os.makedirs(UPLOAD_FOLDER, exist_ok=True)
    app.run(debug=True)

# 📰 Multimodal Fake News Detection System
A robust and intelligent fake news detection platform integrating Natural Language Processing and Computer Vision techniques. The system classifies news as real or fake using both text and image inputs and promotes responsible sharing through a user credibility scoring mechanism.

## 🚀 Features
🔠 Text Analysis using BERT + BiLSTM

🖼️ Image Analysis using ResNet-101

🧠 Hybrid Deep Learning Models for improved accuracy

🧾 SQLite Database for user and content management

🔒 User Authentication & Session Management

📊 Credibility Score Tracking for each user

🌐 Flask-based Web Application with responsive UI

## 📌 Project Objective
To build a scalable, multimodal system capable of detecting fake news content using text and images, and to enhance digital accountability by assigning credibility scores to users based on the authenticity of their shared content.

## 🧱 System Architecture
### 🔤 Textual Analysis Pipeline
Preprocessing: Tokenization using bert-base-uncased

Feature Extraction: BERT Embeddings

Classification: BiLSTM Layer + Dense Layer

### 🖼️ Image Analysis Pipeline
Preprocessing: Resizing and Normalization

Model: CNN using ResNet-101

Output: Binary Classification (Fake/Real)

### 🧾 Credibility Scoring System
Credibility = (No. of Real Posts / Total Posts) × 100

### 🖥️ Flask Web Application
Frontend: HTML, CSS, JavaScript

Backend: Python Flask

Database: SQLite

### 📚 Datasets Used
📝 WELFake Dataset (Kaggle)
Format: CSV

Fields: Title, Text, Label (0: Real, 1: Fake)

🖼️ Fake News Image Classifier (Roboflow)
Format: Image folders (/Fake, /Real)

Purpose: Train ResNet-101 for image classification

## 🧪 Experimental Setup
### ⚙️ Hardware
Intel Core i5 10th Gen or above

Minimum 4 GB RAM, 256 GB SSD

### 💻 Software
OS: Windows 10+

Python 3.7+

Libraries: TensorFlow, Keras, PyTorch, Flask, Scikit-learn

## 📊 Results
Model	Accuracy	Loss	F1 Score
Text Model (BiLSTM + BERT)	High	Low	High
Image Model (ResNet-101)	High	Low	High

Confusion matrices and training plots confirm robust performance for both models. Combined analysis improves overall confidence and accuracy.

## 🔐 Modules Overview
User Authentication Module

Text & Image Prediction Modules

Feed Management System

Credibility Scoring Module

Database Management Module

## 📷 Screenshots

Registration/Login	:Secure user access
![image](https://github.com/user-attachments/assets/28b8466c-cee7-4f88-9154-e96413ca81cf)
![image](https://github.com/user-attachments/assets/39f71ed0-50a7-4fa3-aac8-77a6b593763b)

Home Page	:News submission portal
![image](https://github.com/user-attachments/assets/e8c4c10f-d441-43f9-8872-dd645e9afcc7)

Feed Page	:View and evaluate posts
![image](https://github.com/user-attachments/assets/a580b55b-0a4c-4466-87dd-089267894c23)

Prediction Results	:Fake or Real
![image](https://github.com/user-attachments/assets/124f5499-1b88-45bd-96c6-1ee7e512e59d)


## 💡 Future Enhancements
🎥 Video Content Analysis

🌍 Multilingual Text Processing

⚡ Real-time News Scraping

⛓️ Blockchain for Source Verification

☁️ Cloud Deployment for Scalability

## 📑 References
Key research papers and benchmark models used are cited in the full project report. Includes works published in IEEE Access, Computational Social Systems, and Roboflow.

## 👩‍💻 How to Run Locally
bash
Copy
Edit
# Clone the repository
git clone https://github.com/yourusername/fake-news-detection.git
cd fake-news-detection

# Create a virtual environment
python -m venv venv
source venv/bin/activate  # or venv\Scripts\activate (Windows)

# Install dependencies
pip install -r requirements.txt

# Start the Flask app
python app.py

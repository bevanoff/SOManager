import os
import logging
from flask import Flask, render_template, jsonify, request, send_from_directory
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy.orm import DeclarativeBase

logging.basicConfig(level=logging.DEBUG)

class Base(DeclarativeBase):
    pass

db = SQLAlchemy(model_class=Base)
app = Flask(__name__)
app.secret_key = os.environ.get("SESSION_SECRET")

# Use SQLite for simplicity
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///downloads.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False
db.init_app(app)

# Import models after db initialization
from models import DownloadCount

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/download')
def download():
    download_count = DownloadCount.query.first()
    count = download_count.count if download_count else 0
    return render_template('download.html', download_count=count)

@app.route('/increment-downloads', methods=['POST'])
def increment_downloads():
    download_count = DownloadCount.query.first()
    if not download_count:
        download_count = DownloadCount(count=0)
        db.session.add(download_count)
    download_count.count += 1
    db.session.commit()
    return jsonify({"count": download_count.count})

with app.app_context():
    db.create_all()
    # Initialize counters if not exist
    if not DownloadCount.query.first():
        initial_count = DownloadCount(count=0)
        db.session.add(initial_count)
        db.session.commit()

    # Ensure downloads directory exists
    os.makedirs('static/downloads/windows', exist_ok=True)
    os.makedirs('static/downloads/macos', exist_ok=True)
    os.makedirs('static/downloads/linux', exist_ok=True)
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
from models import DownloadCount, ViewCount

@app.route('/')
def index():
    view_count = ViewCount.query.first()
    if not view_count:
        view_count = ViewCount(count=0)
        db.session.add(view_count)
        db.session.commit()
    view_count.count += 1
    db.session.commit()
    count = view_count.count
    return render_template('index.html', view_count=count)

@app.route('/safety')
def safety():
    return render_template('safety.html')

@app.route('/download')
def download():
    download_count = DownloadCount.query.first()
    count = download_count.count if download_count else 0
    return render_template('download.html', download_count=count)

@app.route('/download/<platform>/<filename>')
def download_file(platform, filename):
    """Handle file downloads from the static/downloads directory"""
    return send_from_directory('static/downloads', f"{platform}/{filename}")

@app.route('/increment-downloads', methods=['POST'])
def increment_downloads():
    download_count = DownloadCount.query.first()
    if not download_count:
        download_count = DownloadCount(count=0)
        db.session.add(download_count)
    download_count.count += 1
    db.session.commit()
    return jsonify({"count": download_count.count})

@app.route('/increment-views', methods=['POST'])
def increment_views():
    view_count = ViewCount.query.first()
    if not view_count:
        view_count = ViewCount(count=0)
        db.session.add(view_count)
    view_count.count += 1
    db.session.commit()
    return jsonify({"count": view_count.count})

with app.app_context():
    db.create_all()
    # Initialize counters if not exist
    if not DownloadCount.query.first():
        initial_download_count = DownloadCount(count=0)
        db.session.add(initial_download_count)
        db.session.commit()
    
    if not ViewCount.query.first():
        initial_view_count = ViewCount(count=0)
        db.session.add(initial_view_count)
        db.session.commit()

    # Ensure downloads directory exists
    os.makedirs('static/downloads/windows', exist_ok=True)
    os.makedirs('static/downloads/macos', exist_ok=True)
    os.makedirs('static/downloads/linux', exist_ok=True)
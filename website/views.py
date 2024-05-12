from flask import Blueprint, render_template, request, jsonify, redirect, url_for
from .models import *
from werkzeug.utils import secure_filename
import os 
from flask_login import login_required, current_user
from ._init_ import db

views = Blueprint('views', __name__)  # views can be changed
UPLOAD_IMG = "static/upload_image/"  # Path to the uploaded images
UPLOAD_FILES = "static/upload_file/"  # Path to the uploaded files

@views.route('/')  #Viewing as guests
def home():
    return render_template("home.html", user=current_user)

@views.route('/dashboard')  #Login successfully
def dashboard():
  return render_template("dashboard.html")


@views.route('/browse')  #Login successfully
def browse():
  return render_template("browse.html")


@views.route('/demos')  #change this into orders or library
def demos():
  return render_template("demos.html")


@views.route('/uploadgame', methods=['GET', 'POST'])
def uploadgame():
    if request.method == 'POST':
        # Extract data from the form
        title = request.form.get('game_title')
        developer_name = request.form.get('game_developer')
        genres = request.form.getlist('genre[]')
        price = float(request.form.get('game-price'))
        description = request.form.get('game_description')
        donation = request.form.get('game_donation')
        # Handle file uploads for game image and zip file
        game_image = request.files['game_image']
        game_zip = request.files['zip_file']
        
        # Store the file
        game_image_filename = secure_filename(game_image.filename)
        game_image_path = os.path.join(UPLOAD_IMG, game_image_filename)
        os.makedirs(os.path.dirname(game_image_path), exist_ok=True)
        game_image.save(game_image_path)

        game_zip_filename = secure_filename(game_zip.filename)
        game_zip_path = os.path.join(UPLOAD_FILES, game_zip_filename)
        os.makedirs(os.path.dirname(game_zip_path), exist_ok=True)
        game_zip.save(game_zip_path)

        # Query the Developer object based on the provided developer name
        developer = Developer.query.filter_by(devName=developer_name).first()
        if not developer:
           # Check if a Developer with the same email already exists
            existing_developer = Developer.query.filter_by(email=current_user.email).first()
            if existing_developer:
          # If a Developer with the same email already exists, use that Developer
              developer = existing_developer
            else:
            # If no Developer with the same email exists, create a new Developer
              developer = Developer(devName=developer_name, donation=donation, email=current_user.email, user_id=current_user.id)
              db.session.add(developer)
              db.session.commit()
          
        # Create a new Game object and save it to the database, appending genre
        new_game = Game(title=title, developer_id=developer.id, price=price, description=description, image=game_image_path, data=game_zip_path)
        db.session.add(new_game)
        db.session.commit()
        for value in genres:
          category = Game_catalog.query.filter_by(category=value).first()
          if category:
            new_game.categories.append(category) # updates game_catalog_games table to link game to category
        db.session.commit()

        return redirect(url_for('views.home'))  # Redirect to the home page after upload

    return render_template("uploadgame.html")

@views.route('/cart', methods=['GET', 'POST'])  #Login successfully
def cart():
  return render_template("cart.html")


@views.route('/add_to_cart', methods=['POST'])  # add games to cart, for a seemless experience, using javascript to POST
def add_to_cart():
  return "<h1>Test</h1>"

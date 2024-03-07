from flask import Flask
from flask import render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
# Load environment variables from .env file

variables = dict(os.environ)



app = Flask(__name__)
app.congig['dbhost'] = variables['POSTGRES_HOST']
app.congig['dbuser'] = variables['POSTGRES_USER']
app.congig['dbpass'] = variables['POSTGRES_PASSWORD']
app.congig['dbname'] = variables['POSTGRES_DATABASE']

# Set up PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config['dbuser']}:{app.config['dbpass']}@{app.config['dbhost']}/{app.config['dbname']}"
db = SQLAlchemy(app)

class Admin(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Game(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admin.admin_id'), nullable=False)
    admin = db.relationship('Admin', backref=db.backref('games', lazy=True))

class Player(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'), nullable=False)
    game = db.relationship('Game', backref=db.backref('players', lazy=True))

class Pairing(db.Model):
    pairing_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('game.game_id'), nullable=False)
    game = db.relationship('Game', backref=db.backref('pairings', lazy=True))
    assassin = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=False)
    target = db.Column(db.Integer, db.ForeignKey('player.player_id'), nullable=False)


@app.route('/')
def hello():
    return render_template('home.html')

@app.route('/how-to-play')
def about():
    return render_template('instructions.html')

@app.route('/player-login')
def player_login():
    return render_template('player_login.html')

@app.route('/admin-login')
def admin_login():
    return render_template('admin_login.html')

@app.route('/test')
def test():
    admins = Admin.query.all()
    return admins

# if __name__ == '__main__':
#     app.run(debug=True)


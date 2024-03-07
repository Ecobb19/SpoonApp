from flask import Flask
from flask import render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
import os
import json
# Load environment variables from .env file

variables = dict(os.environ)

if os.path.isfile('config.json'):
    variables = json.load(open('config.json'))
else:
    variables = dict(os.environ)




app = Flask(__name__)
app.config['dbhost'] = variables['POSTGRES_HOST']
app.config['dbuser'] = variables['POSTGRES_USER']
app.config['dbpass'] = variables['POSTGRES_PASSWORD']
app.config['dbname'] = variables['POSTGRES_DATABASE']

# Set up PostgreSQL connection
app.config['SQLALCHEMY_DATABASE_URI'] = f"postgresql://{app.config['dbuser']}:{app.config['dbpass']}@{app.config['dbhost']}/{app.config['dbname']}"
db = SQLAlchemy(app)

class Admins(db.Model):
    admin_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    password = db.Column(db.String(100), nullable=False)

class Games(db.Model):
    game_id = db.Column(db.Integer, primary_key=True)
    game_name = db.Column(db.String(100), nullable=False)
    admin_id = db.Column(db.Integer, db.ForeignKey('admins.admin_id'), nullable=False)
    admin = db.relationship('Admins', backref=db.backref('games', lazy=True))

class Players(db.Model):
    player_id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    game = db.relationship('Games', backref=db.backref('players', lazy=True))

class Pairings(db.Model):
    pairing_id = db.Column(db.Integer, primary_key=True)
    game_id = db.Column(db.Integer, db.ForeignKey('games.game_id'), nullable=False)
    assassin_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    target_id = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    game = db.relationship('Games', backref=db.backref('pairings', lazy=True))
    assassin = db.relationship('Players', foreign_keys=[assassin_id])
    target = db.relationship('Players', foreign_keys=[target_id])

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
    admins = Admins.query.filter_by(username='username').all()
    admins = [admin.username for admin in admins]
    return str(admins)

if __name__ == '__main__':
    app.run(debug=True)

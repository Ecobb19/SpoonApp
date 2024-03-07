from flask import Flask
from flask import render_template, request, redirect, url_for
import os
from flask_sqlalchemy import SQLAlchemy
# Load environment variables from .env file

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
    assassin = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    target = db.Column(db.Integer, db.ForeignKey('players.player_id'), nullable=False)
    game = db.relationship('Games', backref=db.backref('pairings', lazy=True))
    assassin_ = db.relationship('Players', backref=db.backref('pairings', lazy=True))
    target_ = db.relationship('Players', backref=db.backref('pairings', lazy=True))
    

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
    admins = Admins.query.all()
    return admins

# if __name__ == '__main__':
#     app.run(debug=True)



# # LAMBDA_WARNING: Unhandled exception. The most likely cause is an 
# issue in the function code. However, in rare cases, a Lambda runtime
# update can cause unexpected function behavior. For functions using 
# managed runtimes, runtime updates can be triggered by a function 
# change, or can be applied automatically. To determine if the runtime 
# has been updated, check the runtime version in the INIT_START log 
# entry. If this error correlates with a change in the runtime version, 
# you may be able to mitigate this error by temporarily rolling back to
# the previous runtime version. For more information, 
# see https://docs.aws.amazon.com/lambda/latest/dg/runtimes-update.html

# # [ERROR] Runtime.ImportModuleError: Unable to import module 'vc__
# handler__python': No module named 'psycopg2'
# # Traceback (most recent call last):



# sqlalchemy.exc.InvalidRequestError: One or more mappers failed to 
# initialize - can't proceed with initialization of other mappers. 
# Triggering mapper: 'Mapper[Games(games)]'. Original exception was: 
# When initializing mapper Mapper[Games(games)], expression 'Admin' 
# failed to locate a name ('Admin'). If this is a class name, consider 
# adding this relationship() to the <class '__init__.Games'> class 
# after both dependent classes have been defined.


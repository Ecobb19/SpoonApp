from flask import Flask
from flask import render_template, request, redirect, url_for


app = Flask(__name__)

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
    return POSTGRES_URL


# if __name__ == '__main__':
#     app.run(debug=True)
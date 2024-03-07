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

# [ERROR]	2024-03-07T19:30:11.155Z	7d5dc084-9805-47d2-85e1-697658fa66b3	Exception on /test [GET]
# Traceback (most recent call last):
#   File "/var/task/sqlalchemy/orm/relationships.py", line 2425, in _determine_joins
#     self.primaryjoin = join_condition(
#   File "/var/task/sqlalchemy/sql/util.py", line 123, in join_condition
#     return Join._join_condition(
#   File "/var/task/sqlalchemy/sql/selectable.py", line 1343, in _join_condition
#     cls._joincond_trim_constraints(
#   File "/var/task/sqlalchemy/sql/selectable.py", line 1488, in _joincond_trim_constraints
#     raise exc.AmbiguousForeignKeysError(
# sqlalchemy.exc.AmbiguousForeignKeysError: Can't determine join between 'pairings' and 'players'; tables have more than one foreign key constraint relationship between them. Please specify the 'onclause' of this join explicitly.

# The above exception was the direct cause of the following exception:

# Traceback (most recent call last):
#   File "/var/task/flask/app.py", line 1463, in wsgi_app
#     response = self.full_dispatch_request()
#   File "/var/task/flask/app.py", line 872, in full_dispatch_request
#     rv = self.handle_user_exception(e)
#   File "/var/task/flask/app.py", line 870, in full_dispatch_request
#     rv = self.dispatch_request()
#   File "/var/task/flask/app.py", line 855, in dispatch_request
#     return self.ensure_sync(self.view_functions[rule.endpoint])(**view_args)  # type: ignore[no-any-return]
#   File "./__init__.py", line 66, in test
#     admins = Admins.query.all()
#   File "/var/task/flask_sqlalchemy/model.py", line 22, in __get__
#     return cls.query_class(
#   File "/var/task/sqlalchemy/orm/query.py", line 275, in __init__
#     self._set_entities(entities)
#   File "/var/task/sqlalchemy/orm/query.py", line 287, in _set_entities
#     self._raw_columns = [
#   File "/var/task/sqlalchemy/orm/query.py", line 288, in <listcomp>
#     coercions.expect(
#   File "/var/task/sqlalchemy/sql/coercions.py", line 389, in expect
#     insp._post_inspect
#   File "/var/task/sqlalchemy/util/langhelpers.py", line 1252, in __get__
#     obj.__dict__[self.__name__] = result = self.fget(obj)
#   File "/var/task/sqlalchemy/orm/mapper.py", line 2711, in _post_inspect
#     self._check_configure()
#   File "/var/task/sqlalchemy/orm/mapper.py", line 2388, in _check_configure
#     _configure_registries({self.registry}, cascade=True)
#   File "/var/task/sqlalchemy/orm/mapper.py", line 4203, in _configure_registries
#     _do_configure_registries(registries, cascade)
#   File "/var/task/sqlalchemy/orm/mapper.py", line 4244, in _do_configure_registries
#     mapper._post_configure_properties()
#   File "/var/task/sqlalchemy/orm/mapper.py", line 2405, in _post_configure_properties
#     prop.init()
#   File "/var/task/sqlalchemy/orm/interfaces.py", line 579, in init
#     self.do_init()
#   File "/var/task/sqlalchemy/orm/relationships.py", line 1644, in do_init
#     self._setup_join_conditions()
#   File "/var/task/sqlalchemy/orm/relationships.py", line 1886, in _setup_join_conditions
#     self._join_condition = jc = JoinCondition(
#   File "/var/task/sqlalchemy/orm/relationships.py", line 2312, in __init__
#     self._determine_joins()
#   File "/var/task/sqlalchemy/orm/relationships.py", line 2469, in _determine_joins
#     raise sa_exc.AmbiguousForeignKeysError(
# sqlalchemy.exc.AmbiguousForeignKeysError: Could not determine join condition 
# between parent/child tables on relationship Pairings.assassin_ - 
# there are multiple foreign key paths linking the tables.  
# Specify the 'foreign_keys' argument, providing a list of those columns
# which should be counted as containing a foreign key reference to the parent table.
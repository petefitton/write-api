from models import app, User, Script
from flask import jsonify, request
from crud.user_crud import get_all_users, get_user, create_user, destroy_user, update_user
from crud.script_crud import get_all_scripts, get_one_script, create_script, update_script, delete_script

@app.route('/')
def home():
  first_user = User.query.first()
  print(f'🎀 {first_user}')
  return jsonify(user=first_user.as_dict() if first_user else 'No users!')

# Helper function
@app.errorhandler(Exception)
def unhandled_exception(e):
  app.logger.error('Unhandled Exception: %s', (e))
  message_str = e.__str__()
  return jsonify(message=message_str.split(':')[0])


@app.route('/scripts', methods=["GET", "POST"])
def create_or_get_all_scripts():
  if request.method == "GET":
    return get_all_scripts()
  if request.method == "POST":
    return create_script(request.form['filename'], request.form['content'], request.form['author_id'])


@app.route('/scripts/<int:id>', methods=["GET", "PUT", "DELETE"])
def show_update_delete_script(id):
  if request.method == "GET":
    return get_one_script(id)
  if request.method == "PUT":
    return update_script(
      id=id, 
      filename=request.form['filename'],
      content=request.form['content']
    )
  if request.method == "DELETE":
    return delete_script(id)

@app.route('/users', methods=['GET', 'POST'])
def user_index_create():
  if request.method == 'GET':
    return get_all_users()
  if request.method == 'POST':
    return create_user(request.form['name'], request.form['email'], request.form['bio'])


@app.route('/users/<int:id>', methods=['GET', 'PUT', 'DELETE'])
def user_show_update_delete(id):
  if request.method == 'GET':
    return get_user(id)
  if request.method == 'PUT':
    return update_user(
      id=id, 
      name=request.form['name'],
      email=request.form['email'],
      bio=request.form['bio']
    )
  if request.method == 'DELETE':
    return destroy_user(id)
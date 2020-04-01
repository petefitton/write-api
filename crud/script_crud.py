from flask import jsonify, redirect
from models import db, Script, User

# Index
def get_all_scripts():
  all_scripts = Script.query.all()
  if len(all_scripts) > 0:
    results = [script.as_dict() for script in all_scripts]
  else:
    results = []
  return jsonify(results)

# Show
def get_one_script(id):
  script = Script.query.get(id)
  if script:
    return jsonify(script.as_dict())
  else:
    raise Exception('No Script at id {}'.format(id))

# author_id may throw an error here
# Create
def create_script(filename, content, author_id):
  new_script = Script(filename=filename, content=content, author_id=author_id or None)
  db.session.add(new_script)
  db.session.commit()
  return jsonify(new_script.as_dict())

# Update function!
def update_script(id, filename, content):
  script = Script.query.get(id)
  if script:
    script.content = content or script.content
    script.filename = filename or script.filename
    db.session.commit()
    return jsonify(script.as_dict())
  else:
    raise Exception('No Script at id {}'.format(id))

# Destroy
def delete_script(id):
  script = Script.query.get(id)
  if script:
    db.session.delete(script)
    db.session.commit()
    return redirect('/scripts')
  else:
    raise Exception('No Script at id {}'.format(id))
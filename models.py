from flask import Flask
from flask_sqlalchemy import SQLAlchemy

app=Flask(__name__)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['SQLALCHEMY_ECHO'] = True
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://localhost/write_api'
db = SQLAlchemy(app)

class User(db.Model):
  __tablename__ = 'users'

  id = db.Column(db.Integer, primary_key=True)
  email = db.Column(db.String, unique=True, nullable=False)
  name = db.Column(db.String, nullable=False)
  bio = db.Column(db.String(125))

  # relationship
  scripts = db.relationship('Script', backref='author', lazy=True)

  def __repr__(self):
    return f'User(id={self.id}, email="{self.email}", name="{self.name}", bio="{self.bio}")'

  def as_dict(self):
    return {c.name: getattr(self, c.name) for c in self.__table__.columns}

# Script Model
class Script(db.Model):
  __tablename__ = 'scripts'

  id = db.Column(db.Integer, primary_key=True)
  filename = db.Column(db.String(150), unique=True, nullable=False)
  content = db.Column(db.String, nullable=False)
  author_id = db.Column(db.Integer, db.ForeignKey('users.id', ondelete='SET NULL'))

  # relationship not needed here because of use of backref above

  def __repr__(self):
    return f'Script(id={self.id}, filename="{self.filename}", content="{self.filename}")'

  def as_dict(self):
    return {
      'id': self.id,
      'filename': self.filename,
      'content': self.content,
      'author': self.author.as_dict()['name'],
    }

# possible get or create method
from flask import Flask, request, redirect
from flask import render_template
from flask_sqlalchemy import SQLAlchemy

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///simple-web-notes.db'
db = SQLAlchemy(app)

class Note(db.Model):
  id = db.Column(db.Integer, primary_key=True)
  title = db.Column(db.String(100))
  content = db.Column(db.Text)

  def __repr__(self):
    return '<Note %r>' % self.id


@app.route('/')
def index():
  return render_template('index.html')

@app.route('/create-note', methods=['GET', 'POST'])
def create_note():
  if request.method == 'POST':
    title = request.form['title']
    content = request.form['content']

    note = Note(title=title, content=content)

    try:
      db.session.add(note)
      db.session.commit()
      return redirect('/')
    except:
      return "При добавлении статьи произошла ошибка"
  else:
    return render_template('create-note.html')


@app.route('/notes')
def notes():
  notes = Note.query.order_by(Note.id.desc()).all()
  return render_template('notes.html', notes=notes)

if __name__ == '__main__':
  app.run(debug=True)
"""A sample program for flask"""
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from flask import Flask, render_template, request, redirect

app = Flask(__name__)
app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///todo.db"
db = SQLAlchemy(app)

class Todo(db.Model):
    """Todo class"""
    sno = db.Column(db.Integer, primary_key = True)
    title = db.Column(db.String(200), nullable = False)
    description = db.Column(db.String(500), nullable = False)
    time = db.Column(db.DateTime, default = datetime.utcnow)

    def __repr__(self) -> str :
        return f"{self.sno} - {self.title}"

@app.route('/', methods=['GET','POST'])
def hello_world():
    """A simple hello world function"""
    if request.method == 'POST':
        todo_title = request.form['title']
        todo_desc = request.form['desc']
        data = Todo(title=todo_title, description=todo_desc)
        db.session.add(data)
        db.session.commit()
    alltodo = Todo.query.all()
    return render_template('index.html',alltodo=alltodo)

@app.route('/update/',methods=['GET','POST'])
def update():
    """Function to update todo's"""
    if request.method == 'POST':
        sno = request.form['update']
        data = Todo.query.filter_by(sno=sno).first()
    return render_template('update.html', todo=data)

@app.route('/upgrade/',methods=['GET','POST'])
def upgrade():
    """Function to change todo's post"""
    if request.method == 'POST':
        sno = request.form['update']
        todo = Todo.query.filter_by(sno=sno).first()
        todo.title = request.form['title']
        todo.description = request.form['desc']
        db.session.commit()
        return redirect("/")

@app.route('/delete/', methods=['GET','POST'])
def delete():
    """Function to delete a todo"""
    if request.method == 'POST':
        sno = request.form['delete']
        todo = Todo.query.filter_by(sno=sno).first()
        db.session.delete(todo)
        db.session.commit()
        return redirect("/")

@app.route('/show')
def show():
    "Function to delete a todo"
    alltodo = Todo.query.all()
    print(alltodo)
    return 'this is to return the data from database'

if __name__ == '__main__':
    app.run(debug = True)

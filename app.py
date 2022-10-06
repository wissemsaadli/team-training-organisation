# importing flask and a template render

from crypt import methods
from flask import Flask, redirect , render_template, request
# importing data base
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import DateTime, func
app = Flask(__name__)
# initializing a database
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'

db=SQLAlchemy(app)
app.app_context().push()
# importing date time
import datetime


class ToDo(db.Model):
    id=db.Column(db.Integer, primary_key=True)
    content=db.Column(db.String(20), nullable=False)
    time_created = db.Column(DateTime(timezone=True), server_default=func.now())

    def __rep__(self):
        return '<Task %r>' %self.id


@app.route('/',methods=['POST','GET'])
def index():
    if(request.method=='POST'):
        task_content=request.form['content']
        new_task= ToDo(content=task_content)
        try:
            db.session.add(new_task)
            db.session.commit()
            return redirect('/')
        except:
            return 'there was an issue adding the task'
    else:
        tasks = ToDo.query.order_by(ToDo.time_created).all()
        return render_template("index.html",tasks=tasks)

# routing an function to delete a task
@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete=ToDo.query.get_or_404(id)
    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/')
    except:
        return 'could not delete task'

# routing and function to update a task

@app.route('/update/<int:id>', methods=['GET','POST'])
def update(id):
    uptask=ToDo.query.get_or_404(id)
    if request.method=='POST':
        uptask.content=request.form['content']
        try:
            db.session.commit()
            return redirect('/')
        except:
            return 'issue updating task'
    else:
        return render_template('/update.html',task=uptask)
if __name__ == "__main__ ":
    app.run(debug= True)
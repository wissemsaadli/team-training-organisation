# importing flask and a template render

from flask import Flask , render_template
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

        
@app.route('/')
def index():
    return render_template("index.html")
if __name__ == "__main__ ":
    app.run(debug= True) 
from flask import Flask,render_template,url_for,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime

app=Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI']='sqlite:///test.db'
db=SQLAlchemy(app)

class Todo(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    content= db.Column(db.String(200),nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)


    def __repr__(self):
        return '<Task %r>' % self.id

class Shop(db.Model):
    id= db.Column(db.Integer,primary_key=True)
    product=db.Column(db.String(200),nullable=False)
    price=db.Column(db.Integer,nullable=False)
    stock=db.Column(db.Integer,nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return '<The product %r is added>' % self.product


@app.route('/grocery',methods=['POST','GET'])
def index():
    if request.method =='POST':
         task_content1=request.form['a']
         task_content2=request.form['b']
         task_content3=request.form['c']
         task_content4=request.form['d']

         new_task=Shop(id=task_content1,product=task_content2,stock=task_content3,price=task_content4)
         print(new_task.__repr__())

         try:
             db.session.add(new_task)
             
             db.session.commit()
             return redirect('/grocery')
            
         except:
             return 'There was an issue adding your task'
        
        
        
    else:
        tasks = Shop.query.order_by(Shop.date_created).all()
        return render_template('index.html', tasks=tasks)


@app.route('/delete/<int:id>')
def delete(id):
    task_to_delete= Shop.query.get_or_404(id)

    try:
        db.session.delete(task_to_delete)
        db.session.commit()
        return redirect('/grocery')
    except:
        return "There was problem deleting that task"

@app.route('/grocery/update/<int:id>',methods=['GET','POST'])
def update(id):
    task = Shop.query.get_or_404(id)

    if request.method == 'POST':
        task.id = request.form['a']
        task.product = request.form['b']
        task.stock = request.form['c']
        task.price = request.form['d']

        try:
            db.session.commit()
            return redirect('/grocery')
        except:
            return 'There was an error updating your task  '

    else:
        return render_template('update.html', task=task)


if __name__=="__main__":
    app.run(debug=True)
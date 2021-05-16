from flask import Flask, render_template, request, redirect, json
from flask_sqlalchemy import SQLAlchemy
from flask_mail import Mail, Message

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///students.db"
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

app.config['MAIL_SERVER']='smtp.gmail.com'
app.config['MAIL_PORT'] = 465
app.config['MAIL_USERNAME'] = 'akshayvutukuru@gmail.com'
app.config['MAIL_PASSWORD'] = '***********'
app.config['MAIL_USE_TLS'] = False
app.config['MAIL_USE_SSL'] = True

mail = Mail(app)
db = SQLAlchemy(app)

class Students(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(50), nullable=False)
    age = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), nullable=False)

    def __repr__(self) -> str:
        return f"{self.id}, {self.name}"
    def get_obj(self):
        body = {
            "id": self.id,
            "name": self.name,
            "age": self.age,
            "email": self.email,
        }
        return body

@app.route('/', methods=['GET', 'POST'])
def add_students():
    if request.method=='POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        student = Students(name=name, age=age, email=email)
        db.session.add(student)
        db.session.commit()
        
    allStudents = Students.query.all()
    return render_template('index.html', allStudents=allStudents)

@app.route('/students')
def students_record():
    allStudents = Students.query.all()
    return render_template('students.html', allStudents=allStudents)
    

@app.route('/student/<int:id>')
def student_details(id):
    student = Students.query.filter_by(id=id).first()
    return render_template('student.html', student=student)

@app.route('/update/<int:id>', methods=['GET', 'POST'])
def update(id):
    if request.method=='POST':
        name = request.form['name']
        age = request.form['age']
        email = request.form['email']
        students = Students.query.filter_by(id=id).first()
        students.name = name
        students.age = age
        students.email = email
        db.session.add(students)
        db.session.commit()
        return redirect("/")
        
    student = Students.query.filter_by(id=id).first()
    return render_template('update.html', student=student)

@app.route('/delete/<int:id>')
def delete(id):
    student = Students.query.filter_by(id=id).first()
    db.session.delete(student)
    db.session.commit()
    return redirect("/")

@app.route("/send-mail")
def index():
   msg = Message(
                'Hello',
                sender ='akshayvutukuru@gmail.com',
                recipients = ['akshayvutukuru@gmail.com']
               )
   msg.body = 'Hello Flask message sent from Flask-Mail'
   mail.send(msg)
   return 'Email Sent'

if __name__ == "__main__":
    app.run(debug=True)
from flask import Flask, render_template,request,redirect
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import smtplib 
app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = "sqlite:///Calorie_given.db"
app.config['SQLALCHEMY_BINDS'] = {"one":"sqlite:///Daily_cal.db",
                                    "two":"sqlite:///Progress_cal.db"}

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class Calorie_given(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)
    rate = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.product} - {self.rate} - {self.date_created}"          #method used to obtain specific objects from  database

class Daily_cal(db.Model):
    __bind_key__='one'
    srno = db.Column(db.Integer, primary_key=True)
    product = db.Column(db.String(200), nullable=False)
    rate = db.Column(db.String(500), nullable=False)
    qty = db.Column(db.String(500), nullable=False)
    amount = db.Column(db.String(500), nullable=False)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self) -> str:
        return f"{self.product} - {self.rate} - {self.date_created}" 

@app.route('/' , methods=['GET','POST'])
def hello():
    if request.method=="POST":
    
        product = request.form['product']
        rate = request.form['rate']
        calorie_cal = Calorie_given(product=product,rate=rate)
        db.session.add(calorie_cal)
        db.session.commit()
   
        return redirect("/")

    all_calorie_cal= Calorie_given.query.all()
    return render_template('index.html', all_calorie_cal = all_calorie_cal)


@app.route('/daily_rep' , methods=['GET','POST'])
def daily():
   if request.method =='POST': 
    
     product1 = request.form['product']
     qty= request.form['qty']
     p = Calorie_given.query.filter_by(product=str(product1)).first()
     amount = int(qty) * int(p.rate)
     Daiy_Cal= Daily_cal(product=product1,rate=p.rate,qty=qty,amount=amount)
     db.session.add(Daiy_Cal)
     db.session.commit()
     return redirect("/")

   return render_template('index.html', product1=product1)

@app.route('/calories', methods=['GET','POST'])
def calories():
    if request.method=="POST":
        datee=request.form['pro_date']
        dateee=Daily_cal.query.filter_by(str(datee)).all()
    # dat=Daily_cal.query.filter_by(date_created="date_created").all()
    daily_rep = Calorie_given.query.all()
    return render_template("calories.html",daily_rep=daily_rep)


@app.route('/update/<int:id>',methods=['GET','POST'])
def update(id):
  if request.method == "POST":
    product = request.form['product']
    rate = request.form['rate']
    upd_cal = Calorie_given.query.filter_by(id=id).first()
    upd_cal.product = product
    upd_cal.rate = rate
    db.session.add(upd_cal)
    db.session.commit()

    return redirect("/calories")
  upd_cal = Calorie_given.query.filter_by(id=id).first()
  return render_template("update.html" , upd_cal =upd_cal)

@app.route('/delete/<int:id>')
def delete(id):
    del_cal = Calorie_given.query.filter_by(id=id).first()
    db.session.delete(del_cal)
    db.session.commit()
    return redirect("/calories")


if __name__ =="__main__":
    # server = smtplib.SMTP('smtp.gmail.com', 587)
    # server.ehlo()
    # server.starttls()
    # server.login('forms.developers.ramson@gmail.com', 'aman118@frd')
    # server.sendmail('forms.developers.ramson@gmail.com', "developers.ramson@gmail.com", "Someone open your Calorie caluclator!!")
    # server.close()

    app.run(debug=True , port=8000)
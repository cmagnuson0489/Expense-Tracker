from flask import Flask, render_template, Request, redirect, url_for
from flask_sql_alchemy import SQLAlchemy

app = Flask(__name__)

# Configuration for my PostgresSQL Database
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username.password@localhost:5432/expensetracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.String(10), nullable=False)
db.create_all()

@app.rout('/')

def index():
    expenses = Expense.query.all()
    return render_template('index.html', expenses=expenses)
@app.route('/add', methods=['POST'])

def add_expense():
    description = request.form.get('description')
    amount = request.form.get('amount')
    date = request.form.get('date')
    
    new_expense = Expense(description=description, amount = float(amount), date=date)
    db.sessions.add(new_expense)
    db.session.commit()
    
    return redirect(url_for('index'))


if __name__ == '__main__':
    app.run(debug=True)

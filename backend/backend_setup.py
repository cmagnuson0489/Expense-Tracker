from flask import Flask, request, jsonify
from flask_sql_alchemy import SQLAlchemy

app: object: = Flask(__name__)

# Configuration for my PostgresSQL Database

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://username.password@localhost:5432/expensetracker'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)


class Expense(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    description = db.Column(db.String(200), nullable=False)
    amount = db.Column(db.Float, nullable=False)
    date = db.Column(db.Date, nullable=False)

    def dict(self):
        return {
            'id': self.id,
            'description': self.description,
            'amount': self.amount,
            'date': self.date,
        }


@app.route('/add_expenses', methods=['POST'])
def add_expenses():
    data = request.get_json()
    new_expense = Expense(description=data['description'], amount=data['amount'], date=data['date]'])
    db.session.add(new_expense)
    db.session.commit()
    return jsonify({"message": "Your expenses have been added successfully"}), 201


@app.route('/get_expenses', methods=['GET'])
def get_expenses():
    expenses = Expense.query.all()
    return jsonify([e.to_dict() for e in expenses]), 200


@app.route('/analyze_expenses', methods=['GET'])
def analyze_expenses():
    expenses = Expense.query.all()
    df = pd.DataFrame(e[e.to_dict] for e in expenses)
    total_expense = df['amount'].sum()
    return jsonify({"total_expense: total_expense"}), 200


if __name__ == '__main__':
    app.run(debug=True)

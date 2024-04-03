from flask import Flask, request, jsonify, render_template, session, redirect, url_for
from werkzeug.security import generate_password_hash, check_password_hash
from flask_sqlalchemy import SQLAlchemy
from mysql.connector import connect, Error

app = Flask(__name__)
app.secret_key = 'type_something_random_for_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///users.db'
db = SQLAlchemy(app)

class User(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(128), nullable=False)



@app.route('/')
def hello_world():
    return render_template("home.html")

@app.route('/register')
def register():
    return render_template("register.html")

@app.route('/register_data', methods=['POST'])
def register_data():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        hashed_password = generate_password_hash(password)
        new_user = User(username=username, password_hash=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        return redirect(url_for('login'))
    return render_template('register.html')

@app.route('/login')
def login():
    return render_template('login.html')

@app.route('/login_data', methods=['POST'])
def login_data():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        user = User.query.filter_by(username=username).first()
        if user and check_password_hash(user.password_hash, password):
            session['username'] = username
            return redirect(url_for('index'))
        else:
            return render_template('login.html', message='Invalid username or password')
    return render_template('index.html')

@app.route('/index')
def index():
    return render_template('index.html')


@app.route('/submitData', methods=['POST'])
def submit_data():
        
    try:
        expenses = request.form['expenses']
        profit = request.form['profit']
        with connect(
            host="host",
            user="user",
            password="password",
            database = "database"
        ) as connection:
            insert_table_query = """
    INSERT INTO shop_data (expenses, profit) VALUES (%s, %s)

    """
            data = (expenses, profit)
            with connection.cursor() as cursor:
                cursor.execute(insert_table_query,data)
                connection.commit()
    except Error as e:
        print(e)
    
    

    return jsonify({'message': 'Data inserted successfully'})

@app.route('/getData', methods=['GET'])
def get_data():
        
    try:
       
        with connect(
            host="host",
            user="user",
            password="password",
            database = "database"
        ) as connection:
            display_table_query = """
    SELECT * FROM shop_data

    """
            
            with connection.cursor() as cursor:
                cursor.execute(display_table_query)
                data = cursor.fetchall()
                print(data)
    except Error as e:
        print(e)
    return jsonify({'data': data})

def ml_model():
    #your ml code goes here
    #you can pass the 'data' fetched from the above table as an input argument by defining parameters in the declaration
    pass

if __name__ == '__main__':
    app.run(debug=True)

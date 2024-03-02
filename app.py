from flask import Flask, render_template, session, request, redirect, jsonify,url_for
from pymongo import MongoClient

app = Flask(__name__)
app.secret_key = "asdfghjkl"  # Set your secret key here


client = MongoClient("mongodb+srv://Admin:admin@cluster0.itmtb0r.mongodb.net/?retryWrites=true&w=majority&appName=Cluster0")
db = client['MyDatabase']  # Change 'MyDatabase' to your actual database name
users_collection = db['users']  # Change 'users' to your actual collection name

@app.route("/login", methods=['POST'])
def login():
    email = request.form['email']
    password = request.form['pass']

    user = users_collection.find_one({'email': email})
    if user and user['pass'] == password:
        session['user'] = user['email']
        return redirect(url_for('dashboard'))
    else:
        return jsonify({'error': 'Invalid email or password'})

@app.route("/dashboard")
def dashboard():
    if 'user' in session:
        return 'Welcome to the dashboard, {}'.format(session['user'])
    else:
        return redirect(url_for('home'))

@app.route("/register", methods=['POST'])
def create_user():
    new_user = {
        'name': request.json['name'],
        'email': request.json['email'],
        'pass': request.json['pass']
    }
    
    result = users_collection.insert_one(new_user)
    return jsonify({'id': str(result.inserted_id), 'msg': 'User created'})


@app.route("/users")
def get_users():
    users = []
    for user in users_collection.find():
        users.append({
            'id': str(user['_id']),
            'name': user['name'],
            'email': user['email'],
            'pass':user['pass']
            # Assuming your password field is named 'pass'
        })
    return jsonify(users)
    
@app.route("/")
def home():
    return render_template('home.html')


if __name__ == '__main__':
    app.run(debug=True)

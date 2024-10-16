from flask import Flask, render_template, request, redirect, url_for
import mysql.connector

# Initialize Flask app
app = Flask(__name__)

def get_db_connection():
    connection = mysql.connector.connect(
        host='your_db_host',
        user='your_db_user',
        password='your_db_password',
        database='your_db_name' )
    return connection

# Home page route
@app.route('/')
def home():
    return render_template('index.html')

@app.route('/create_profile', methods=['POST'])
def create_profile():
    # Get form data
    name = request.form['name']
    age = request.form['age']
    bio = request.form['bio']
    interests = request.form['interests']
    
    # Insert into MySQL
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("INSERT INTO elders (name, age, bio, interests) VALUES (%s, %s, %s, %s)",
                   (name, age, bio, interests))
    connection.commit()
    cursor.close()
    connection.close()
    
    return redirect(url_for('show_profiles'))

@app.route('/show_profiles')
def show_profiles():
    connection = get_db_connection()
    cursor = connection.cursor()
    cursor.execute("SELECT * FROM elders")
    elders = cursor.fetchall()
    cursor.close()
    connection.close()
    return render_template('profiles.html', elders=elders)

# Sign Up page route
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    if request.method == 'POST':
        name = request.form['name']
        email = request.form['email']
        phone = request.form['phone']

        # Create a new elder entry
        new_elder = Elder(name=name, email=email, phone=phone)
        db.session.add(new_elder)
        db.session.commit()

        return redirect(url_for('home'))  # Redirect back to home after successful signup
    return render_template('signup.html')

# About Us page route
@app.route('/about')
def about():
    return render_template('about.html')

if __name__ == '__main__':
    app.run(debug=True)

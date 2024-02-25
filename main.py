import gc
import MySQLdb
import gspread
from flask import Flask, render_template, request, redirect, url_for, session
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# For simplicity, hardcode admin credentials (replace with secure storage in production)
admin_credentials = {'admin1': 'password123', 'admin2': 'securepass'}

class AdminLoginForm(FlaskForm):
    username = StringField('Username', validators=[DataRequired()])
    password = PasswordField('Password', validators=[DataRequired()])
    submit = SubmitField('Login')

@app.route('/')
def index():
    return render_template('index.html')

@app.route('/submit', methods=['POST'])
def submit():
    # Handle form submission logic here
    # You can access form data using request.form['fieldname']
    return redirect(url_for('index'))

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/admin-login', methods=['GET', 'POST'])
def admin_login():
    form = AdminLoginForm()

    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data

        # Check admin credentials in the database
        cur = MySQLdb.connection.cursor()
        cur.execute("SELECT * FROM admin WHERE username=%s AND password=%s", (username, password))
        admin = cur.fetchone()
        cur.close()

        if admin:
            session['admin_logged_in'] = True
            return redirect(url_for('admin_dashboard'))

    return render_template('admin_login.html', form=form)

@app.route('/admin-dashboard')
def admin_dashboard():
    if 'admin_logged_in' not in session or not session['admin_logged_in']:
        return redirect(url_for('admin_login'))

    # Add logic to render the admin dashboard
    return render_template('admin_dashboard.html')

if __name__ == '__main__':
    app.run(debug=True)

@app.route('/logout')
def logout():
    session.pop('admin_logged_in', None)
    return redirect(url_for('index'))

sheet = gc.open('https://forms.gle/T7JPNW3N85xP6n49A').sheet1
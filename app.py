from flask import Flask, render_template, request, redirect, url_for
from flask_login import LoginManager, UserMixin, login_user, logout_user, login_required
import os, pandas as pd
app = Flask(__name__)
app.config['SECRET_KEY'] = 'MyNewSecretKey'

# create a user class
class User(UserMixin):
    def __init__(self, id):
        self.id = id

# set up login manager
login_manager = LoginManager()
login_manager.init_app(app)

# create a dummy user for testing purposes
users = {'admin': {'password': 'admin'}}

# set up user loader function
@login_manager.user_loader
def load_user(user_id):
    return User(user_id)

# set up login page
@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        if username in users and password == users[username]['password']:
            user = User(username)
            login_user(user)
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html', error='Invalid username or password')
    else:
        return render_template('login.html')


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # Get uploaded file
        file = request.files['file']

        # Check if file is CSV or XLSX
        if file.filename.endswith('.csv'):
            f = request.files['file']
            f.save('one/'+ f.filename)
            return render_template('login.html', message='successful')
        elif file.filename.endswith('.xlsx'):
            f = request.files['file']
            f.save('one/'+f.filename)
            return render_template('login.html', message='successful!')
        else:
            return render_template('index.html', message='Invalid file type!')
        # Return success message
        return render_template('index.html', message='File uploaded successfully!')
    else:
        return render_template('index.html')
# Define a route to render the file list template
@app.route('/dashboard')
@login_required
def dashboard():
    # Get the list of files in the folder
    files = os.listdir('E:\code\one')
    # Pass the list of files to the template
    return render_template('admin.html', files=files)
@app.route('/download/<path:file_path>')
def download(file_path):
    # Construct the full path to the file
    full_path = os.path.join('E:\code\one', file_path)

    # Send the file to the client for download
    return send_file(full_path, as_attachment=True)

# Define a route to open a file
@app.route('/open/<filename>')
def open_file(filename):
    full_path = os.path.join('E:\code\one', filename)
    extension = os.path.splitext(full_path)[1]
    if extension == ".csv":
        data = pd.read_csv(full_path)
        data.to_html("E:\code\\templates\\table.html")
        return render_template('table.html')
    else:
        data = pd.read_excel(full_path)
        table_html =  data.to_html()
        with open('E:\code\\templates\\table.html', 'w', encoding='utf-8') as f:
            f.write(table_html)
        return render_template('table.html', table_html=table_html)
@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('login'))



if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, send_file
import os
import pandas as pd

app = Flask(__name__)

# Create a directory for uploaded files
if not os.path.exists('uploads'):
    os.makedirs('uploads')

# Admin Login Page
@app.route('/admin_login', methods=['GET', 'POST'])
def admin_login():
    if request.method == 'POST':
        if request.form['username'] == 'admin' and request.form['password'] == 'admin':
            return redirect(url_for('admin_panel'))
        else:
            return render_template('admin_login.html', error='Invalid Credentials')
    return render_template('admin_login.html', error=None)

# Admin Panel
@app.route('/admin_panel')
def admin_panel():
    files = []
    for filename in os.listdir('uploads'):
        file_info = {}
        file_info['name'] = filename
        file_info['path'] = 'uploads/' + filename
        files.append(file_info)
    return render_template('admin_panel.html', files=files)

# File Upload
@app.route('/upload', methods=['GET', 'POST'])
def upload():
    if request.method == 'POST':
        file = request.files['file']
        file.save(os.path.join('uploads', file.filename))
        return redirect(url_for('admin_panel'))
    return render_template('upload.html')

# File Download
@app.route('/download/<filename>')
def download(filename):
    return send_file(os.path.join('uploads', filename), as_attachment=True)

# File Open and Render as Table
@app.route('/open/<filename>')
def open_file(filename):
    data = pd.read_csv(os.path.join('uploads', filename)) # assuming csv file
    table = data.to_html(index=False)
    return render_template('table.html', table=table)

if __name__ == '__main__':
    app.run(debug=True)

from flask import Flask, render_template, request, redirect, url_for, session, flash, jsonify
import os
from werkzeug.utils import secure_filename
import json
from datetime import datetime
import random
import string

app = Flask(__name__)
app.secret_key = 'demo_secret_key_for_poc'

# Configuration
UPLOAD_FOLDER = 'uploads'
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'json', 'csv', 'xml'}
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

# Create upload directory if it doesn't exist
os.makedirs(UPLOAD_FOLDER, exist_ok=True)

# Demo credentials (in production, these would be in a database)
DEMO_CREDENTIALS = {
    'shipping_admin': 'secure_pass123',
    'logistics_user': 'logistics_pass456'
}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def generate_confirmation_number():
    """Generate a unique confirmation number"""
    timestamp = datetime.now().strftime('%Y%m%d%H%M%S')
    random_suffix = ''.join(random.choices(string.ascii_uppercase + string.digits, k=4))
    return f"CONF-{timestamp}-{random_suffix}"

@app.route('/')
def index():
    if 'username' in session:
        return redirect(url_for('dashboard'))
    return redirect(url_for('login'))

@app.route('/login', methods=['GET', 'POST'])
def login():
    if request.method == 'POST':
        username = request.form['username']
        password = request.form['password']
        
        if username in DEMO_CREDENTIALS and DEMO_CREDENTIALS[username] == password:
            session['username'] = username
            flash('Login successful!', 'success')
            return redirect(url_for('dashboard'))
        else:
            flash('Invalid username or password', 'error')
    
    return render_template('login.html')

@app.route('/dashboard')
def dashboard():
    if 'username' not in session:
        return redirect(url_for('login'))
    return render_template('dashboard.html', username=session['username'])

@app.route('/shipment_form', methods=['GET', 'POST'])
def shipment_form():
    if 'username' not in session:
        return redirect(url_for('login'))
    
    if request.method == 'POST':
        # Generate confirmation number
        confirmation_number = generate_confirmation_number()
        
        # Handle form submission
        form_data = {
            'confirmation_number': confirmation_number,
            'status': 'Submitted',
            'shipper_name': request.form.get('shipper_name'),
            'shipper_address': request.form.get('shipper_address'),
            'recipient_name': request.form.get('recipient_name'),
            'recipient_address': request.form.get('recipient_address'),
            'package_weight': request.form.get('package_weight'),
            'package_dimensions': request.form.get('package_dimensions'),
            'shipping_date': request.form.get('shipping_date'),
            'tracking_number': request.form.get('tracking_number'),
            'special_instructions': request.form.get('special_instructions'),
            'submitted_by': session['username'],
            'submitted_at': datetime.now().isoformat()
        }
        
        # Handle file upload
        uploaded_file = None
        if 'shipment_document' in request.files:
            file = request.files['shipment_document']
            if file and file.filename != '' and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                timestamp = datetime.now().strftime('%Y%m%d_%H%M%S')
                filename = f"{timestamp}_{filename}"
                filepath = os.path.join(app.config['UPLOAD_FOLDER'], filename)
                file.save(filepath)
                uploaded_file = filename
                form_data['uploaded_file'] = filename
        
        # Save submission data
        submission_file = f"submissions/{datetime.now().strftime('%Y%m%d_%H%M%S')}_submission.json"
        os.makedirs('submissions', exist_ok=True)
        with open(submission_file, 'w') as f:
            json.dump(form_data, f, indent=2)
        
        flash('Shipment form submitted successfully!', 'success')
        return render_template('submission_success.html', form_data=form_data)
    
    return render_template('shipment_form.html')

@app.route('/logout')
def logout():
    session.clear()
    flash('You have been logged out', 'info')
    return redirect(url_for('login'))

@app.route('/api/health')
def health_check():
    return jsonify({'status': 'healthy', 'timestamp': datetime.now().isoformat()})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000, debug=True) 
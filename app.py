import os
import shutil
from flask import Flask, request, render_template, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy

# Flask app initialization
app = Flask(__name__)

# Define paths
BASE_DIR = os.path.dirname(os.path.abspath(__file__))
DB_SOURCE = os.path.join(BASE_DIR, "data.db")  # Read-only database in project folder
DB_TMP = "/tmp/data.db"  # Writable database in /tmp/

# If no database exists in /tmp/, copy one from DB_SOURCE if available.
if not os.path.exists(DB_TMP):
    if os.path.exists(DB_SOURCE):
        shutil.copy(DB_SOURCE, DB_TMP)  # Copy existing DB
    # Otherwise, do nothing and let SQLite create the file

# Use /tmp/ as the active database
app.config['SQLALCHEMY_DATABASE_URI'] = f"sqlite:///{DB_TMP}"

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# Define the Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    company_name = db.Column(db.String(30))
    service_type = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    file_path = db.Column(db.String(300))  # Store file path for uploaded files
    message = db.Column(db.String(2000), nullable=False)

# Create Database
with app.app_context():
    print("🚀 Running db.create_all()...")
    db.create_all()
    print("✅ Database tables should now be created!")

# Ensure `/tmp/uploads/` exists for storing files
UPLOAD_FOLDER = "/tmp/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Use writable upload path

# Debugging: Print paths on startup
print(f"🚀 Database Location: {DB_TMP}")
print(f"🚀 Uploads Folder: {UPLOAD_FOLDER}")

# Context processor to put default values for render_template
@app.context_processor
def defaults():
    return {
        "success": False,
        "name": "",
        "company_name": "",
        "service_type": "",
        "email": "",
        "message": "",
        "id": 0,
        "key": "-CeJwZMGPM4E6Nfeb"
    }

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# Contact route
@app.route('/contact')
def contact():
    return render_template('contact.html')

# Portfolio route
@app.route('/portfolio')
def portfolio():
    return render_template('past_work.html')

# Serve uploaded files
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Submit form route
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        name = request.form.get('name')
        company_name = request.form.get('company_name')
        service_type = request.form.get('service_type')
        email = request.form.get('email')
        file = request.files.get('file')  # Handle file upload
        message = request.form.get('message')

        print("🚀 Received Form Data:", name, company_name, service_type, email, message)

        # Save file if uploaded (store in `/tmp/uploads/`)
        file_path = None
        if file and file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)  # Save file in writable directory
            print(f"📁 File saved at: {file_path}")

        # Save customer info to the database
        customer = Customer(name=name, company_name=company_name,
                            service_type=service_type, email=email,
                            file_path=file_path, message=message)
        db.session.add(customer)
        db.session.commit()

        print("✅ New customer added to DB:", customer.id)

        return render_template('contact.html', success=True,
            name=name, company_name=company_name, service_type=service_type,
            email=email, message=message, id=customer.id)
    except Exception as e:
        db.session.rollback()  # Rollback on error
        print(f"❌ Error: {e}")
        return render_template('contact.html', success=False, error=str(e))

# Run the app
if __name__ == '__main__':
    app.run(debug=False)

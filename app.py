import os
import shutil
from flask import Flask, request, render_template, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Define database paths
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
ORIGINAL_DB_PATH = os.path.join(BASE_DIR, "data.db")  # Read-only database
TMP_DB_PATH = "/tmp/data.db"  # ✅ Writable database location

# Ensure the database exists in /tmp/
if os.path.exists(ORIGINAL_DB_PATH) and not os.path.exists(TMP_DB_PATH):
    shutil.copy(ORIGINAL_DB_PATH, TMP_DB_PATH)  # ✅ Copy DB to writable location

# Configure SQLite database in /tmp/
app.config["SQLALCHEMY_DATABASE_URI"] = f"sqlite:///{TMP_DB_PATH}"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# ✅ Ensure database schema exists
with app.app_context():
    db.create_all()

# Define the Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    company_name = db.Column(db.String(30))
    service_type = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    file_path = db.Column(db.String(300))  # Store file path for uploaded files
    message = db.Column(db.String(2000), nullable=False)

# ✅ Ensure `/tmp/uploads/` exists for storing files
UPLOAD_FOLDER = "/tmp/uploads"
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER  # Use writable upload path

# 🚀 Debugging: Print paths on startup
print(f"🚀 Database Location: {TMP_DB_PATH}")
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

# ✅ Serve uploaded files
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

        # ✅ Save file if uploaded (store in `/tmp/uploads/`)
        file_path = None
        if file and file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            file.save(file_path)  # ✅ Save file in writable directory
            print(f"📁 File saved at: {file_path}")

        # ✅ Save customer info to the database
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

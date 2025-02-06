import os
import shutil
import requests
from flask import Flask, request, render_template, send_from_directory, Response, url_for, session, jsonify
from flask_sqlalchemy import SQLAlchemy

# Flask app initialization
app = Flask(__name__)

# Environment variables
DATABASE_URL = os.environ.get('DATABASE_URL')
DATABASE_URL = DATABASE_URL.replace("postgres://", "postgresql://")
EMAILJS_KEY = os.environ.get('EMAILJS_KEY')
BLOB_TOKEN = os.environ.get('BLOB_READ_WRITE_TOKEN')

app.config['SQLALCHEMY_DATABASE_URI'] = DATABASE_URL
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
BLOB_URL = "https://xoexfhw5cyoavrhg.public.blob.vercel-storage.com"

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


# Debugging: Print paths on startup
print(f"🚀 Database Location: {DATABASE_URL}")


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
    }

# Home route
@app.route('/')
def home():
    return render_template('index.html')

# BLOB KEY
@app.route('/blobtoken')
def blob_token():
    return jsonify({'BLOB_TOKEN': session.get('BLOB_TOKEN', None)})

# EMAILJS_KEY
@app.route('/emailjs')
def emailjs():
    return jsonify({'EMAILJS_KEY': session.get('EMAILJS_KEY', None)})

# Contact route
@app.route('/contact')
def contact():
    session['EMAILJS_KEY'] = EMAILJS_KEY
    session['BLOB_TOKEN'] = BLOB_TOKEN
    return render_template('contact.html')

# Portfolio route
@app.route('/portfolio')
def portfolio():
    return render_template('past_work.html')

# Admin route
@app.route('/admin')
def admin():
    auth = request.authorization
    if auth and auth.username == 'msalk.tr' and auth.password == 'Mminecraft9182$#':
        customers = Customer.query.all()
        customer_list = []
        for customer in customers:
            if customer.file_path:
                customer_list.append({"id": customer.id, "file_path": customer.file_path})
        return render_template('admin.html', customers=customer_list)
    else:
        return Response(
        "Unauthorized. Please provide credentials.", 401,
        {"WWW-Authenticate": 'Basic realm="Login Required"'}
        )

# Submit form route
@app.route('/submit', methods=['POST'])
def submit_form():
    try:
        # Get form data
        name = request.form.get('name')
        company_name = request.form.get('company_name')
        service_type = request.form.get('service_type')
        email = request.form.get('email')
        file_path = request.form.get('file')  # Handle file upload
        message = request.form.get('message')

        print("🚀 Received Form Data:", name, company_name, service_type, email, message, file_path)

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

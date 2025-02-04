import os
import base64
from flask import Flask, request, render_template, redirect, url_for, session, send_from_directory, Response
from flask_sqlalchemy import SQLAlchemy

# Flask app initialization
app = Flask(__name__)
app.secret_key = os.urandom(24)  # Required for session management

# Set up the database path and configuration
BASE_DIR = os.path.abspath(os.path.dirname(__file__))
DATABASE_PATH = os.path.join(BASE_DIR, 'data.db')
app.config['SQLALCHEMY_DATABASE_URI'] = f'sqlite:///{DATABASE_PATH}'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

# Initialize SQLAlchemy
db = SQLAlchemy(app)

# File upload configuration
UPLOAD_FOLDER = os.path.join(BASE_DIR, 'uploads')
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

# Define the Customer model
class Customer(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(30), nullable=False)
    company_name = db.Column(db.String(30))
    service_type = db.Column(db.String(20), nullable=False)
    email = db.Column(db.String(80), nullable=False)
    file_path = db.Column(db.String(300))
    message = db.Column(db.String(2000), nullable=False)

    def __init__(self, name, company_name, service_type, email, file_path, message):
        self.name = name
        self.company_name = company_name
        self.service_type = service_type
        self.email = email
        self.file_path = file_path
        self.message = message
    
# Context processor to put default values for render_template
@app.context_processor
def defaults():
    print("🚀 Context processor running!")
    return {
        "success": False,
        "name": "",
        "company_name": "",
        "service_type": "",
        "email": "",
        "message": "",
        "id": 0
    }

# Ensure database is created
with app.app_context():
    db.create_all()

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

# Download file route
@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

# Admin route
@app.route('/admin')
def admin():
    auth = request.authorization
    if auth and auth.username == 'msalk.tr' and auth.password == 'Mminecraft9182$#':
        customers = Customer.query.all()
        customer_list = []
        for customer in customers:
            if customer.file_path:
                idx = customer.file_path.find('uploads')
                file = '/../' + customer.file_path[idx:]
                customer_list.append({"id": customer.id, "file_path": file})
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
        name = request.form['name']
        company_name = request.form['company_name']
        service_type = request.form['service_type']
        email = request.form['email']
        file = request.files.get('file')  # Handle file upload
        print(file)
        message = request.form['message']

        # Save file if uploaded
        file_path = None
        if file and file.filename != '':
            file_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
            print(file_path)
            file.save(file_path)

        # Save customer info to the database
        customer = Customer(name, company_name, service_type, email, file_path, message)

        db.session.add(customer)
        db.session.commit()

        id = customer.id

        return render_template('contact.html', success=True,
        name=name, company_name=company_name, service_type=service_type,
        email=email, message=message, id=id)
    except Exception as e:
        print(f"Error: {e}")
        return render_template('contact.html', success=False, error=str(e))


# Run the app
if __name__ == '__main__':
    app.run(debug=False)

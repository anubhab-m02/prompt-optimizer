# backend/app.py
from flask import Flask, jsonify,request
from flask_cors import CORS
from flask_jwt_extended import JWTManager
from models import db
from routes.auth import auth_bp
from routes.prompt import prompt_bp
from utils.prompt_optimizer import optimize_prompt_text
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)
CORS(app)

# Configuration
app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv('DATABASE_URI', 'sqlite:///db.sqlite3')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.config['JWT_SECRET_KEY'] = os.getenv('JWT_SECRET_KEY', 'your_jwt_secret_key')

# Initialize extensions
db.init_app(app)
jwt = JWTManager(app)

# Register Blueprints
app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(prompt_bp, url_prefix='/api/prompts')

@app.route('/')
def home():
    return jsonify({"message": "Welcome to the Prompt Optimization API"}), 200

@app.route('/test-optimize', methods=['POST'])
def test_optimize():
    data = request.get_json()
    original_prompt = data.get('prompt', '')
    optimized = optimize_prompt_text(original_prompt)
    return jsonify({"optimized_prompt": optimized}), 200


if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True)

from flask import Flask, jsonify
import os

# CI/CD Pipeline Test - Trigger build
app = Flask(__name__)

@app.route('/')
def hello():
    return jsonify({
        "message": "Hello from AWS ECR!",
        "version": "1.0.0",
        "environment": os.getenv('ENVIRONMENT', 'development')
    })

@app.route('/health')
def health():
    return jsonify({"status": "healthy"})

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=int(os.getenv('PORT', 8080)), debug=True) 
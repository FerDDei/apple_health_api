from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store for demonstration (not recommended for production)
apple_health_data_store = []

@app.route('/', methods=['GET'])
def index():
    return (
        "Welcome to the Apple Health Data API! "
        "POST data to /applehealth and GET from /applehealth"
    ), 200

@app.route('/applehealth', methods=['POST'])
def receive_apple_health_data():
    """
    Receives JSON data from Apple Health export.
    Example: 
    {
        "step_count": 1000,
        "heart_rate": 72,
        "sleep_hours": 7
    }
    """
    data = request.json  # parse the JSON from request body
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    # Store the data in memory (for demonstration)
    apple_health_data_store.append(data)

    return jsonify({"message": "Data received successfully", "data": data}), 201

@app.route('/applehealth', methods=['GET'])
def get_apple_health_data():
    """
    Returns all Apple Health data stored so far in JSON format.
    """
    return jsonify(apple_health_data_store), 200

if __name__ == '__main__':
    # Run the Flask application (development server)
    app.run(host='0.0.0.0', port=5000, debug=True)

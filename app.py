from flask import Flask, request, jsonify

app = Flask(__name__)

# In-memory data store for demonstration (not recommended for production)
apple_health_data_store = []

# Desired metric order
METRICS_ORDER = [
    "active_energy",
    "step_count",
    "apple_exercise_time",
    "dietary_water"
]

def reorder_metrics(data_obj):
    """
    Reorders the 'data.metrics' array in data_obj according to METRICS_ORDER.
    If additional metrics exist, they won't appear in the final list (you can
    modify logic to handle extras if needed).
    """
    # Check if the JSON structure has "data" -> "metrics"
    if "data" in data_obj and isinstance(data_obj["data"], dict):
        original_metrics = data_obj["data"].get("metrics", [])
        
        # Convert the metrics list into a dict keyed by 'name'
        # e.g. {"active_energy": {metricObj}, "step_count": {metricObj}, ...}
        metric_map = {metric["name"]: metric for metric in original_metrics}
        
        # Build a new list of metrics in the desired order
        reordered = []
        for name in METRICS_ORDER:
            if name in metric_map:
                reordered.append(metric_map[name])
        
        # Assign the reordered list back to data_obj
        data_obj["data"]["metrics"] = reordered
    
    return data_obj

@app.route('/', methods=['GET'])
def index():
    return (
        "Welcome to the Apple Health Data API! "
        "POST data to /applehealth, GET from /applehealth, "
        "and DELETE /applehealth to clear stored data."
    ), 200

@app.route('/applehealth', methods=['POST'])
def receive_apple_health_data():
    """
    Receives JSON data from Apple Health export.
    Example: 
    {
        "data": {
            "metrics": [
                {
                    "name": "active_energy",
                    "units": "kcal",
                    "data": [...],
                },
                ...
            ]
        }
    }
    """
    data = request.json  # parse the JSON from request body
    if not data:
        return jsonify({"error": "No JSON data received"}), 400
    
    # Clear the old data (as you do in your code)
    apple_health_data_store.clear()
    
    # Reorder the metrics according to the fixed order
    data = reorder_metrics(data)
    
    # Store the data in memory
    apple_health_data_store.append(data)
    
    return jsonify({"message": "Data received successfully", "data": data}), 201

@app.route('/applehealth', methods=['GET'])
def get_apple_health_data():
    """
    Returns all Apple Health data stored so far in JSON format.
    """
    return jsonify(apple_health_data_store), 200

@app.route('/applehealth', methods=['DELETE'])
def clear_apple_health_data():
    """
    Clears all Apple Health data from the in-memory store.
    """
    apple_health_data_store.clear()
    return jsonify({"message": "All Apple Health data has been cleared."}), 200

if __name__ == '__main__':
    # Run the Flask application (development server)
    app.run(host='0.0.0.0', port=5000, debug=True)

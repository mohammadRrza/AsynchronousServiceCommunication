from flask import Flask, request, jsonify

app = Flask(__name__)


@app.route('/check', methods=['POST'])
def check():
    data = request.json
    driver_token = data.get('driver_token')

    # Simulate different responses based on the driver_token (simple logic)
    if driver_token.startswith("valid"):
        return jsonify({"status": "allowed"})
    elif driver_token.startswith("invalid"):
        return jsonify({"status": "invalid"})
    elif driver_token.startswith("unknown"):
        return jsonify({"status": "unknown"})
    else:
        return jsonify({"status": "not_allowed"})


if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)

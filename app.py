from flask import Flask, request, jsonify # type: ignore
from flask_cors import CORS # type: ignore
from utils.open_ai_service import process_openai_response
from dotenv import load_dotenv # type: ignore
load_dotenv()

app = Flask(__name__)
CORS(app)

@app.route("/process_lines", methods=["POST"])
def process_lines():
    process_openai_response(request.json)
    return jsonify({"message": "Processing started"}), 200

if __name__ == "__main__":
    app.run(debug=True)

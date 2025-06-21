# review_api_mock.py
from flask import Flask, jsonify
import pandas as pd

app = Flask(__name__)

@app.route("/api/reviews", methods=["GET"])
def get_reviews():
    try:
        df = pd.read_csv("data/reviews_api/olist_order_reviews_dataset.csv")
        return jsonify(df.to_dict(orient="records"))
    except Exception as e:
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5001)

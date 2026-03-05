from flask import Flask, jsonify, request
from flask_cors import CORS
import pandas as pd
import os

app = Flask(__name__)
CORS(app)

CSV_PATH = os.path.join(os.path.dirname(__file__), "..", "data", "All_Diets.csv")
df = pd.read_csv(CSV_PATH)

numeric_cols = ["Protein(g)", "Carbs(g)", "Fat(g)"]
df[numeric_cols] = df[numeric_cols].fillna(df[numeric_cols].mean())

@app.route("/")
def home():
    return "Nutritional Insights API is running!"

@app.route("/api/insights")
def get_insights():
    avg_macros = df.groupby("Diet_type")[["Protein(g)", "Carbs(g)", "Fat(g)"]].mean()
    result = avg_macros.to_dict("index")
    return jsonify(result)

@app.route("/api/recipes")
def get_recipes():
    diet_type = request.args.get("diet_type", None)
    if diet_type:
        filtered = df[df["Diet_type"] == diet_type]
        return jsonify(filtered.to_dict("records"))
    return jsonify(df.to_dict("records"))

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000, debug=True)
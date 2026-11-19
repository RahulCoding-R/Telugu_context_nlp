
from flask import Flask, request, jsonify
from transliteration import transliterate

app = Flask(__name__)
app.json.ensure_ascii = False

@app.route("/transliterate", methods=["POST"])
def convert():
    data = request.get_json()
    text = data.get("text", "").strip()

    if not text:
        return jsonify({"error": "Text is required"}), 400

    result = transliterate(text)

    return app.response_class(
        response=__import__("json").dumps(
            {"telugu": result},
            ensure_ascii=False
        ),
        status=200,
        mimetype="application/json"
    )

if __name__ == "__main__":
    print("IndicXlit service starting...")
    app.run(host="127.0.0.1", port=5001, debug=False)

from flask import Flask, render_template, jsonify

app = Flask(
    __name__,
    template_folder="../frontend",
    static_folder="../frontend/static"
)

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/api/test")
def hello():
    return jsonify({"message": "Test from backend"})

if __name__ == "__main__":
    app.run(debug=True)

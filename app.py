from flask import Flask, render_template, request, jsonify
import random
import string

app = Flask(__name__)


def check_password_strength(password):

    score = 0
    suggestions = []

    if len(password) >= 8:
        score += 1
    else:
        suggestions.append("Use at least 8 characters.")

    if any(char.islower() for char in password):
        score += 1
    else:
        suggestions.append("Add at least one lowercase letter.")

    if any(char.isupper() for char in password):
        score += 1
    else:
        suggestions.append("Add at least one uppercase letter.")

    if any(char.isdigit() for char in password):
        score += 1
    else:
        suggestions.append("Add at least one number.")

    if any(char in string.punctuation for char in password):
        score += 1
    else:
        suggestions.append("Add at least one special character.")

    if score <= 2:
        strength = "Weak"

    elif score <= 4:
        strength = "Medium"

    else:
        strength = "Strong"

    return {
        "score": score,
        "strength": strength,
        "suggestions": suggestions
    }


@app.route("/")
def home():
    return render_template("index.html")


@app.route("/check-password", methods=["POST"])
def check_password():

    data = request.get_json()

    if not data:
        return jsonify({
            "error": "Invalid request"
        }), 400

    password = data.get("password", "")

    if not password:
        return jsonify({
            "error": "Password is required"
        }), 400

    return jsonify(
        check_password_strength(password)
    )


@app.route("/generate-password")
def generate_password():

    all_characters = (
        string.ascii_letters
        + string.digits
        + string.punctuation
    )

    password_chars = [
        random.choice(string.ascii_lowercase),
        random.choice(string.ascii_uppercase),
        random.choice(string.digits),
        random.choice(string.punctuation)
    ]

    password_chars += [
        random.choice(all_characters)
        for _ in range(12)
    ]

    random.shuffle(password_chars)

    password = "".join(password_chars)

    return jsonify({
        "password": password
    })


if __name__ == "__main__":
    app.run(debug=True)
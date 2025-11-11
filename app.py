from flask import Flask, render_template, request, redirect, url_for
import json, random, os, string

app = Flask(__name__)

DATA_FILE = "pairs.json"

def load_pairs():
    if os.path.exists(DATA_FILE):
        with open(DATA_FILE, "r") as f:
            return json.load(f)
    return {}

def save_pairs(pairs):
    with open(DATA_FILE, "w") as f:
        json.dump(pairs, f, indent=4)

def generate_token(length=6):
    return ''.join(random.choices(string.ascii_lowercase + string.digits, k=length))

@app.route("/", methods=["GET", "POST"])
def index():
    if request.method == "POST":
        names = request.form["names"].strip().split("\n")
        names = [n.strip() for n in names if n.strip()]
        if len(names) < 2:
            return render_template("error.html", message="Musisz podać co najmniej 2 osoby 🎅")

        # --- losowanie bez wylosowania siebie ---
        def derange(lst):
            while True:
                shuffled = lst.copy()
                random.shuffle(shuffled)
                if all(a != b for a, b in zip(lst, shuffled)):
                    return shuffled

        shuffled = derange(names)

        pairs = {}
        for giver, receiver in zip(names, shuffled):
            token = generate_token()
            pairs[giver] = {"receiver": receiver, "token": token}

        save_pairs(pairs)
        return render_template("links.html", pairs=pairs)

    return render_template("index.html")

@app.route("/view/<name>-<token>")
def view(name, token):
    pairs = load_pairs()
    if name in pairs and pairs[name]["token"] == token:
        return render_template("view.html", name=name, receiver=pairs[name]["receiver"])
    return render_template("error.html", message="Nieprawidłowy link 🎅")

if __name__ == "__main__":
    import os
    port = int(os.environ.get("PORT", 5000))
    app.run(host="0.0.0.0", port=port)

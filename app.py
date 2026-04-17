from flask import Flask, render_template, request, jsonify
import requests
import colorthief
from io import BytesIO
app = Flask(__name__)
UNSPLASH_KEY = "I1DcvL9XP9gnNGw7iGvSq-4QwZ6RI_J79QntMYuWQgE"
def get_images(word):
    url = f"https://api.unsplash.com/search/photos?query={word}&per_page=10"
    headers = {
        "Authorization": f"Client-ID {UNSPLASH_KEY}"
    }
    response = requests.get(url, headers=headers)
    print("STATUS:", response.status_code)
    print("RESPONSE:", response.json())
    data = response.json()
    if "results" not in data:
        return []
    return [img["urls"]["small"] for img in data["results"]]
def get_dominant_color(image_url):
    try:
        response = requests.get(image_url)
        img = BytesIO(response.content)
        color_thief = colorthief.ColorThief(img)
        return color_thief.get_color(quality=1)
    except:
        return (0, 0, 0)
def rgb_to_hex(rgb):
    return '#%02x%02x%02x' % rgb
@app.route("/")
def home():
    return render_template("index.html")
@app.route("/colors")
def colors():
    word = request.args.get("word")
    images = get_images(word)
    if not images:
        return jsonify(["#000000"])
    hex_colors = []
    for img in images:
        rgb = get_dominant_color(img)
        hex_colors.append(rgb_to_hex(rgb))
    return jsonify(hex_colors)
if __name__ == "__main__":
    app.run(debug=True)
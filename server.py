from flask import Flask, jsonify, request, send_from_directory, render_template
import os
import json
import random

app = Flask(__name__)

IMAGE_DIRS = {
    "crawford": "/Users/ciaramaguire/web scraping/crawford_gallery_images",
    "national": "/Users/ciaramaguire/museum_scape/national_gal_images",
    "survey": "/Users/ciaramaguire/survey/images"
}

def get_images(directory, num=2):
    """Returns a list of randomly selected image file names from a given directory."""
    images = [img for img in os.listdir(directory) if img.lower().endswith(('.png', '.jpg', '.jpeg'))]
    return random.sample(images, min(len(images), num))  # Select 2 random images

@app.route('/')
def survey_page():
    """Serves the main survey HTML page."""
    return render_template("survey.html")

@app.route('/get-images', methods=['GET'])
def get_all_images():
    """Returns a selection of images from each category as JSON."""
    all_images = {key: get_images(path) for key, path in IMAGE_DIRS.items()}
    return jsonify(all_images)

@app.route('/images/<category>/<filename>')
def serve_image(category, filename):
    """Serves images dynamically."""
    if category in IMAGE_DIRS:
        return send_from_directory(IMAGE_DIRS[category], filename)
    return jsonify({"error": "Category not found"}), 404

@app.route('/submit-survey', methods=['POST'])
def submit_survey():
    """Receives and saves survey responses."""
    data = request.json
    with open("survey_responses.json", "a") as f:
        json.dump(data, f)
        f.write("\n")  # New line for each response
    return jsonify({"message": "Survey submitted successfully!"})

if __name__ == '__main__':
    app.run(debug=True)

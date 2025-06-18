
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import Flask,request,jsonify,render_template
import requests

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

# initialize the flask
app =Flask(__name__)

app.config["upload_folder"] ='static'

@app.route('/')
def index():
  return render_template('index.html', )

@app.route('/generateimages/<prompt>')
def generate(prompt):
    print("prompt:", prompt)

    response = client.images.generate(
        prompt=prompt,
        n=2,
        size="256x256"
    )

    image_urls = [img.url for img in response.data]
    saved_files = []

    for i, url in enumerate(image_urls):
        image_data = requests.get(url).content
        filename = f"{prompt.replace(' ', '_')}_{i}.png"
        filepath = os.path.join(app.config["upload_folder"], filename)

        with open(filepath, "wb") as f:
            f.write(image_data)

        saved_files.append(filepath)

    return jsonify({
        "local_images": saved_files,
        "remote_urls": image_urls
    })

  


app.run(host="0.0.0.0", debug=True, port=8080)

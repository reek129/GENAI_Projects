
from openai import OpenAI
import os
from dotenv import load_dotenv
from flask import Flask,request,jsonify,render_template

load_dotenv()
OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")

client = OpenAI(api_key=OPENAI_API_KEY)

audio = open("Recording.mp3","rb")

output = client.audio.translations.create(
        model="whisper-1",
        file=audio
    )
print(output)
print(output.text)

# initialize the flask
app =Flask(__name__)

app.config["upload_folder"] ='static'

@app.route('/',methods=['GET','POST'])
def main():
    if request.method =="POST":
        language = request.form["language"]
        file = request.files['file']

        if file:
            filename = file.filename
            file.save(os.path.join(app.config['upload_folder'],filename))
            audio = open(os.path.join(app.config['upload_folder'], filename), "rb")
            transcript = client.audio.translations.create(
                    model="whisper-1",
                    file=audio
                )
            # print(output)
            print(transcript.text)

            response = client.chat.completions.create(
                model="gpt-3.5-turbo",
                messages= [ {
                    "role":"system", "content":f"You will be provided with a sentence in English, and your task is to translate it into {language}"},
                    {"role":"user","content":transcript.text}],
                    temperature=0,
                    max_tokens=128
                )
            print(response.choices[0].message.content)
            return jsonify(response.model_dump())
        
    return render_template("index.html")


if __name__ == "__main__":
    app.run(host="0.0.0.0", debug=True, port=8080)

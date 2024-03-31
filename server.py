from flask import Flask, render_template, jsonify
from flask_socketio import SocketIO, emit
from flask_cors import CORS
import time 
import os
from pydub import AudioSegment
from ai_search import Gemini
from speech_to_text import SpeechToText
from geopy.geocoders import Nominatim


app = Flask(__name__)
CORS(app)
app.config['SECRET_KEY'] = 'secret!'
socketio = SocketIO(app)


@app.route("/", methods=["GET"])
def home():
    return render_template("home.html")


@socketio.on('connect')
def handle_connect_request():
    print('request made')

values = 1
time_now = time.time()

speech_to_text_engine = SpeechToText()
gemini_bot = Gemini()

first_prompt_flag = True

val_file_name_for_run = 1
os.makedirs(f"audio_recording/{time_now}/{val_file_name_for_run}")

test_out = None

text_from_speech = ""

@socketio.on('stream')
def handle_message(data, geolocation):
    global val_file_name_for_run
    global values
    global test_out

    global text_from_speech
    global gemini_bot

    global first_prompt_flag

    global text_from_speech

    print(geolocation)
    file_name = f"audio_recording/{time_now}/{val_file_name_for_run}/test" + str(values) + ".wav"
    with open(file_name, "ab") as file:
        file.write(data)

    if values == 1:
        test_out = AudioSegment.from_wav(file_name)
        first_prompt_flag = False
        first_prompt_text = "The following is a conversation between a police officer and a driver. "
        if len(geolocation) != 0:
            latitude = geolocation['latitude']
            longitude = geolocation['longitude']

            geolocator = Nominatim(user_agent="myApp")
            location = geolocator.reverse(f"{latitude}, {longitude}", exactly_one=True) 

            if location:
                address_dict = location.raw['address']
                state = address_dict.get('state', 'State not available')  # Handle cases where state is missing
                county = address_dict.get('county', 'County not available')
                first_prompt_text+=f"This is taking place in {state} and {county} county. "
        
    else:
        test_out+=AudioSegment.from_wav(file_name)
        first_prompt_text = ""

    
    text_from_speech += speech_to_text_engine.convert_speech_to_text(file_name)
    text_from_speech += "\n"
    print(text_from_speech)

    prompt = f"""
            {first_prompt_text}
            Split up the following "Information" into sentences based on your understanding, but don't show it in your response. 
            After which, there is a question, please answer that.
            
            Information:
            {text_from_speech}

            Is there any law that protects me? Be specific about the details of the laws, put them in bullet points, 
            and limit it to 400 words and point us to the government documents on the web that work as a proof. 
            include only the Rights and proofs in the response.
            """
    try:
        gemini_response = gemini_bot.ask_gemini(prompt)

        print(gemini_response)
    except:
        gemini_response = None
        text_from_speech = ""
        print("No Valid Response")

    socketio.emit('recommendation', {'data' : gemini_response})
    values+=1
    if(os.path.exists(file_name)):
        os.remove(file_name)
    print(f"Done: {len(data)}")

@app.route("/stop-recording", methods=['GET'])
def update_val_file_name_for_run():
    global values
    global val_file_name_for_run
    global test_out
    global time_now
    global text_from_speech
    global gemini_bot

    gemini_bot = Gemini()

    test_out.export(f"audio_recording/{time_now}/{val_file_name_for_run}/testOut.wav", format = "wav")

    text_from_speech = ""
    val_file_name_for_run+=1
    values = 0
    os.makedirs(f"audio_recording/{time_now}/{val_file_name_for_run}")
    return jsonify({"msg:": "All OK"})

if __name__ == '__main__':
    socketio.run(app)

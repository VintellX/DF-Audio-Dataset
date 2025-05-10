import os
import speech_recognition as sr
import json
import re

def fetchTranscript(dir_path):
    print(dir_path)
    recognizer = sr.Recognizer()
    transcriptions = {}
    removedFiles = []
    pattern = re.compile(r"^(.+)_input(\d+)\.wav$")
    for filename in os.listdir(dir_path):
        m = pattern.match(filename)
        if not m:
            continue
        filenum = int(m.group(2))
        audioPhile = os.path.join(dir_path, filename)
        with sr.AudioFile(audioPhile) as source:
                audio_data = recognizer.record(source)
                try:
                    text = recognizer.recognize_google(audio_data)
                    transcriptions[filenum] = text
                except sr.UnknownValueError:
                    os.remove(audioPhile)
                    removedFiles.append(filenum)
                    print(f"couldn't understand {filename}")
                    print("removed the file")
                except sr.RequestError as e:
                    removedFiles.append(filenum)
                    os.remove(audioPhile)
                    print(f"error: {e}")
                    print("removed the file")
    return transcriptions, removedFiles

def jasonifyTranscript(transcript, speaker):
    new_data = {f"{speaker}_input{key}": value for key, value in transcript.items()}
    with open(os.path.join("DeepFake","FakeAudios",f"{speaker}_recordings","transcript.json"), "w", encoding="utf-8") as f:
        json.dump(new_data, f, indent=4, ensure_ascii=False)
    print("json file saved")

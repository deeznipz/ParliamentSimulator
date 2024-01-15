import whisper


model = whisper.load_model("base")
audio = whisper.load_audio("C:/Users/deezn/Desktop/py/CHATBOTS/SeymChloeAM.mp3")     
result = model.transcribe(audio)
print(result["text"])
print(result["segments"])
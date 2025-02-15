import whisper
import opencc

model = whisper.load_model("tiny")
result = model.transcribe("test.wav", language="zh")
print(result["text"])


cc = opencc.OpenCC('t2s.json')
result = cc.convert(result['text'])
print(result)

import pyaudio
import time
import whisper
import wave
import webrtcvad
import threading
import queue
import whisper
import gtts
from zhipuai import ZhipuAI
import base64
import requests
import json
import urllib
from pydub import AudioSegment
import config

prompt_front = """你是一个智能语音助手，负责将用户的语音转换为对应的指令 ID。
下面是指令的映射表（id → description）：
- 1001 → 小爱同学
- 1002 → 瞄准
- 1003 → 开火
- 0 → 未知指令
你的任务是：
1. 尽可能匹配 用户的输入到最接近的指令 ID，避免返回 0，除非完全无法推测意图。
2. 允许一定程度的错误匹配，例如“灯光”可以匹配“打开灯”或“关闭灯”，“调高空调”可以匹配“提高温度”。
3. 仅返回整数 ID，不要包含任何其他文本**。
4. 返回格式：仅返回对应的指令 **整数 ID**，如果无法匹配，则返回 0。
用户输入："""




CHUNK = 4800  # 采样块（暂存区大小/暂存的采样点数）
SAMPLE_RATE = 48000  # 采样率
CHANNELS = 1  # 通道数
RECORD_SECONDS = 0.3  # 采样时间
SAMPLE_DEPTH = pyaudio.paInt16  # 采样深度
SAMPLE_BYTES = pyaudio.get_sample_size(SAMPLE_DEPTH)  # 采样字节数
VAD_DURATION = 0.01
API_KEY = "lYEShay5YT17nwTj4T5CU9ye"
SECRET_KEY = "XSygUiSVW8xTIkXqVkoKqFMDoYYkRetQ"



class AudioInput:
    def __init__(self):
        self.client = ZhipuAI(
            api_key="f8ab318eb41a4d34a2524ec4f8706157.s6SZey1ivTJkcrvJ"
        )  # 初始化ZhipuAI
        """队列"""
        self.fifo_queue = queue.Queue()  # 创建队列
        self.sample_buffer = []  # 创建采样暂存区
        self.voice_buffer = []  # 创建语音暂存区

        """Whisper"""
        self.model = whisper.load_model("base")  # 加载模型

        """Pyaudio"""
        self.audio_input = pyaudio.PyAudio()  # 创建PyAudio对象
        self.is_audio_input_thread_running = True  # 音频输入线程是否运行
        self.stream = self.audio_input.open(
            format=SAMPLE_DEPTH,
            channels=CHANNELS,
            rate=SAMPLE_RATE,
            frames_per_buffer=CHUNK,
            input=True,
            input_device_index=1,
            stream_callback=self.callback,
            start=False,
        )  # 创建流

        """VAD"""
        self.vad = webrtcvad.Vad()  # 初始化VAD
        self.vad.set_mode(3)  # 设置VAD模式
        self.is_vad_thread_running = True  # VAD线程是否运行
        self.vad_thread = threading.Thread(target=self.vad_thread_func)  # 创建VAD线程
        self.vad_thread.start()

        self.aim = 0
        self.fire = 0

    def vad_thread_func(self):

        while True:
            print("begin")
            self.fifo_queue.get()  # 从队列中取出数据
            config.tag = 1
            result = self.model.transcribe("temp.wav")  # 识别语音
            '''result = self.post()
            result_dict = json.loads(result)
            result = {}
            result["text"] = result_dict["result"][0]'''
            print(result["text"])

            content = prompt_front + result["text"]
            print(content)
            response = self.client.chat.completions.create(
                model="glm-4-plus",  # 请填写您要调用的模型名称
                messages=[
                    {
                        "role": "user",
                        "content": content,
                    },
                ],
            )
            result = response.choices[0].message.content

            if result == "1001":
                voice = "在"
                print("小爱同学")
                self.command = 0
            elif result == "1002":
                voice = "好的"
                print("瞄准")
                self.aim = 1
            elif result == "1003":
                voice = "收到"
                print("开火")
                self.fire = 1
            else:
                voice = "什么"
                print("无法识别")
                self.command = 0
            print(voice)
            tts = gtts.gTTS(text=str(voice), lang="zh", slow=True)
            tts.save("result.mp3")  # gTTS 生成的是 MP3 格式

            # 转换 MP3 到 WAV（PCM 格式）
            audio = AudioSegment.from_mp3("result.mp3")
            audio.export("result.wav", format="wav")
            wf = wave.open("result.wav", 'rb')
            audio_output = pyaudio.PyAudio()
            stream_output = audio_output.open(format=self.audio_input.get_format_from_width(wf.getsampwidth()),
                channels=wf.getnchannels(),
                rate=wf.getframerate(),
                output=True)
            # 读取数据并播放
            chunk_size = 1024  # 每次读取的帧数
            data = wf.readframes(chunk_size)
            
            while data:
                stream_output.write(data)  # 播放音频数据
                data = wf.readframes(chunk_size)
            config.tag = 0
            time.sleep(0.5)
            print("end")

    def callback(self, in_data, frame_count, time_info, status_flags):
        self.sample_buffer.append(in_data)  # 暂存区添加数据
        if (
            len(self.sample_buffer) >= RECORD_SECONDS * SAMPLE_RATE / CHUNK
        ):  # 暂存区数据量达到采样时间
            sample_buffer_bytes = b"".join(
                self.sample_buffer
            )  # 采样暂存区字节数组数据拼接
            speech_rate = self._calculate_speech_rate(sample_buffer_bytes)  # 计算语音率
            #print(speech_rate)
            if speech_rate > 0.5:
                self.voice_buffer.append(sample_buffer_bytes)  # 语音暂存区添加数据
            else:
                if len(self.voice_buffer) > 0:
                    with wave.open("temp.wav", "wb") as wf:
                        wf.setnchannels(CHANNELS)  # 设置采样通道
                        wf.setsampwidth(
                            self.audio_input.get_sample_size(SAMPLE_DEPTH)
                        )  # 设置采样深度
                        wf.setframerate(SAMPLE_RATE)  # 设置采样率
                        wf.writeframes(b"".join(self.voice_buffer))  # 写入文件
                    self.voice_buffer = []  # 清空语音暂存区
                    self.fifo_queue.put(1)  # 添加到队列
            self.sample_buffer = []  # 清空采样暂存区
        return (b"", pyaudio.paContinue)

    def post(self):
        url = "https://vop.baidu.com/pro_api"

        # speech 可以通过 get_file_content_as_base64("C:\fakepath\temp.wav",False) 方法获取
        speech, len = self._get_file_content_as_base64(
            "/home/YFENG/Desktop/Raspi-car/temp.wav", False
        )
        payload = json.dumps(
            {
                "format": "wav",
                "rate": 16000,
                "channel": 1,
                "cuid": "N0AfnEwIjBnyuPaswZ2g5UTwYQPyhj8U",
                "dev_pid": 80001,
                "speech": speech,
                "len": len,
                "token": self._get_access_token(),
            },
            ensure_ascii=False,
        )
        headers = {"Content-Type": "application/json", "Accept": "application/json"}

        response = requests.request(
            "POST", url, headers=headers, data=payload.encode("utf-8")
        )

        print(response.text)
        return response.text

    def _get_file_content_as_base64(self, path, urlencoded=False):
        """
        获取文件base64编码
        :param path: 文件路径
        :param urlencoded: 是否对结果进行urlencoded
        :return: base64编码信息
        """
        with open(path, "rb") as f:
            data = f.read()
            length = len(data)
            content = base64.b64encode(data).decode("utf8")
            if urlencoded:
                content = urllib.parse.quote_plus(content)
        return content, length

    def _get_access_token(self):
        """
        使用 AK，SK 生成鉴权签名（Access Token）
        :return: access_token，或是None(如果错误)
        """
        url = "https://aip.baidubce.com/oauth/2.0/token"
        params = {
            "grant_type": "client_credentials",
            "client_id": API_KEY,
            "client_secret": SECRET_KEY,
        }
        return str(requests.post(url, params=params).json().get("access_token"))

    def _calculate_speech_rate(self, data):
        count = 0
        speech_count = 0
        for i in range(0, len(data), int(SAMPLE_BYTES * VAD_DURATION * SAMPLE_RATE)):
            contains_speech = self.vad.is_speech(
                data[i : i + int(SAMPLE_BYTES * VAD_DURATION * SAMPLE_RATE)],
                SAMPLE_RATE,
            )
            count += 1
            if contains_speech:
                speech_count += 1
        speech_rate = speech_count / count
        return speech_rate

    def get_command(self):
        pass


class AudioOutput:
    def __init__(self):
        self.audio_output = pyaudio.PyAudio()
        self.frames = []
        self.stream = self.audio_output.open(
            format=SAMPLE_DEPTH,
            channels=1,
            rate=SAMPLE_RATE,
            frames_per_buffer=CHUNK,
            output=True,
            input_device_index=2,
            stream_callback=self.callback,
            start=False,
        )

    def callback(self, in_data, frame_count, time_info, status_flags):
        print(len(in_data))
        self.frames.append(in_data)
        return (b"", pyaudio.paContinue)

    def start(self):
        print(self.stream.is_active())
        if not self.stream.is_active():
            self.stream.start_stream()
            print("播放开始")
        else:
            print("播放未停止，开启失败")

    def stop(self):
        print(self.stream.is_active())
        if self.stream.is_active():
            self.stream.stop_stream()
            print("播放停止")
        else:
            print("播放未开始，停止失败")


if __name__ == "__main__":
    audio_input = AudioInput()
    time.sleep(1000)
    audio_input.stream.stop_stream()
    audio_input.is_vad_thread_running = False

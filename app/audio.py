import pyaudio
import time
import whisper
import wave
import webrtcvad
import threading
import queue
import whisper
import opencc
import numpy

CHUNK = 4800  # 采样块（暂存区大小/暂存的采样点数）
SAMPLE_RATE = 48000
CHANNELS = 1
RECORD_SECONDS = 1  # 采样时间
SAMPLE_DEPTH = pyaudio.paInt16  # 采样深度
SAMPLE_BYTES = pyaudio.get_sample_size(SAMPLE_DEPTH)  # 采样字节数
VAD_DURATION = 0.01


class AudioInput:
    def __init__(self):
        """队列"""
        self.fifo_queue = queue.Queue()  # 创建队列
        self.in_data_frames = []  # 创建暂存区
        self.communication_buffer = []

        """Whisper"""
        self.model = whisper.load_model("base")

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
            start=True,
        )  # 创建流

        """VAD"""
        self.vad = webrtcvad.Vad()  # 初始化VAD
        self.vad.set_mode(1)  # 设置VAD模式
        self.is_vad_thread_running = True  # VAD线程是否运行
        self.vad_thread = threading.Thread(target=self.vad_thread_func)  # 创建VAD线程
        self.vad_thread.start()



    def callback(self, in_data, frame_count, time_info, status_flags):
        print(len(in_data))
        self.in_data_frames.append(in_data)  # 暂存区添加数据
        if (
            len(self.in_data_frames) >= RECORD_SECONDS * SAMPLE_RATE / CHUNK
        ):  # 暂存区数据量达到采样时间
            self.fifo_queue.put(b"".join(self.in_data_frames))  # 添加数据到队列
            self.in_data_frames = []
            '''with wave.open("test.wav", "wb") as wf:
                wf.setnchannels(CHANNELS)
                wf.setsampwidth(self.audio_input.get_sample_size(SAMPLE_DEPTH))
                wf.setframerate(SAMPLE_RATE)
                wf.writeframes(b"".join(self.in_data_frames))
                self.in_data_frames = []
            return (b"", pyaudio.paComplete)'''
        return (b"", pyaudio.paContinue)

    def vad_thread_func(self):
        while True:
            data = self.fifo_queue.get()
            count = 0
            speech_count = 0
            for i in range(
                0, len(data), int(SAMPLE_BYTES * VAD_DURATION * SAMPLE_RATE)
            ):
                contains_speech = self.vad.is_speech(
                    data[i : i + int(SAMPLE_BYTES * VAD_DURATION * SAMPLE_RATE)],
                    SAMPLE_RATE,
                )
                count += 1
                if contains_speech:
                    speech_count += 1
            speech_rate = speech_count / count
            print(speech_rate)
            if speech_rate > 0.5:
                self.communication_buffer.append(data)
            else:
                array = numpy.ndarray(b"".join(self.communication_buffer), dtype=numpy.int16)
                result = self.model.transcribe(array)
                print(result["text"])
                self.communication_buffer = []

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
    time.sleep(5)
    audio_input.stream.stop_stream()
    audio_input.is_vad_thread_running = False

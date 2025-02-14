import pyaudio
import time

CHUNK = 1024  # 采样块（暂存区大小/暂存的采样点数）
SAMPLE_RATE = 44100  # 采样率
RECORD_SECONDS = 5  # 采样时间
SAMPLE_DEPTH = pyaudio.paInt16  # 采样深度


class Audio:
    def __init__(self):
        self.audio = pyaudio.PyAudio()
        self.frames = []
        self.is_recording = False
        self.is_playing =False
        self.frames = []
        self.stream = self.audio.open(
            format=SAMPLE_DEPTH,
            channels=1,
            rate=SAMPLE_RATE,
            input=True,
            input_device_index=0,
            frames_per_buffer=CHUNK,
            stream_callback=self.callback,
            start=False
        )
    def callback(self, in_data, frame_count, time_info, status_flags):
        print(len(in_data))
        self.frames.append(in_data)
        return (b'', pyaudio.paContinue)
    def start(self):
        print(self.stream.is_active())
        if not self.stream.is_active():
            self.stream.start_stream()
            print("录音开始")
        else:
            print("录音未停止，开启失败")

    def stop(self):
        print(self.stream.is_active())
        if self.stream.is_active():
            self.stream.stop_stream()
            print("录音停止")
        else:
            print("录音未开始，停止失败")

if __name__ == '__main__':
    audio = pyaudio.PyAudio()
    print(audio.get_device_count())
    def callback(in_data, frame_count, time_info, status_flags):
        print(len(in_data))
        return (b'', pyaudio.paContinue)
    stream = audio.open(
        format=SAMPLE_DEPTH,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        input_device_index=0,
        frames_per_buffer=CHUNK,
    )
    while True:
        time.sleep(1)
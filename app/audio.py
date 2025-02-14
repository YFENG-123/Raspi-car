import pyaudio
import time

CHUNK = 1024  # 采样块（暂存区大小/暂存的采样点数）
SAMPLE_RATE = 16000
RECORD_SECONDS = 5  # 采样时间
SAMPLE_DEPTH = pyaudio.paInt16  # 采样深度


class AudioInput:
    def __init__(self):
        self.audio_input = pyaudio.PyAudio()
        self.frames = []
        self.stream = self.audio_input.open(
            format=SAMPLE_DEPTH,
            channels=1,
            rate=SAMPLE_RATE,
            frames_per_buffer=CHUNK,
            input=True,
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
    audio = pyaudio.PyAudio()
    print("count:", audio.get_device_count())
    print("0:", audio.get_device_info_by_index(0))
    print("1:", audio.get_device_info_by_index(1))
    print("2:", audio.get_device_info_by_index(2))

    def callback(in_data, frame_count, time_info, status_flags):
        print(len(in_data))
        return (b"", pyaudio.paContinue)

    stream = audio.open(
        format=SAMPLE_DEPTH,
        channels=1,
        rate=SAMPLE_RATE,
        input=True,
        input_device_index=0,
        frames_per_buffer=CHUNK,
        stream_callback=callback,
        start=False
    )
    while True:
        time.sleep(1)

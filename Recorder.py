import pyaudio
import wave
import os

class RecAUD:

    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):

        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.RECORD_SECONDS = 10
        self.p = py
        self.frames = []
        self.st = 1
        self.recording = False


    def start_record(self,duration,song):
        self.stream = self.p.open(format=self.FORMAT, channels=self.CHANNELS, rate=self.RATE, input=True, frames_per_buffer=self.CHUNK)
        self.frames = []
        self.recording = True
        print("record inicio")
        for i in range(0, int(self.RATE / self.CHUNK * duration)):#self.RECORD_SECONDS)):
            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            print("* recording:", duration)
            if self.recording == False:
                break


        self.stop(song)

    def stop(self,song):
        self.stream.close()
        file = song + '.wav'
        i = 0
        while os.path.isfile(os.getcwd() + '/Recordings/' + file) == True:
            i+= 1
            file = song + str(i) + '.wav'
        print(os.getcwd() + '/Recordings/' + file)
        wf = wave.open(os.getcwd() + '/Recordings/' + file, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.p.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()

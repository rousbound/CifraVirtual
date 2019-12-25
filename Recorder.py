import pyaudio
import wave
import os

class RecAUD:

    def __init__(self, chunk=3024, frmat=pyaudio.paInt16, channels=2, rate=44100, py=pyaudio.PyAudio()):

        self.CHUNK = chunk
        self.FORMAT = frmat
        self.CHANNELS = channels
        self.RATE = rate
        self.RECORD_SECONDS = 1500
        self.pyaudio = py
        self.frames = []
        #self.st = 1
        self.recording = False


    def captureChunkData(self, song):
        self.stream     =          self.pyaudio.open\
                           (format=self.FORMAT,\
                          channels=self.CHANNELS,\
                              rate=self.RATE,\
                             input=True,
                 frames_per_buffer=self.CHUNK)

        self.frames = []
        self.recording = True
        
        asdasdasd

        print("Start Recording")

        for i in range(0, int(self.RATE / self.CHUNK * self.RECORD_SECONDS)):

            data = self.stream.read(self.CHUNK)
            self.frames.append(data)
            if self.recording == False:
                break

        self.saveChunkData(song)
  

    def saveChunkData(self,song):
        self.stream.close()
        filePath = song + '.wav'
        i = 0

        #Song Version control
        while os.path.isfile(os.getcwd() + '/Recordings/' + filePath) == True:
            i+= 1
            filePath = song + str(i) + '.wav'
        print("Song File Path:", os.getcwd() + '/Recordings/' + filePath)

        wf = wave.open(os.getcwd() + '/Recordings/' + filePath, 'wb')
        wf.setnchannels(self.CHANNELS)
        wf.setsampwidth(self.pyaudio.get_sample_size(self.FORMAT))
        wf.setframerate(self.RATE)
        wf.writeframes(b''.join(self.frames))
        wf.close()


    def stopRecording(self):
        self.recording = False

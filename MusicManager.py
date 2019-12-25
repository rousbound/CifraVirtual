from Recorder import *
import threading
import vlc
from pytube import YouTube
import os

class AudioHandler:
    def __init__(self):
        self.player = None
        self.recorder = RecAUD()

    def getCurrentItemTitle(self,Main):
      return Main.ui.musicList.currentItem().text()

    def getSongPathFromList(self,listWidget):
      title = listWidget.currentItem().text()
      return "Music/" + title + ".mp3"

    def toggleMusic(self,Main,listWidget):
        if listWidget.currentItem():
            
            filePath = self.getSongPathFromList(listWidget)
            if not os.path.isfile(filePath):
              print("Song not found")
              return

            if self.player == None:

              self.player = vlc.MediaPlayer(filePath)

              if Main.ui.musicRecording.isChecked():
                self.startRecordingThread(Main)

              self.player.play()

              self.updatePositionThread = threading.Thread\
                                (target = self.updatePosition, 
                                 daemon = True, 
                                   args = (Main,))

              self.updatePositionThread.start()

            else:

              self.recorder.stopRecording()
              self.player.pause()
              self.player.audio_set_volume(100)

        else:

          print("No song selected")

    def startRecordingThread(self, Main):
        self.recording = True
        recordingLength = 5
        print("Song Length:", recordingLength)
        self.recordThread               =     threading.Thread\
                                (target = self.recorder.captureChunkData,
                                 daemon = True, 
                                   args = (self.getCurrentItemTitle(Main),))
        self.recordThread.start()

    def updatePosition(self, Main):
        while True:
            try:
                Main.ui.musicTimeTrack.setValue(self.player.get_position()*100)
            except:
                pass

    def replayMusic(self,listWidget):
        if self.player:
          self.player.stop()
          filePath = self.getSongPathFromList(listWidget)
          self.player = vlc.MediaPlayer(filePath)
          self.player.play()
        else:
          print("No song playing")

    def changeTimePos(self,interval):
        if self.player:
          print("Old time:",self.player.get_time())
          now = self.player.get_time()
          self.player.set_time(now+interval)
        else:
          print("No song playing")

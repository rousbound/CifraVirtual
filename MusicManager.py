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


            if self.player == None:

              if not os.path.isfile(filePath):
                if Main.ui.musicRecording.isChecked():
                  print("Song not found, recording anyway")
                  self.startRecordingThread(Main)
                  self.player = "recording"
                  return
                else:
                  print("Song not found")
                  return

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

              try:
                self.player.pause()
                self.player.audio_set_volume(100)
              except:
                pass

        else:

          print("No song selected")

    def startRecordingThread(self, Main):
        self.recording = True
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

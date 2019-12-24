from Recorder import *
import threading
import vlc
from pytube import YouTube
import os

class MusicComponent:
    def __init__(self):
        self.player = None
        self.recorder = RecAUD()

    def getSongPathFromList(self,list):
      title = list.currentItem().text()
      return "Music/" + title + ".mp3"

    def toogleMusic(self,Main,list):
        if list.currentItem():
              filePath = self.getSongPathFromList(list)
              if not os.path.isfile(filePath):
                print("Song not found")
                return
              if self.player == None:
                  self.player = vlc.MediaPlayer(filePath)
                  self.player.play()

                  self.updatePositionThread = threading.Thread(target = self.updatePosition, daemon = True, args = (Main,))
                  self.updatePositionThread.start()


              else:
                  self.player.pause()
              self.player.audio_set_volume(100)
        else:
          print("No song selected")

    def updatePosition(self, Main):
        while True:
            try:
                Main.ui.musicTimeTrack.setValue(self.player.get_position()*100)
            except:
                pass

    def replayMusic(self,list):
        if(self.player):
          self.player.stop()
          file = getSongPathFromList(list)
          self.player = vlc.MediaPlayer(file)
          self.player.play()
        else:
          print("No song playing")

    def changeTimePos(self,interval):
        if(self.player):
          print("Old time:",self.player.get_time())
          now = self.player.get_time()
          new_pos = now + interval
          self.player.set_time(new_pos)
        print("No song playing")



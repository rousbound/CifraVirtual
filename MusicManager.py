from Recorder import *
import threading
import vlc
from pytube import YouTube
import os

class AudioHandler:
    def __init__(self):
        self.player = None
        self.recorder = RecAUD()

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
								self.player.play()

								self.updatePositionThread = \
								threading.Thread(target = self.updatePosition, \
																 daemon = True, \
																   args = (Main,))

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
          new_pos = now + interval
          self.player.set_time(new_pos)
				else:
					print("No song playing")



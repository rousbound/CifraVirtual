from Recorder import *
import threading
import vlc
from pytube import YouTube

class Music:
    def __init__(self):
        self.player = None
        self.recorder = RecAUD()

    def manageRecording(self, command, Main):
        if command == "start":
            if Main.ui.musicRecording.isChecked():
                print("lenght1:",self.player.get_length())
                for i in range(100):
                    length = 15 * 1000
                    if length != 0:
                        break
                print("length:",length)
                self.recordThread = threading.Thread(target = self.recorder.start_record, daemon = True, args = (length,Main.ui.musicList.currentItem().text(),))
                self.recordThread.start()
                self.recording = True
        if command == "stop":
            self.recorder.recording = False

    def updatePosition(self, Main):
        while True:
            try:
                Main.ui.musicTimeTrack.setValue(self.player.get_position()*100)
            except:
                pass

    def MusicAddItem(self, Main):
        if Main.ui.musicSmartButton.isChecked():
            self.downloadthread = threading.Thread(target = self.downloadMusicNew, args = (Main,), daemon = True)
            self.downloadthread.start()
            Main.ui.musicSmartButton.setCheckState(False)
            Main.ui.musicUrlLineEntry.clear()
            Main.newListItem(lineEntry = Main.ui.musicLineEntry, textDisplay = Main.ui.musicTextDisplay, list = Main.ui.musicList)

        else:
            Main.newListItem(lineEntry = Main.ui.musicLineEntry, textDisplay = Main.ui.musicTextDisplay, list = Main.ui.musicList)


    def downloadMusic(self, Main):
        yt = YouTube(Main.ui.musicUrlLineEntry.text())
        print("Download Confirmed")
        print("downloading:",yt.title)
        yt.streams.filter(only_audio=True).first().download()
        cwd = os.getcwd()
        for i,el in enumerate(os.listdir(cwd)):
            if Main.ui.musicLineEntry.text() in el:
                os.rename(el,cwd + '/Music/'+ Main.ui.musicLineEntry.text() + ".mp3")
        print("download succesfull")
        self.newListItem(lineEntry = self.ui.musicLineEntry, textDisplay = self.ui.musicTextDisplay, list = self.ui.musicList)

    def downloadMusicNew(self,Main):
        yt = YouTube(Main.ui.musicUrlLineEntry.text())
        print("Download Confirmed")
        print("downloading:",yt.title)
        yt.streams.filter(only_audio=True).first().download()
        cwd = os.getcwd()
        for i,el in enumerate(os.listdir(cwd)):
            if ".mp4" in el:
                os.rename(el,cwd + '/Music/'+ Main.ui.musicLineEntry.text() + ".mp3")
        print("download succesfull")
        #Main.newListItem(lineEntry = Main.ui.musicLineEntry, textDisplay = Main.ui.musicTextDisplay, list = Main.ui.musicList)

    def playMusic(self,Main,list):
        if self.player == None:
            file = "Music/" + list.currentItem().text() + ".mp3"
            self.player = vlc.MediaPlayer(file)
            self.player.play()
            print("LENGHT:",self.player.get_length())
            self.manageRecording("start",Main)
            self.updatePositionThread = threading.Thread(target = self.updatePosition, daemon = True, args = (Main,))
            self.updatePositionThread.start()
        else:
            self.player.pause()
            self.manageRecording("stop",Main)
            #self.updatePositionThread.stop()
        self.player.audio_set_volume(100)

    def changeTimePos(self,interval):
        print("old time:",self.player.get_time())
        now = self.player.get_time()
        new_pos = now + interval
        self.player.set_time(new_pos)
        print("new time:",self.player.get_time())#,self.player.get_time()-5000)#self.player.get_time())


    def replayMusic(self,list):
        self.player.stop()
        file = "Music/" + list.currentItem().text() + ".mp3"
        self.player = vlc.MediaPlayer(file)
        self.player.play()


    def openItem(self,main,path,list,display):
        if self.player:
            self.player.stop()
            self.player = None
        text = path + list.currentItem().text()
        main.open_file(text,display)

music = Music()

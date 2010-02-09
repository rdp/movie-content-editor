import vlc
import sys
import time
from threading import Thread

DEBUG = True

def sendDebug(msg, newline=1):
    global DEBUG
    if DEBUG:
        if newline:
            print ' '
        print msg

# For now I need to define the path, I commented out so it should work for you guys
#path = 'C:\Users\Kimberly\Desktop\Andrew\Movie Editor\movie-editor\\'
path = ''

# ------ pre-process sections to mute -----------
try:
    f = open(path + 'mute.txt','r')
    i = 0
    aType = []
    begin = []
    finish = []
    for line in f:
        separate = line.strip().split()
        aType.append(int(separate[0]))
        begin.append(float(separate[1])*1000)
        finish.append(float(separate[2])*1000)
    f.close()
except IOError:
    print("File not found")
    sys.exit()
# ------------------------------------------------

# -------- Load and start movie ----------------
instance = vlc.Instance()
instance.add_intf("qt")
media = instance.media_new(path + "Kung Fu Panda.m4v")
player = instance.media_player_new()
player.set_media(media)
player.play()
# -------------------------------------------------

# I use this for testing with Panda
player.set_time(35000)

# turn on subtitles
player.video_set_subtitle_file(path + "panda_edit.srt")


# ------------- subclass off of Thread ---------------
class editThread (Thread):
        
    # right now this only handles mute and will need to include a
    # check in case it is interrupted by another thread.  
    def run ( self ):
        for i in range (0,len(begin)):
            
            # sleep until time for next action
            tSleep = (begin[i] - player.get_time())/1000
            if (tSleep > 30):
                time.sleep(tSleep-30)
                tSleep = (begin[i] - player.get_time())/1000
            time.sleep(tSleep)
            
            # perform action
            if (aType[i] == 0):
                onMute()
            elif (aType[i] == 1):
                offMute()
            elif (aType[i] == 2):
                skip((finish[i] - begin[i])/1000)
                
        return
# ------------------------------------------------------

# ------- methods -------------------------
def onMute ():
    instance.audio_set_mute(1)
    return
    
def offMute ():
    instance.audio_set_mute(0)
    return

def skip(tSkip):
    player.set_time(player.get_time() + long(tSkip*1000))
    return

def stop(player):
    player.stop()
    sys.exit()
# --------------------------------------------

thread1 = editThread()
thread1.start()

# this is temporary just so player doesn't go on for long time
time.sleep(80-player.get_time()/1000)
stop(player)



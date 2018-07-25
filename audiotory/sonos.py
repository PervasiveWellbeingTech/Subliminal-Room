import libs
import soco
import time
zones = soco.discover()
sonos = zones.pop()
sonos.play_uri(
        'http://ia801402.us.archive.org/20/items/TenD2005-07-16.flac16/TenD2005-07-16t10Wonderboy.mp3')

time.sleep(2)
sonos.pause()

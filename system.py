import ika
import sys

try:
    import os
except ImportError:
    # No python installed.  Try to figure out what the builtin
    # module is, and (evil hack) import that in its place
    for m in ('posix', 'nt', 'os2', 'mac', 'ce', 'riscos'):
        if m in sys.builtin_module_names:
            os = __import__(m)
            break

# If a src/ directory exists, add it to the search path.
# If not, and a src.zip exists, use that.
if os.access('src', os.R_OK):
    sys.path.insert(0, 'src')
elif os.access('src.zip', os.R_OK):
    sys.path.append(0, 'src.zip')
else:
    ika.Exit('Unable to find source!!')



import config
import engine
import gui
from intro import intro, menu
import sound

import controls
controls.init()

import subscreen
subscreen.init()

try:
    c = controls.readConfig(config.CONTROL_CONFIG)
except IOError:
    c = controls.defaultControls
    controls.writeConfig(config.CONTROL_CONFIG, c)

#c = controls.defaultControls
controls.setConfig(c)



import data
data.init()

sound.playMusic('title')

# LEAVE THIS FOR LATER K
#for n in range(1,100):
#    print '%i: %i' % (n, int(50 * (1.9 ** (n - 1))))

intro()

while True:

    #sound.fader.kill()
    #introMusic.position = 0
    #introMusic.Play()

    #need to move to appropriate place

    result = menu()
    if result == 0:
        #introMusic.Pause()
        engine.beginNewGame()

    elif result == 1:
        #introMusic.Pause()
        engine.loadGame()

    elif result == 2:
        break

    elif result == 3:
        engine.happyFunTime()

    else:
        raise RuntimeError('Wacky intro menu result %i! :o' % result)
    engine.player = None

ika.Exit()

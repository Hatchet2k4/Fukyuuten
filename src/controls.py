'''Input abstraction.'''

import ika
import controls  # hack, don't remove
import aries


_keyNames = [
    'BACKSPACE', 'TAB', 'CLEAR', 'RETURN', 'PAUSE', 'ESCAPE', 'SPACE',
    'EXCLAIM', 'QUOTEDBL', 'HASH', 'DOLLAR', 'AMPERSAND', 'QUOTE', 'LEFTPAREN',
    'RIGHTPAREN', 'ASTERISK', 'PLUS', 'COMMA', 'MINUS', 'PERIOD', 'SLASH', '0',
    '1', '2', '3', '4', '5', '6', '7', '8', '9', 'COLON', 'SEMICOLON', 'LESS',
    'EQUALS', 'GREATER', 'QUESTION', 'AT', 'LEFTBRACKET', 'BACKSLASH',
    'RIGHTBRACKET', 'CARET', 'UNDERSCORE', 'BACKQUOTE', 'A', 'B', 'C', 'D',
    'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'O', 'P', 'Q', 'R', 'S',
    'T', 'U', 'V', 'W', 'X', 'Y', 'Z', 'DELETE', 'KP0', 'KP1', 'KP2', 'KP3',
    'KP4', 'KP5', 'KP6', 'KP7', 'KP8', 'KP9', 'KP_PERIOD', 'KP_DIVIDE',
    'KP_MULTIPLY', 'KP_MINUS', 'KP_PLUS', 'KP_ENTER', 'KP_EQUALS', 'UP',
    'DOWN', 'RIGHT', 'LEFT', 'INSERT', 'HOME', 'END', 'PAGEUP', 'PAGEDOWN',
    'F1', 'F2', 'F3', 'F4', 'F5', 'F6', 'F7', 'F8', 'F9', 'F10', 'F11',
    'F12', 'F13', 'F14', 'F15', 'NUMLOCK', 'CAPSLOCK', 'SCROLLOCK', 'RSHIFT',
    'LSHIFT', 'RCTRL', 'LCTRL', 'RALT', 'LALT', 'RMETA', 'LMETA', 'LSUPER',
    'RSUPER', 'MODE'
]


# Name : Control pairs
_allControls = {}

#  'up': 'UP',
#   'down': 'DOWN',
#   'left': 'LEFT',
#   'right': 'RIGHT',
#   'cancel': 'ESCAPE',
#   'attack1': 'SPACE',
#   'attack2' : 'F',
#   'tool1': 'D',
#   'tool2': 'S',
#   'tool3': 'A',
    
defaultControls = {
    'up': 'joy0axis1-',
    'down': 'joy0axis1+',
    'left': 'joy0axis0-',
    'right': 'joy0axis0+',
    'cancel': 'joy0button2',
    'attack1': 'joy0button1',
    'attack2' : 'joy0button0',
    'tool1': 'joy0button3',
    'tool2': 'joy0button4',
    'tool3': 'joy0button5',
    

    
}


def init():
    '''Fill up _allControls.'''
    # Null control
    _allControls['none'] = lambda: False

    # keyboard keys:
    for k in _keyNames:
        _allControls[k] = ika.Input.keyboard[k]

    # joystick:
    for joyIndex, joy in enumerate(ika.Input.joysticks):

        # joystick axes:
        for axisIndex, axis in enumerate(joy.axes):
            _allControls['joy%iaxis%i+' % (joyIndex, axisIndex)] = axis
        for axisIndex, axis in enumerate(joy.reverseaxes):
            _allControls['joy%iaxis%i-' % (joyIndex, axisIndex)] = axis

        # joystick buttons:
        for buttonIndex, button in enumerate(joy.buttons):
            _allControls['joy%ibutton%i' % (joyIndex, buttonIndex)] = button

    setConfig(defaultControls)


def readConfig(f):
    return aries.Document(f).process().toDict()


def writeConfig(f, config):
    aries.writeDict(f, config)


def setConfig(config=None):
    class PosControl(object):
        def __init__(self, name):
            self.name = name
            self.c = _allControls[config[name]]
        def __call__(self):
            return self.c.Position() > 0

        position = property(lambda self: self.c.Position())
        pressed = property(lambda self: self.c.Pressed())

        def __repr__(self):
            return '<Winter control %s>' % self.name

    class PressControl(PosControl):
        def __call__(self):
            return self.c.Pressed()

    if config is None:
        config = defaultConfig

    # Directional controls:
    for name in ('up', 'down', 'left', 'right'):
        globals()[name] = PosControl(name)

    # Buttons
    for name in ('cancel', 'attack1', 'attack2', 'tool1', 'tool2', 'tool3'):
        globals()[name] = PressControl(name)

    # Copy controls over to xi.
    for c in ('up', 'down', 'left', 'right'):
        setattr(controls, c, getattr(controls, c))

    controls.enter = controls.attack1


# global control objects.  These are all set by setConfig
up = down = left = right = cancel = attack1 = attack2 = tool1 = tool2 = tool3 = None

# xi hack
import xi.controls
xi.controls.up = lambda: up()
xi.controls.down = lambda: down()
xi.controls.left = lambda: left()
xi.controls.right = lambda: right()
xi.controls.enter = lambda: attack1()
xi.controls.cancel = lambda: cancel()

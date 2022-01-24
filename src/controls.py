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
  'up': 'UP',
   'down': 'DOWN',
   'left': 'LEFT',
   'right': 'RIGHT',
   'cancel': 'ESCAPE',
   'attack1': 'SPACE',
   'attack2' : 'F',
   'tool1': 'D',
   'tool2': 'S',
   'tool3': 'A',
    
    
    'joy_up': 'joy0axis1-',
    'joy_down': 'joy0axis1+',
    'joy_left': 'joy0axis0-',
    'joy_right': 'joy0axis0+',
    'joy_cancel': 'joy0button2',
    'joy_attack1': 'joy0button1',
    'joy_attack2' : 'joy0button0',
    'joy_tool1': 'joy0button3',
    'joy_tool2': 'joy0button4',
    'joy_tool3': 'joy0button5',
    
    'ui_up': 'UP',
    'ui_down': 'DOWN',
    'ui_left': 'LEFT',
    'ui_right': 'RIGHT',
    'ui_accept': 'RETURN',
    'ui_cancel': 'ESCAPE'      
}
displayControls = {
   'up': 'UP',
   'down': 'DOWN',
   'left': 'LEFT',
   'right': 'RIGHT',
   'cancel': 'ESCAPE',
   'attack1': 'SPACE',
   'attack2' : 'F',
   'tool1': 'D',
   'tool2': 'S',
   'tool3': 'A',
    
    
    'joy_up': 'None',
    'joy_down': 'None',
    'joy_left': 'None',
    'joy_right': 'None',
    'joy_cancel': 'None',
    'joy_attack1': 'None',
    'joy_attack2' : 'None',
    'joy_tool1': 'None',
    'joy_tool2': 'None',
    'joy_tool3': 'None',
    
    'ui_up': 'UP',
    'ui_down': 'DOWN',
    'ui_left': 'LEFT',
    'ui_right': 'RIGHT',
    'ui_accept': 'RETURN',
    'ui_cancel': 'ESCAPE'      
}

#for mapping joystick buttons to names
buttonmapping = {
'0-': 'Stick Left',
'0+': 'Stick Right',
'1-': 'Stick Up',
'1+': 'Stick Down',
'2-': 'Axis 2-',
'2+': 'Axis 2+',
'3-': 'Axis 3-',
'3+': 'Axis 3+',
'4-': 'Axis 4-',
'4+': 'Axis 4+',
'5-': 'Axis 5-',
'5+': 'Axis 5+',
'6-': 'Axis 6-',
'6+': 'Axis 6+',
'7-': 'Axis 7-',
'7+': 'Axis 7+',
'8-': 'Axis 8-',
'8+': 'Axis 8+',
'9-': 'Axis 9-',
'9+': 'Axis 9+',
'0': 'Button 1',
'1': 'Button 2',
'2': 'Button 3',
'3': 'Button 4',
'4': 'Button 5',
'5': 'Button 6',
'6': 'Button 7',
'7': 'Button 8',
'8': 'Button 9',
'9': 'Button 10',
'10': 'Button 11',
'11': 'Button 12',
'13': 'Button 13',
'14': 'Button 14',
'15': 'Button 15',
'16': 'Button 16',
'17': 'Button 17',
'18': 'Button 18',
'19': 'Button 19',
'20': 'Button 20'
}

useGamePad = False


def init():
    '''Fill up _allControls.'''
    global useGamePad, firstrun
    
    # Null control
    _allControls['none'] = lambda: False

    # keyboard keys:
    for k in _keyNames:
        _allControls[k] = ika.Input.keyboard[k]

    # joystick:
    if len(ika.Input.joysticks) > 0:    
        ika.Log(str(len(ika.Input.joysticks)) +' gamepad(s) found:')
            
        for joyIndex, joy in enumerate(ika.Input.joysticks):

            # joystick axes:
            for axisIndex, axis in enumerate(joy.axes):
                _allControls['joy%iaxis%i+' % (joyIndex, axisIndex)] = axis
            for axisIndex, axis in enumerate(joy.reverseaxes):
                _allControls['joy%iaxis%i-' % (joyIndex, axisIndex)] = axis

            # joystick buttons:
            for buttonIndex, button in enumerate(joy.buttons):
                _allControls['joy%ibutton%i' % (joyIndex, buttonIndex)] = button

        useGamePad = True #got this far - presumably this worked!
        
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
            return self.c.Position() > 0.5

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
    for name in ('up', 'down', 'left', 'right', 'joy_up', 'joy_down', 'joy_right', 'joy_left'):
        globals()[name] = PosControl(name)

    #Dedicated UI controls
    for name in ('ui_up', 'ui_down', 'ui_left', 'ui_right'):
        globals()[name] = PosControl(name)

    # Buttons
    for name in ('cancel', 'attack1', 'attack2', 'tool1', 'tool2', 'tool3'):
        globals()[name] = PressControl(name)
        globals()['joy_'+name] = PressControl('joy_'+name)

    for name in ('ui_accept', 'ui_cancel'):
        globals()[name] = PressControl(name)

    # Copy controls over to xi.
    #for c in ('up', 'down', 'left', 'right'):
    for c in ('up', 'down', 'left', 'right', 'joy_up', 'joy_down', 'joy_left', 'joy_right', 
            'ui_up', 'ui_down', 'ui_left', 'ui_right', 'ui_accept', 'ui_cancel'):    
        setattr(controls, c, getattr(controls, c))

    controls.enter = controls.attack1
    controls.joy_enter = controls.joy_attack1
  


# global control objects.  These are all set by setConfig
up = down = left = right = cancel = attack1 = attack2 = tool1 = tool2 = tool3 = None
joy_up = joy_down = joy_left = joy_right = joy_cancel = joy_attack1 = joy_attack2 = joy_tool1 = joy_tool2 = joy_tool3 = None
ui_up = ui_down = ui_left = ui_right = ui_accept = ui_cancel = None

# xi hack
import xi.controls
xi.controls.up = lambda: up()
xi.controls.down = lambda: down()
xi.controls.left = lambda: left()
xi.controls.right = lambda: right()
xi.controls.enter = lambda: attack1()
xi.controls.cancel = lambda: cancel()

# Input control abstraction
# Coded by Andy Friesen
# Copyright whenever.  All rights reserved.
#
# This source code may be used for any purpose, provided that
# the original author is never misrepresented in any way.
#
# There is no warranty, express or implied on the functionality, or
# suitability of this code for any purpose.

import ika

up = lambda: ika.Input.up.Position() > 0
down = lambda: ika.Input.down.Position() > 0
left = lambda: ika.Input.left.Position() > 0
right = lambda: ika.Input.right.Position() > 0
enter = lambda: ika.Input.enter.Pressed()
cancel = lambda: ika.Input.cancel.Pressed()

joy_up = lambda: ika.Input.up.Pressed()
joy_down = lambda: ika.Input.down.Pressed()
joy_left = lambda: ika.Input.left.Pressed()
joy_right = lambda: ika.Input.right.Pressed()
joy_enter = lambda: ika.Input.enter.Pressed()
joy_cancel = lambda: ika.Input.cancel.Pressed()

ui_up = lambda: ika.Input.up.Pressed()
ui_down = lambda: ika.Input.down.Pressed()
ui_left = lambda: ika.Input.left.Pressed()
ui_right = lambda: ika.Input.right.Pressed()
ui_accept = lambda: ika.Input.enter.Pressed()
ui_cancel = lambda: ika.Input.cancel.Pressed()


import aries


FILE = 'game.cfg'

# copy game.cfg into module globals():
globals().update(aries.Document(FILE).process().toDict())

FRAME_RATE = int(FRAME_RATE)
MAX_SKIP_COUNT = int(MAX_SKIP_COUNT)
TILE_WIDTH = int(TILE_WIDTH)
TILE_HEIGHT = int(TILE_HEIGHT)
START_X = int(START_X) * TILE_WIDTH
START_Y = int(START_Y) * TILE_HEIGHT
START_POSITION = (START_X, START_Y)

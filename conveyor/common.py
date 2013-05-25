def enum(*sequential, **named):
    ''' Creates a Python enum!
    '''
    enums = dict(zip(sequential, range(len(sequential))), **named)
    return type('Enum', (), enums)

DIRECTION = enum('Up', 'Down', 'Left', 'Right')

MOUSESCROLLDOWN = 5
MOUSESCROLLUP = 4
ZOOM = enum ('In', 'Out')

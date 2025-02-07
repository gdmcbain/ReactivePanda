from pythonfrp import Globals
from pythonfrp.Types import *
from pythonfrp import Numerics
from pythonfrp import World
from PandaFRP.PandaColor import gray


def updateColor(self):
    c = self._get("color")
    if (c is not None):
        base.setBackgroundColor(c.r, c.g, c.b)  # What is base?
        
def _initWorld():
    print("Inside world signals")
    World.addSignal("color", gray, colorType, updateColor)
    World.addSignal("gravity", Numerics.p3(0, 0, -1), p3Type, lambda x: None)

_initWorld()
world = World.world
# This is confusing, and maybe needs to be changed: World.world is
# an instance of the World class inside the World module
# World.addSignal is inside the World module, but not the World class. world, defined here, is a pointer for the rest
# of the engine. Should we re-name this? There are a lot of worlds, and it took me a while to figure them out.


def resetWorld(continueFn=lambda: None):
    World.resetWorld(continueFn, _initWorld)
    # Should we export this through engine somehow?
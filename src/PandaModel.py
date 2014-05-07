# This defines an object that appears on the screen whose representation is obtained from a
# 3-D model in an egg file from the Panda-3D engine.  These have the following reactive parameters:
#   position  P3      location in 3-space
#   hpr       HPR     orientation in 3-space
#   scale     scalar  relative size (1 = unit cube)
#   color     Color   dynamic texture (None = model skin, otherwise = color of object)

from direct.actor import Actor
import direct.directbase.DirectStart
from panda3d.core import Filename
from Engine import *
from Signal import *
from Proxy import *
from Numerics import *
from Functions import degrees
from StaticNumerics import pi
from Globals import pandaPath
import FileIO
import FileSearch

# This fills in all of the defaults
parameterCache = {}
defaultModelParameters = {"localPosition" : SP3(0,0,0),
                          "localSize" : 0.05,
                          "localOrientation" : SHPR(0,.25,0),
                          "joints" : [],
                          "animations" : None,
                          "defaultAnimation" : None,
                          "frame" : None,
                          "cRadius" : 1,
                          "cFloor" : 0,
                          "cTop" : 1,
                          "cType" : "cyl"}

pandaParameters = { "localSize" : 0.05,
                    "localPosition" : SP3( 0, 200, 0),
                    "localOrientation" : SHPR(0, 0, 0)}
def pandaModel(fileName = None, size = None, hpr = None, position = None, collections = []):
    return PandaModel(  fileName, size, hpr, position, collections)
class PandaModel(Proxy):
    def __init__(self, fileName, size, hpr, position, collections):
        Proxy.__init__(self, name = str(fileName)+"-gID: "+str(Globals.nextModelId), updater = updater, 
        types = {"position": p3Type, "hpr": hprType ,"localSize": numType})
        #(p3Type, SP3(0,0,0)), "hpr": (hprType, SHPR(0,0,0)), "size": (numType, 1)})
        Globals.nextModelId = Globals.nextModelId + 1
        self._mFile = FileSearch.fileSearch(fileName, "models",["egg"])
        #print "Object Name: "+ str(fileName)+"-gID: "+str(Globals.nextModelId);
        if self._mFile is None:
            print "Can't find model " + repr(fileName)
            self._mFile = Filename(pandaPath + "models/"+fileName)
            #self._mParams = pandaParameters
            self._mParams = pandaParameters
        #self._mFile = Filename("/c/Panda3D-1.8.1/models/"+fileName)
        #print "File Path: " + repr(mFile)
        elif fileName in parameterCache:
            self._mParams = parameterCache[fileName]
        else:
            mParamFile = Filename(self._mFile)
            #print repr(mParamFile)
            mParamFile.setExtension("model")
            if mParamFile.exists():
                self._mParams = FileIO.loadDict(mParamFile,types = self._types,  defaults = defaultModelParameters)
            else:
                print "No .model for " + str(fileName)
                self._mParams = defaultModelParameters
            parameterCache[fileName] = self._mParams
        self._pandaModel = loader.loadModel(self._mFile)
        self._onScreen = False
        self._size=self._mParams['localSize']
        self._hpr=self._mParams['localOrientation']
        self._position=self._mParams['localPosition']
        self._cRadius = float(self._mParams['cRadius'])
        self._cType = self._mParams['cType']
        self._cFloor = self._mParams['cFloor']
        self._cTop = self._mParams['cTop']
        self.size = 1
        self.position = P3(1,1,1)
        self.hpr = HPR(0,0,0)
        if position is not None:
            self.position = position
        if hpr is not None:
            self.hpr = hpr
        if size is not None:
            self.size = size
        showModel(self)#This call needs to move into the updater method. We don't have it working with the engine yet.
        for tag in collections:
            try:
                Globals.collections[tag].append(self)
            except KeyError:
                Globals.collection[tag] = []
                Globals.collections[tag].append(self)
    def touches(self, handle, trace = False):
        if trace:
           print "Touch: " + repr(self) + " (" + self._cType + ") " + repr(handle) + " (" + handle._cType + ")"
        #print (repr(self._cRadius))
        #print (repr(self.get("size")))
        mr = self._cRadius * self.get("size")
        mp = self.get("position")
        yr = handle.cRadius*handle.get("size")
        yp = handle.get("position")
        if trace:
            print repr(mp) + " [" + repr(mr) + "] " + repr(yp) + " [" + repr(yr) + "]"
        if self._cType == "sphere":
            if handle._cType == "sphere":
                return absP3(subP3(mp, yp)) < mr + yr
            elif handle._cType == "cyl": # Test if the x,y points are close enough. This treats the sphere as a cylinder
                d = absP2(subP2(P2(mp.x, mp.y), P2(yp.x, yp.y)))
                if d > mr + yr:
                    return False
                else:
                    cb = yp.z + handle.self.get("size")*handle._cFloor
                    ct = yp.z + handle.self.get("size")*handle._cTop
                    sb = mp.z-mr
                    st = mp.z+mr
                    # print str(cb) + " " + str(ct) + " " + str(sb) + " " + str(st)
                    if ct > sb and cb < st:
                        return True
                    else:
                        return False
        elif self._cType == "cyl":
            if handle._cType == "sphere":
                d = absP2(subP2(P2(mp.x, mp.y), P2(yp.x, yp.y)))
                # print "c to s (dist = " + str(d) + ")"
                if d > mr + yr:
                    return False
                else:
                    cb = mp.z + self.get("size")*self._cFloor
                    ct = mp.z + self.get("size")*self._cTop
                    sb = yp.z-yr
                    st = yp.z+yr
                    # print str(cb) + " " + str(ct) + " " + str(sb) + " " + str(st)
                    return ct > sb and cb < st
            elif handle._cType == "cyl":
                # print str(mp.x) + " , " + str(mp.y)
                d = absP2(subP2(P2(mp.x, mp.y), P2(yp.x, yp.y)))
                if trace:
                    print "c to c (dist = " + str(d) + ") " + str(mr+yr)
                if d > mr + yr:
                    return False
                else:
                    res = self._cTop + mp.z > handle._cFloor + yp.z and self._cFloor + mp.z < handle._cTop + yp.z
                    if trace:
                        print "Result: " + str(res) + " " + str((self._cTop, mp.z, handle._cFloor, yp.z, self._cFloor, handle._cTop))
                    print ("*****"+repr(res))
                    return res

def updater(self):
    #These parameters find the static offset which was created during initialization and the current position which is returned by the self.get() method
    positionOffset = self._position
    positionNow = self.get("position")
    sizeScalar = self.get("size")
    sizeOffset = self._size
    hprOffset = self._hpr
    hprNow = self.get( "hpr")
    
    #This is the actual updates to position/size/hpr etc.
    if Globals.eventSignals is not None: 
            for signal in Globals.events:
                print repr(signal)
    
    
    print "size signal: "+repr(sizeScalar)+"  offset size: "+repr(sizeOffset)
    self._pandaModel.setScale(sizeScalar*sizeOffset)
    self._pandaModel.setPos(positionNow.x + positionOffset.x*sizeScalar,
                            positionNow.y + positionOffset.y*sizeScalar,
                            positionNow.z + positionOffset.z*sizeScalar)
                            
     
    self._pandaModel.setHpr(degrees(hprNow.h + hprOffset.h),
                            degrees(hprNow.p + hprOffset.p),
                            degrees(hprNow.r + hprOffset.r))
 
def showModel(self):
    if not self._onScreen:
           self._pandaModel.reparentTo(render)
           self._onScreen = True

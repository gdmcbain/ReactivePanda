from PandaSRC.Panda import *

#This test...

grassScene()

dragon(position = p3(-3,5,-2), hpr=hpr(-5,0,0), size=4)
bee(position = p3(1.1*sin(integral(2, 0)-pi) , -1.1*cos(integral(2, 0)-pi), -0.88), hpr = hpr(integral(2, 0),0,0), color= cyan, size = .5)
panda(position = p3(0,0,-1), hpr = hpr(integral(2, 0),10,0), color=pink)
fireish(position = p3(0,0,-1.5), size = .15)
fireish(position = p3(2,5,3), size = .15)
#launchCamera("medevil")

#def reset(m,v):

#react(b, leftClick(b), reset)


start()

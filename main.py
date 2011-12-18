import sys, pygame
from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin
from os import chdir
import resources.objloader as ol

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
 
glLightfv(GL_LIGHT0, GL_POSITION,  (-40, 200, 100, 0.0))
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.2, 0.2, 0.2, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (0.5, 0.5, 0.5, 1.0))
glEnable(GL_LIGHT0)
glEnable(GL_LIGHTING)
glEnable(GL_COLOR_MATERIAL)
glEnable(GL_DEPTH_TEST)
glShadeModel(GL_SMOOTH)           # most obj files expect to be smooth-shaded
 
# LOAD OBJECT AFTER PYGAME INIT
 
clock = pygame.time.Clock()
 
glMatrixMode(GL_PROJECTION)
glLoadIdentity()
width, height = viewport
gluPerspective(90.0, width/float(height), 1, 100.0)
glEnable(GL_DEPTH_TEST)
glMatrixMode(GL_MODELVIEW)
glEnable(GL_CULL_FACE)
glCullFace(GL_BACK)
glEnable(GL_COLOR_MATERIAL)

def makeFace():
    glBegin(GL_POLYGON)
    glNormal3f(0,0,1)
    glVertex3f(-0.5,0.5,0)
    glVertex3f(-0.5,-0.5,0)
    glVertex3f(0.5,-0.5,0)
    glVertex3f(0.5,0.5,0)
    glEnd()

rx, ry = (0,0)
tx, ty = (0,0)
zpos = 10
rotate = move = False

glq = gluNewQuadric()

def makeCube():
    glColor(0,1,0)
    glPushMatrix()
    glTranslate(0,0,0.5)
    makeFace()
    glPopMatrix()
    
    glColor(0,1,1)
    glPushMatrix()
    glTranslate(0.5, 0, 0)
    glRotate(90, 0, 1, 0)
    makeFace()
    glPopMatrix()
    
    glColor(1,0,1)
    glPushMatrix()
    glTranslate(-0.5, 0, 0)
    glRotate(-90, 0, 1, 0)
    makeFace()
    glPopMatrix() 
 
    glColor(1,0,0)
    glPushMatrix()
    glTranslate(0, 0, -0.5)
    glRotate(180, 0, 1, 0)
    makeFace()
    glPopMatrix()
    
    glColor(1,1,0)
    glPushMatrix()
    glTranslate(0, 0.5, 0)
    glRotate(-90, 1, 0, 0)
    makeFace()
    glPopMatrix()
    
    glColor(0,0,1)
    glPushMatrix()
    glTranslate(0,-0.5,0)
    glRotate(90, 1, 0, 0)
    makeFace()
    glPopMatrix()

angle = 0

chdir("resources/props/")
obj1 = ol.OBJ("pencilpot.obj", swapyz=True)
chdir("../../")

while 1:
    clock.tick(30)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum( -4/3*.04, 4/3*.04, -.04, .04, .1, 200.0 )

    objx = angle - 20
    objy = cos(angle)*4
    angle += 0.1
    
    glMatrixMode( GL_MODELVIEW )
    glLoadIdentity()
    gluLookAt(0, 0, 4, 
              0, 0, 0, 
              0, 1, 0)
    
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == MOUSEBUTTONDOWN:
            if e.button == 4: zpos = max(1, zpos-1)
            elif e.button == 5: zpos += 1
            elif e.button == 1: rotate = True
            elif e.button == 3: move = True
        elif e.type == MOUSEBUTTONUP:
            if e.button == 1: rotate = False
            elif e.button == 3: move = False
        elif e.type == MOUSEMOTION:
            i, j = e.rel
            if rotate:
                rx += i
                ry += j
            if move:
                tx += i
                ty -= j
    
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    
    glPushMatrix()
    glColor(1,1,1)
    glDisable(GL_CULL_FACE)
    glEnable(GL_NORMALIZE)
    glScale(0.3,0.3,0.3)
    glRotate(-90,1,0,0)
    glCallList(obj1.gl_list)
    glDisable(GL_NORMALIZE)
    glEnable(GL_CULL_FACE)
    glPopMatrix()
    
    glPushMatrix()
    glTranslate(objx, objy, 0)
    makeCube()
    glPopMatrix()
    
    pygame.display.flip()

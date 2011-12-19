import sys, pygame

from pygame.locals import *
from pygame.constants import *
from OpenGL.GL import *
from OpenGL.GLU import *
from math import cos, sin
from os import chdir
import resources.objloader as ol
import resources.sounds as snd
from resources.sounds.soundengine import SoundEngine
from resources.maps import readmap as rm

pygame.init()
viewport = (800,600)
hx = viewport[0]/2
hy = viewport[1]/2
srf = pygame.display.set_mode(viewport, OPENGL | DOUBLEBUF)
 
glq = gluNewQuadric()
gluQuadricDrawStyle(glq, GLU_FILL);
gluQuadricNormals(glq, GLU_SMOOTH);
gluQuadricOrientation(glq, GLU_INSIDE);
gluQuadricTexture(glq, GL_TRUE);
 
light0pos = [0, 0, 5, 1]
glLightfv(GL_LIGHT0, GL_POSITION, light0pos)
glLightfv(GL_LIGHT0, GL_AMBIENT, (0.01, 0.01, 0.01, 1.0))
glLightfv(GL_LIGHT0, GL_DIFFUSE, (1.0, 1.0, 1.0, 1.0))
glLightfv(GL_LIGHT0, GL_SPECULAR, (0.7, 0.7, 0.7, 1.0))
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
    
def loadTexture(filename):
    surf = pygame.image.load(filename)
    image = pygame.image.tostring(surf, 'RGBA', 1)
    ix, iy = surf.get_rect().size
    texid = glGenTextures(1)
    glBindTexture(GL_TEXTURE_2D, texid)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MIN_FILTER, GL_LINEAR)
    glTexParameteri(GL_TEXTURE_2D, GL_TEXTURE_MAG_FILTER, GL_LINEAR)
    glTexImage2D(GL_TEXTURE_2D, 0, GL_RGBA, ix, iy, 0, GL_RGBA, GL_UNSIGNED_BYTE, image)
    
    return texid

def crossProduct(x1, y1, z1, x2, y2, z2):
    return [y1*z2-z1*y2, z1*x2-x1*z2, x1*y2-y1*x2]

def computeNormals(Neighbors):
    x1,y1,z1,x2,y2,z2,x3,y3,z3,x4,y4,z4 = Neighbors
    
    xf1, yf1, zf1 = crossProduct(x1,y1,z1,x2,y2,z2)
    xf2, yf2, zf2 = crossProduct(x2,y2,z2,x3,y3,z3)
    xf3, yf3, zf3 = crossProduct(x3,y3,z3,x4,y4,z4)
    xf4, yf4, zf4 = crossProduct(x4,y4,z4,x1,y1,z1)
    
    return [-(xf1+xf2+xf3+xf4), -(xf1+yf2+yf3+yf4), -(zf1+zf2+zf3+zf4)]

def getValue(depthMap, x, y):
    
    if x >= 0 and x < len(depthMap[0]) and y >= 0 and y < len(depthMap):
        return depthMap[y][x]
    
    return 0

def generateTerrain(depthMap, texture, texXReps, texYReps):
    gl_list = glGenLists(1)
    glNewList(gl_list, GL_COMPILE)
    glEnable(GL_TEXTURE_2D)
    glFrontFace(GL_CCW)
    glBindTexture(GL_TEXTURE_2D, texture)
    texDeltaX = float(texXReps)/(len(depthMap[0]) - 1)
    texDeltaY = float(texYReps)/(len(depthMap) - 1)
    currentDeltaY = 0
    currentDeltaX = 0
    
    for y in range(len(depthMap) - 1):
        for x in range(len(depthMap[0]) - 1):
            print x, y, texDeltaX, texDeltaY, currentDeltaX, currentDeltaY
            
            glBegin(GL_TRIANGLE_FAN)
            
            normals = computeNormals([x, depthMap[y][x], y,
                                      x+1, depthMap[y][x+1], y,
                                      x+1, depthMap[y+1][x+1], y+1,
                                      x, depthMap[y+1][x], y+1
                                      ])
            
            print "Middle ", normals
            
            glNormal(normals[0], normals[1], normals[2])
            
            glTexCoord(currentDeltaX+texDeltaX/2., currentDeltaY+texDeltaY/2.)
            glVertex(x+0.5,
                    max(depthMap[y][x], depthMap[y][x+1], depthMap[y+1][x], depthMap[y+1][x+1])/2., 
                     y+0.5)
            
            
            
            firstnormals = computeNormals([x-1, getValue(depthMap, x-1, y), y,
                                      x, getValue(depthMap, x, y-1), y-1,
                                      x+1, getValue(depthMap, x+1, y), y,
                                      x, getValue(depthMap, x, y+1), y+1
                                      ])
            print "Top left ", firstnormals
            glNormal(firstnormals[0], firstnormals[1], firstnormals[2])
            glTexCoord(currentDeltaX, currentDeltaY)
            glVertex(x, depthMap[y][x], y)
            
            
            normals = computeNormals([x-1, getValue(depthMap, x-1, y+1), y+1,
                                      x, getValue(depthMap, x, y+1-1), y+1-1,
                                      x+1, getValue(depthMap, x+1, y+1), y+1,
                                      x, getValue(depthMap, x, y+1+1), y+1+1
                                      ])
            print "Bottom left ", firstnormals
            glNormal(normals[0], normals[1], normals[2])
            glTexCoord(currentDeltaX, currentDeltaY + texDeltaY)
            glVertex(x, depthMap[y+1][x], y+1)
            
            normals = computeNormals([x+1-1, getValue(depthMap, x+1-1, y+1), y+1,
                                      x+1, getValue(depthMap, x+1, y+1-1), y+1-1,
                                      x+1+1, getValue(depthMap, x+1+1, y+1), y+1,
                                      x+1, getValue(depthMap, x+1, y+1+1), y+1+1
                                      ])
            print "Bottom right ", normals
            glNormal(normals[0], normals[1], normals[2])
            glTexCoord(currentDeltaX + texDeltaX, currentDeltaY + texDeltaY)
            glVertex(x+1, depthMap[y+1][x+1], y+1)
            
            normals = computeNormals([x+1-1, getValue(depthMap, x+1-1, y), y,
                                      x+1, getValue(depthMap, x+1, y-1), y-1,
                                      x+1+1, getValue(depthMap, x+1+1, y), y,
                                      x+1, getValue(depthMap, x+1, y+1), y+1
                                      ])
            print "Top right ", normals
            glNormal(normals[0], normals[1], normals[2])
            glTexCoord(currentDeltaX + texDeltaX, currentDeltaY)
            glVertex(x+1, depthMap[y][x+1], y)
            
            
            glNormal(firstnormals[0], firstnormals[1], firstnormals[2])
            glTexCoord(currentDeltaX, currentDeltaY)
            glVertex(x, depthMap[y][x], y)
            
            
            glEnd()
#            glBegin(GL_POLYGON)
#            
#            glTexCoord(currentDeltaX, currentDeltaY)
#            glVertex(x, depthMap[y][x], y)
#            
#            glTexCoord(currentDeltaX, currentDeltaY + texDeltaY)
#            glVertex(x, depthMap[y+1][x], y+1)
#            
#            glTexCoord(currentDeltaX + texDeltaX, currentDeltaY + texDeltaY)
#            glVertex(x+1, depthMap[y+1][x+1], y+1)
#            
#            glTexCoord(currentDeltaX + texDeltaX, currentDeltaY)
#            glVertex(x+1, depthMap[y][x+1], y)
#            
#            glEnd()
            
            currentDeltaX += texDeltaX
        
        currentDeltaX = 0
        currentDeltaY += texDeltaY
    
    glDisable(GL_TEXTURE_2D)
    glEndList()
    return gl_list

angle = 0

se = SoundEngine()
se.addTrack("resources/sounds/rip.ogg")
se.playTrack("resources/sounds/rip.ogg", None, 5)

chdir("resources/maps/")
gm = rm.GameMap()
gm.parseFile("example.map")
print gm.terrain
chdir("../../")

skyTex = loadTexture("resources/textures/sky.bmp")
grassTex = loadTexture("resources/textures/grass.bmp")

skybox_back = loadTexture("resources/textures/skybox_back.tga")
skybox_bottom = loadTexture("resources/textures/skybox_bottom.tga")
skybox_front = loadTexture("resources/textures/skybox_front.tga")
skybox_left = loadTexture("resources/textures/skybox_left.tga")
skybox_right = loadTexture("resources/textures/skybox_right.tga")
skybox_top = loadTexture("resources/textures/skybox_top.tga")

terrainTex = loadTexture("resources/textures/" + gm.terraintex)
terrainTexXReps = gm.terraintexxreps
terrainTexYReps = gm.terraintexyreps
terrainList = generateTerrain(gm.terrain, terrainTex, terrainTexXReps, terrainTexYReps)

renderObjectStore = {}

gameObjects = []

class GameObject:
    def __init__(self, filename, rotation, scale, position):
        self.visible = True
        self.filename = filename
        self.rotx, self.roty, self.rotz = rotation
        self.scalex, self.scaley, self.scalez = scale
        self.posx, self.posy, self.posz = position
        global renderObjectStore
        if filename not in renderObjectStore.keys():
            glDisable(GL_LIGHTING)
            renderObject = ol.OBJ(self.filename, True)
            glEnable(GL_LIGHTING)
            self.renderObject = renderObject
            renderObjectStore[filename] = renderObject
            
    def render(self):
        if self.visible:
            glDisable(GL_CULL_FACE)
            glPushMatrix()
            glEnable(GL_NORMALIZE)
            glTranslate(self.posx, self.posy, self.posz)
            glScale(self.scalex, self.scaley, self.scalez)
            glRotate(self.rotx, 1, 0, 0)
            glRotate(self.roty, 0, 1, 0)
            glRotate(self.rotz, 0, 0, 1)
            glCallList(renderObjectStore[self.filename].gl_list)
            glPopMatrix()
            glEnable(GL_CULL_FACE)
        

chdir("resources/props/")
for gameObj in gm.objlist:
    print gameObj.objfile
    print gameObj.rotation
    print gameObj.scale
    print gameObj.position
    gameObjects.append(GameObject(gameObj.objfile, gameObj.rotation, gameObj.scale, gameObj.position))
chdir("../../")

while 1:
    clock.tick(30)
    
    glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
    glMatrixMode(GL_PROJECTION)
    glLoadIdentity()
    glFrustum( -4/3*.04, 4/3*.04, -.04, .04, .1, 200.0 )

#    objx = angle - 20
#    objy = cos(angle)*4
#    angle += 0.1
    
    glMatrixMode( GL_MODELVIEW )
    
    glPushMatrix()
    glLoadIdentity()
#    gluLookAt(
#        0,0,0,
#        0,0,4,
#        0,1,0);
    glPushAttrib(GL_ENABLE_BIT)
    glEnable(GL_TEXTURE_2D)
    glDisable(GL_DEPTH_TEST)
    glDisable(GL_LIGHTING)
    glDisable(GL_BLEND)
    glDepthMask(GL_FALSE)
    glCullFace(GL_FRONT)    
    glPushMatrix()          
    glTranslatef(0,0,0)
    glRotatef(ry,1,0,0)
    glRotatef(rx,0,1,0)
    glBindTexture(GL_TEXTURE_2D, skybox_front)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f(  0.5, -0.5, -0.5 )
    glTexCoord2f(1, 0)
    glVertex3f( -0.5, -0.5, -0.5 )
    glTexCoord2f(1, 1)
    glVertex3f( -0.5,  0.5, -0.5 )
    glTexCoord2f(0, 1)
    glVertex3f(  0.5,  0.5, -0.5 )
    glEnd()
 
    glBindTexture(GL_TEXTURE_2D, skybox_left);
    glBegin(GL_QUADS);
    glTexCoord2f(0, 0)
    glVertex3f(  0.5, -0.5,  0.5 )
    glTexCoord2f(1, 0)
    glVertex3f(  0.5, -0.5, -0.5 )
    glTexCoord2f(1, 1)
    glVertex3f(  0.5,  0.5, -0.5 )
    glTexCoord2f(0, 1)
    glVertex3f(  0.5,  0.5,  0.5 )
    glEnd();
    
    glBindTexture(GL_TEXTURE_2D, skybox_back)
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f( -0.5, -0.5,  0.5 )
    glTexCoord2f(1, 0)
    glVertex3f(  0.5, -0.5,  0.5 )
    glTexCoord2f(1, 1)
    glVertex3f(  0.5,  0.5,  0.5 )
    glTexCoord2f(0, 1)
    glVertex3f( -0.5,  0.5,  0.5 )
    glEnd();

    glBindTexture(GL_TEXTURE_2D, skybox_right);
    glBegin(GL_QUADS)
    glTexCoord2f(0, 0)
    glVertex3f( -0.5, -0.5, -0.5 )
    glTexCoord2f(1, 0)
    glVertex3f( -0.5, -0.5,  0.5 )
    glTexCoord2f(1, 1)
    glVertex3f( -0.5,  0.5,  0.5 )
    glTexCoord2f(0, 1)
    glVertex3f( -0.5,  0.5, -0.5 )
    glEnd()
 
    glBindTexture(GL_TEXTURE_2D, skybox_top);
    glBegin(GL_QUADS);
    glTexCoord2f(0, 1)
    glVertex3f( -0.5,  0.5, -0.5 )
    glTexCoord2f(0, 0)
    glVertex3f( -0.5,  0.5,  0.5 )
    glTexCoord2f(1, 0)
    glVertex3f(  0.5,  0.5,  0.5 )
    glTexCoord2f(1, 1)
    glVertex3f(  0.5,  0.5, -0.5 )
    glEnd();
 
    glBindTexture(GL_TEXTURE_2D, skybox_bottom)
    glBegin(GL_QUADS)
    glTexCoord2f(1, 0)
    glVertex3f(  0.5, -0.5, -0.5 )
    glTexCoord2f(1, 1)
    glVertex3f(  0.5, -0.5,  0.5 )
    glTexCoord2f(0, 1) 
    glVertex3f( -0.5, -0.5,  0.5 )
    glTexCoord2f(0, 0) 
    glVertex3f( -0.5, -0.5, -0.5 )
    glEnd()

    glPopMatrix()

    glCullFace(GL_BACK)
    glDepthMask(GL_TRUE)

    
#    glPushAttrib(GL_ENABLE_BIT)
#    glEnable(GL_TEXTURE_2D)
#    glDisable(GL_DEPTH_TEST)
#    glDisable(GL_LIGHTING)
#    glDisable(GL_BLEND)
# 
#    glColor4f(1,1,1,1)
#
#    glBindTexture(GL_TEXTURE_2D, skybox_front)
#    glBegin(GL_QUADS)
#    glTexCoord2f(0, 0)
#    glVertex3f(  0.5, -0.5, -0.5 )
#    glTexCoord2f(1, 0)
#    glVertex3f( -0.5, -0.5, -0.5 )
#    glTexCoord2f(1, 1)
#    glVertex3f( -0.5,  0.5, -0.5 )
#    glTexCoord2f(0, 1)
#    glVertex3f(  0.5,  0.5, -0.5 )
#    glEnd()
# 
#    glBindTexture(GL_TEXTURE_2D, skybox_left);
#    glBegin(GL_QUADS);
#    glTexCoord2f(0, 0)
#    glVertex3f(  0.5, -0.5,  0.5 )
#    glTexCoord2f(1, 0)
#    glVertex3f(  0.5, -0.5, -0.5 )
#    glTexCoord2f(1, 1)
#    glVertex3f(  0.5,  0.5, -0.5 )
#    glTexCoord2f(0, 1)
#    glVertex3f(  0.5,  0.5,  0.5 )
#    glEnd();
#    
#    glBindTexture(GL_TEXTURE_2D, skybox_back)
#    glBegin(GL_QUADS)
#    glTexCoord2f(0, 0)
#    glVertex3f( -0.5, -0.5,  0.5 )
#    glTexCoord2f(1, 0)
#    glVertex3f(  0.5, -0.5,  0.5 )
#    glTexCoord2f(1, 1)
#    glVertex3f(  0.5,  0.5,  0.5 )
#    glTexCoord2f(0, 1)
#    glVertex3f( -0.5,  0.5,  0.5 )
#    glEnd();
#
#    glBindTexture(GL_TEXTURE_2D, skybox_right);
#    glBegin(GL_QUADS)
#    glTexCoord2f(0, 0)
#    glVertex3f( -0.5, -0.5, -0.5 )
#    glTexCoord2f(1, 0)
#    glVertex3f( -0.5, -0.5,  0.5 )
#    glTexCoord2f(1, 1)
#    glVertex3f( -0.5,  0.5,  0.5 )
#    glTexCoord2f(0, 1)
#    glVertex3f( -0.5,  0.5, -0.5 )
#    glEnd()
# 
#    glBindTexture(GL_TEXTURE_2D, skybox_top);
#    glBegin(GL_QUADS);
#    glTexCoord2f(0, 1)
#    glVertex3f( -0.5,  0.5, -0.5 )
#    glTexCoord2f(0, 0)
#    glVertex3f( -0.5,  0.5,  0.5 )
#    glTexCoord2f(1, 0)
#    glVertex3f(  0.5,  0.5,  0.5 )
#    glTexCoord2f(1, 1)
#    glVertex3f(  0.5,  0.5, -0.5 )
#    glEnd();
# 
#    glBindTexture(GL_TEXTURE_2D, skybox_bottom)
#    glBegin(GL_QUADS);
#    glTexCoord2f(0, 0) 
#    glVertex3f( -0.5, -0.5, -0.5 )
#    glTexCoord2f(0, 1) 
#    glVertex3f( -0.5, -0.5,  0.5 )
#    glTexCoord2f(1, 1)
#    glVertex3f(  0.5, -0.5,  0.5 )
#    glTexCoord2f(1, 0)
#    glVertex3f(  0.5, -0.5, -0.5 )
#    glEnd()
 
    glPopAttrib()
    glPopMatrix()
    
    for e in pygame.event.get():
        if e.type == QUIT:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_ESCAPE:
            sys.exit()
        elif e.type == KEYDOWN and e.key == K_r:
            glPolygonMode(GL_FRONT, GL_FILL)
        elif e.type == KEYDOWN and e.key == K_t:
            glPolygonMode(GL_FRONT, GL_LINE)
        elif e.type == KEYDOWN and e.key == K_i:
            light0pos[1]+=0.5
        elif e.type == KEYDOWN and e.key == K_k:
            light0pos[1]-=0.5
        elif e.type == KEYDOWN and e.key == K_j:
            light0pos[0]-=0.5
        elif e.type == KEYDOWN and e.key == K_l:
            light0pos[0]+=0.5
        elif e.type == KEYDOWN and e.key == K_u:
            light0pos[2]-=0.5
        elif e.type == KEYDOWN and e.key == K_h:
            light0pos[2]+=0.5
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
    
    glPushMatrix()
    glTranslate(tx/20., ty/20., - zpos)
    glRotate(ry, 1, 0, 0)
    glRotate(rx, 0, 1, 0)
    
    glPushMatrix()
    glTranslate(light0pos[0],light0pos[1],light0pos[2])
    gluSphere(glq, 0.5, 20, 20)
    glPopMatrix()
    
    glLight(GL_LIGHT0, GL_POSITION, light0pos)
    
    for gameObject in gameObjects:
        gameObject.render()
    
    glEnable(GL_TEXTURE_2D)
    glColor(1,1,1)

    glDisable(GL_TEXTURE_2D)
    
    glCallList(terrainList)
    glPopMatrix()
    
    
#    glPushMatrix()
#    glColor(1,1,1)
#    glDisable(GL_CULL_FACE)
#    glEnable(GL_NORMALIZE)
#    glScale(0.3,0.3,0.3)
#    glRotate(-90,1,0,0)
#    glCallList(obj1.gl_list)
#    glDisable(GL_NORMALIZE)
#    glEnable(GL_CULL_FACE)
#    glPopMatrix()
    
#    glPushMatrix()
#    glTranslate(objx, objy, 0)
#    makeCube()
#    glPopMatrix()
    
    pygame.display.flip()


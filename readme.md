#Ludum Dare 22 Plans

##3D rts, turnbased. 

###Using these frameworks/apis:

* http://pyopengl.sourceforge.net/
* http://pygame.org/

###Using these resources:

* http://opengameart.org/content/abstract-rts-models

##Tools

We have an obj file loader/viewer in the resources folder. You call it with
```
python objviewer.py FILENAMEHERE.obj
```

The viewer will accept mtl files for texturing but make sure they have the texture address set relationally, and *not* absolute.

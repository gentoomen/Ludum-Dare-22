#Ludum Dare 22 Plans

##Ideas
The theme is "Alone"

* A 3D RTS (this was the initial plan, but unsure how to theme this to "Alone"
* FPS, set on the desk where the paper hero's comrades are gone(or dead) and
	he has to survive against the papercraft machines who are still operating
* Paper base defence sim
* "Town Construction" game, where you're the last remaining person in your town and you have to make your town more appealing, to persuade your friends to come back (probably something similar to Animal Crossing?)

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

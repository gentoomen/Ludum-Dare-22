#Documentation

##soundengine.py
The sound engine is incredibly simple and serves just to add to the functionality of pygame.mixer. It should be obvious the purpose of each function, but this serves as a quick reference if needed:

####SoundEngine.playTrack(songname *string*, time=None *int*, loop=0 *int*)

>*songname* The name of the given song within the library.
>
>*time* the time, in seconds, for the song to run. It will be converted to milliseconds.
>
>*loop* the number of times for the sound to loop. Passing 5 will cause it to play once, then loop 5 times. Passing -1 will cause it to play indefinitely until stopTrack() is called.

####SoundEngine.stopTrack(songname *string*, fadeout=False *bool*)

>*songname* The name of the given song within the library.
>
>*fadeout* Describes whether the song fades out, or whether it stops suddenly.

####SoundEngine.setVolume(songname *string*, volume=.5 *float*)

>*songname* the name of the given song within the library.
>
>*volume* a float number describing the volume. Volume has a lower bound of 0.0 (mute) and 1.0 (loudest)

This game was made during a Lua Development + Love2D tutorial and later ported
to Python + Pygame by me. As such there most likely are things that are not very
Pythonic but in the end this is more of a learning experience for me than anything else.

This tutorial was about creating a game of Asteroids with grouping files by functionalities
and making everything a little more OOP-ish. I think.

While this began as a port some differences between Love2D and Pygame made it necessary to
edit a few more things, in particular how the engine renders alpha color channels and the
need to create and blit surfaces together. By far this was the biggest change as it led
to rethinking how the game should handle game objects being drawn more faded during the
paused state.

Other changes merely include RGB colors expressed in tuples ints with range [0..255] instead
of floats between [0..1], passing delta time from the main loop clock instead of calculating
it inside of the other files and delegating the task of adding or removing children to their
parent container (so, for example, a laser doesn't remove itself once it's travelled far
enough; that's a job to the player object who fired it).

The Lua lessons had been followed up until LuaRocks, which for some unknown reason didn't
want to work on my machine. Whether in the windows environment or on Ubuntu via WSL. The
remainder of the Lua tutorial *will* be followed, however any additional code will only
be made on the Python port, not having its equivalent Lua counterpart.

For reference the parts missing from the Lua code will be:
* a score system
* a game over screen
* player invincibility (iframes on respawn I assume)
* infinite levels
* being able to reset the game
* saving the high score
* bgm & sfx

If you have Python 3.9 (unsure if other versions will work) you can run:
```
python3 "src\main.py"
```

Command to build the exe:
```
pyinstaller "src\main.py" --onefile --name asteroids --windowed
```

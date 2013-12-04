README
GENERAL
-------
This project is a grid-based SRPG videogame, similar to Chess/FFTactics/Disgaea.

To play, you must have version 2.69 (current) of Blender, which can be found for free here:
http://www.blender.org/download/
Open “battlefield.blend” with Blender and press p to begin playing.

This game is being produced by Kiva-Entertainment, and is free to download from GitHub.
However, redistribution and/or commercial use is forbidden.
For more information on licensing, see LICENSE

To watch tutorials and other videos, visit the youtube channel:
https://www.youtube.com/channel/UCFDRx42y3uBs-IROz3pMZNQ

CREDIT
------
Specific credit given within folders containing external content

General credit:
Charles Gabriel on openGameArt.org for face images
Henrique Lazarini on openGameArt.org for icon images
Daniel Cook on lostGarden.com for tile images

CONTROLS
--------
When selecting units:
Arrow keys move cardinally
a/d to rotate view
q/e zoom in/out
f Cycle through units acting in current turn (See below)
x End current turn
space select whatever target is over (To view menu/move/make attack target)

When unitMenu is open
Up Move
Left Action select
Down View info
w Deselect unit (Close menu)

In action select/info
Arrow keys to navigate
space Select
w Exit
a/d to raise or lower extent (Makes attacks more significant)

TURNS
------
Units are placed in turn order based on their speed
Speed is between 1 and 100
2 units with speed c (ex: 20) always act on the same turn
A unit with speed 100 acts 4x as often as one with speed 25
(In the above case, the unit w speed 25 always acts on the same turn as the one with 100, but the 100 has 3 additional turns by itself)
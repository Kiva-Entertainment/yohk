README
GENERAL
-------
This project is a grid-based SRPG videogame, similar to Chess/FFTactics/Disgaea/Fire-Emblem.

To play, you must have version 2.69 (current) of Blender, which can be downloaded for free here:
http://www.blender.org/download/
Open battlefield.blend with Blender and press p to begin playing.

This game is being produced by Kiva-Entertainment, and is free to download from GitHub.
However, redistribution and/or commercial use is forbidden.
For more information on licensing, see LICENSE.

It is highly recommended that you download the latest stable release.
All releases can be found here:
https://github.com/Kiva-Entertainment/yohk/releases

To watch game matches, tutorials, and other videos, visit our Youtube channel:
https://www.youtube.com/channel/UCFDRx42y3uBs-IROz3pMZNQ

To discuss the game and get the latest news, visit this game’s thread:
http://blenderartists.org/forum/showthread.php?319877-Yohk-SRPG-wip


CREDIT
------
All credit for external resources given in the directory that contains the resource


CONTROLS
--------
Arrow keys	Move
Space key	Select
W Key		Deselect/Exit/Undo
X Key		End turn
A/D keys	Rotate view
		Raise/Lower extent while selecting a command that extends (See <i>Extent</i>)
F/G Keys	Move cursor to next valid unit
		G is stricter (While selecting units to act, only move to units with actions remaining, F moves to units with actions OR movement left)
		G maximizes extent while selecting a command that extends (See <i>Extent</i>)
Q/E keys	Zoom in/out
I key		View unit info
M key		Mute
Esc key		Exit game


VICTORY
-------
In this demo, it is up to the players to decide when one team has won
You could decide that a player wins once they have remove all of their enemies from the field (This can take a long time)
You could also decide that a player wins after they’ve defeated N of their opponent’s units
It is up to you to decide when the match is over


EXTENT
------
Some skills have something called “extent”
When you use a skill, you can spend more sp to raise the extent of the skill
This makes the skill more substantial in some way (Greater range, greater damage, etc.)
To raise extent, press “D” to raise it by 1, or “G” to raise it as high as possible
To lower extent, press “A” to lower it by 1

Spending just the right amount on each skill is essential to ensuring your victory


TURNS
------
Units act in turns
Units act more frequently if they have higher speed
In this demo, all units have same speed, except for bases, which have 1/10th the number of turns that other units have


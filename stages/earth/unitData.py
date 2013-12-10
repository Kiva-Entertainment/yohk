{ 'active' :
[
	{	'position' : [6,13],
		'model' : 'base',
		'name' : 'Holy Ground',
		'align' : 'solarServants',
		'health' : 1000,
		'hp' : 1000,
		'spirit' : 0,
		'sp' : 0,
		'move' : 0,
		'mv' : 0,
		'actions' : 1,
		'act' : 1,
		'strength' : 0,
		'intelligence' : 0,
		'toughness' : 100,
		'willpower' : 100,
		'focus' : 0,
		'agility' : 0,
		'speed' : 1,
		'jump' : 0,
		'regen' : 0,
		'commands' : [['deploy', 'slash']]
	},
	{	'position' : [6,0],
		'model' : 'base',
		'name' : 'Base Camp',
		'align' : 'martialLegion',
		'health' : 1000,
		'hp' : 1000,
		'spirit' : 0,
		'sp' : 0,
		'move' : 0,
		'mv' : 0,
		'actions' : 1,
		'act' : 1,
		'strength' : 0,
		'intelligence' : 0,
		'toughness' : 100,
		'willpower' : 100,
		'focus' : 0,
		'agility' : 0,
		'speed' : 1,
		'jump' : 0,
		'regen' : 0,
		'commands' : [['deploy']]
	},
	{	'position' : [6,2],
		'model' : 'barrel',
		'name' : 'Barrel',
		'align' : 'neutral',
		'health' : 200,
		'hp' : 200,
		'spirit' : 0,
		'sp' : 0,
		'move' : 0,
		'mv' : 0,
		'actions' : 0,
		'act' : 0,
		'strength' : 0,
		'intelligence' : 0,
		'toughness' : 10,
		'willpower' : 0,
		'focus' : 0,
		'agility' : 0,
		'speed' : 0,
		'jump' : 0,
		'regen' : 0,
		'commands' : [[]]
	}
],
'inactive' :
[
	{	'model' : 'soldier',
		'name' : 'Shino, Blood Dancer',
		'align' : 'martialLegion',
		'health' : 1100,
		'hp' : 1100,
		'spirit' : 400,
		'sp' : 0,
		'move' : 5,
		'mv' : 5,
		'actions' : 1,
		'act' : 1,
		'strength' : 120,
		'intelligence' : 70,
		'toughness' : 120,
		'willpower' : 60,
		'focus' : 110,
		'agility' : 90,
		'speed' : 10,
		'jump' : 12,
		'regen' : 5,
		'commands' :	[['slash', 'kick', 'gorgonSlash'],
						['ribbonDash', 'predatorsDescent', 'ebber'],
						['dash', 'rush', 'sneak']]
	},
	{ 	'model' : 'soldier',
		'name' : 'Ichi, the Masochist',
		'align' : 'martialLegion',
		'health' : 1100,
		'hp' : 1100,
		'spirit' : 400,
		'sp' : 0,
		'move' : 5,
		'mv' : 5,
		'actions' : 1,
		'act' : 1,
		'strength' : 120,
		'intelligence' : 70,
		'toughness' : 120,
		'willpower' : 60,
		'focus' : 110,
		'agility' : 90,
		'speed' : 10,
		'jump' : 12,
		'regen' : 5,
		'commands' : 	[['chop', 'quakeImpact', 'grandSwath'],
						['skullShatter', 'murderTwist', 'concentratedChaos'],
						['bloodRitual', 'bloodlust', 'riteOfImmortality']] # Iron maiden
	},
	{	'model' : 'devoted',
		'name' : 'Urchin, the Summoner',
		'align' : 'solarServants',
		'health' : 800,
		'hp' : 800,
		'spirit' : 700,
		'sp' : 0,
		'move' : 4,
		'mv' : 4,
		'actions' : 1,
		'act' : 1,
		'strength' : 40,
		'intelligence' : 120,
		'toughness' : 60,
		'willpower' : 120,
		'focus' : 110,
		'agility' : 90,
		'speed' : 10,
		'jump' : 10,
		'regen' : 7,
		'commands' : 	[['psiStrike', 'flameBarrage', 'meteor'],
						['birdcall', 'stoneGarden', 'divineReflection'],
						['tutor', 'stoneArmor', 'emogen']]
	},
	{	'model' : 'devoted',
		'name' : 'Lish, Sorrowmancer',
		'align' : 'solarServants',
		'health' : 800,
		'hp' : 800,
		'spirit' : 700,
		'sp' : 0,
		'move' : 4,
		'mv' : 4,
		'actions' : 1,
		'act' : 1,
		'strength' : 40,
		'intelligence' : 120,
		'toughness' : 60,
		'willpower' : 120,
		'focus' : 110,
		'agility' : 90,
		'speed' : 10,
		'jump' : 10,
		'regen' : 7,
		'commands' : 	[['psiStrike', 'mudshot', 'aeroImpact'],
						['earthGrip', 'icePrison'],
						['study', 'stoneArmor', 'emogen']]
	}
]
}

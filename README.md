# LoLAbilityGuessingGame
A python program that randomly shows the names of abilites of all champions from League Of Legends to let you or your friends guess.
It has a GUI (tkinter) and a built-in timer (default: 20s) which lets you or your friends guess the champion name and the ability slot (Passive, Q, W, E or R).
It takes a JSON-file as input where I stored all the champion names and their corresponding abilites.
The JSON file is not created by this program, but by another python script which I run manually every time a new champion is released or something else changes (like champion reworks, VGUs, ...).

The dependencies in the manifest are not all necessary, but since the sript for the creation of the JSON-file and the Guessing Game are in the same project folder, I can only provide a shared dependency manifest at this point.

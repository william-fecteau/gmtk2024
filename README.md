# Overflow
A puzzle game about math and breaking stuff.

Hope you didn't sleep through your math class!

This project was made in 48h during the GMTK 2024 game jam.

## How to play the game

### Built binaries
[Windows](https://github.com/william-fecteau/gmtk2024/releases/download/1.0/overflow-windows.exe) 

[Linux](https://github.com/william-fecteau/gmtk2024/releases/download/1.0/overflow-linux) 

### With python directly
**Pre-requisite: Python 3.10**

1. Clone this repo
```
git clone https://github.com/william-fecteau/gmtk2024
cd gtmk2024
```
3. Install python requirements
```bash
pip install -r requirements.txt
```
3. Launch the game
```bash
python game.py
```

### Building binaries

**Pre-requisite: Follow all the steps from the last section to install the necessary dependencies**

#### Windows
```bash
./build_windows.bat
```

#### Linux
```bash
chmod +x build_linux.bash
./build_linux.bash
```

## Meet the team
Parazytee - Level design, Music, Sound effects, Art

AggroBane - Programming, Input parser, UI, fix monkiBrain's code

MonkiBrain -  Programming, Card snaps, Optimisation

02Zack - Programming, lots of UI

PsychoPatt - Programming, cutscenes, bug fixes

Th3Bos5 - Programming, Sand simulation

Seraphii - Art

## Known Issues

Factorials allow non-integers parameter (sympy auto completes with the gamma function :~] ).

Level 25-28 are therefore a lot easier to complete.

Have fun!

pyinstaller -n "Overflow" --onefile --noconsole --icon="res/shnake.ico" --add-data="res/*:res/" --add-data="res/credits/*:res/credits/" --add-data="res/MenuImg/*:res/MenuImg/" --add-data="res/worlds/0/*:res/worlds/0/" --add-data="res/worlds/1/*:res/worlds/1/" --add-data="res/worlds/2/*:res/worlds/2/" --add-data="res/worlds/3/*:res/worlds/3/" --add-data="res/worlds/*:res/worlds/" --add-data="res/worlds/4/*:res/worlds/4/" ./game.py
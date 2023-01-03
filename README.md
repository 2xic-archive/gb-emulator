(Fixed readme and pushed to github in 2022)

Basic GB emulator based of https://github.com/trekawek/coffee-gb (used as reference) and http://marc.rawer.de/Gameboy/Docs/GBCPUman.pdf

This project was started in december 2018 after reading [http://blog.rekawek.eu/2017/02/09/coffee-gb/](http://blog.rekawek.eu/2017/02/09/coffee-gb/) on Hackernews. 

Mostly written between 2018 december - 2019 february. Should be able to run Tetris :)

Requirements
- sdl2 and sdl2mixer
  - `sudo apt-get install -y libsdl2-mixer-2.0-0`
- `pip install pysdl2`
- `pip install numpy`
- Use `pypy 2.7` since pythonc is slow
  - PyPy is also a bit slow since the emulator is not optimized.

# SpiritMS-Script-Spider
This script crawls through Swordie-style script folders to search for Script Manager method usages.  

This project is adapted from [ascii_checker](https://github.com/TEAM-SPIRIT-Productions/ascii_checker), which was initially made for filtering non-ASCII text from Azure v316 style source code (e.g. [ElectronMS](https://github.com/Bratah123/ElectronMS)).  

---

## How To Use  
1) Configure `config.py`  
    - E.g. `REPOSITORY_ROOT = "E:\Downloads\SpiritMS"`  
2) Run `start.bat`  
3) Provide a method to search for  
    - E.g. Type in `getNX` if you would like to see all usages of the `getNX` method in the scripts  
4) Check the `/output/` folder of this repository, there should be a file corresponding to to your search

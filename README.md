# ReactBot for Linux

## Introduction

This is a simple python script meant to serve as a substitute for ReactBot.exe created by Jacksfilms, Cuyoya, and Camtoonist, written for Linux.
Since the original program was built for Windows in Unity, and not everyone was able to make Wine or Proton compatibility layers work (including me), I thought that a simple script written especially for Linux would be good.
This probably won't work on all Linux Distributions, but I hope it serves as a template for anyone who wants to help adjust it for specific distributions or window environments.
I created this on Linux Mint so hopefully Debian-based distributions should work well.

## Getting started

Note: This program requires root permission. This is because I rely on the `keyboard` module in python, which reads raw device files (/dev/input/inputX) but it requires root. If anyone knows how to read keyboard inputs system-wide without root, please submit a pull request.

I don't know how the "DLC" will be structured when it comes out, but I assume it's a similar setup to what is in the free version, so you probably won't have to do any different steps.

### Dependencies
- VLC
- If the compiled executable does not work for you, Python (which may come with your distro)

### Installation
1. Download [ReactBot.exe](https://jacksfilmscouncil-shop.fourthwall.com/products/reactbot-exe)
2. Extract it out to some directory, I will call this .../ReactBot
3. Download this repo, click Code, Download ZIP, then extract it.
4. Make the `reactbot` executable actually executable: `chmod +x reactbot`
5. Place `reactbot` and `config.json` in the same directory. It does not have to be the same directory as ReactBot
6. In `config.json`, edit "idle" to .../ReactBot/ReactBot_Data/sharedassets0.resource
7. In `config.json`, edit "phrases" to .../ReactBot/ReactBot_Data/StreamingAssets/GrabBag. Do not end the path with a "/"!
8. You can edit "phrase_key" to be whatever you want it to be, or leave it at the default F7
9. You must edit "quit_key": ***The program will not stop if you close the VLC window.*** This leads to a leak of resources, so use the quit_key to exit properly.
10. You can ignore "aout", it's for if you have problems later on.
11. Save and close `config.json`, then run the `reactbot` executable.

## Troubleshooting

### Sound
If you have problems with the vlc output not having any sound, try telling vlc which audio server you are using. Edit aout in the config to a valid aout for vlc, which you can get a list of by running `vlc --list | grep "audio output"`. For example, you can set aout=pulse for pulseaudio.

### General troubleshooting 
- Try running the program from the terminal instead of through the GUI, look for specific error messages, make sure to run with sudo. I put my error messages there, so this should probably be the first thing you do when you start troubleshooting.
- Try running the program directly through python, instead of the pyinstaller version - see the [Contributing](#contributing) instructions
- Ensure you have root access when running the program
- Ensure vlc is installed and in your $PATH, you should be able to run `vlc` in your terminal and a window should appear
- Ask an LLM for help
- make an issue or send me a message idk

## Contributing

Contributions are welcome! Please help me fix my terrible code.

1. Clone the repo
2. Make a venv (virtual environment) directory for the modules: `mkdir venv`
3. Ensure that you are using a virtual environment: `python -m venv ./venv`
4. Get the dependencies: `./venv/bin/pip install keyboard python-vlc`, optionally also get pyinstaller
5. Make your changes
6. Run the program with `sudo ./venv/bin/python main.py`
7. Make a pull request on GitHub
8. If you want to use pyinstaller to make an executable, you probably need to modify vlc.py. Follow along with the instructions at the last comment of [this GitHub issue](https://github.com/pyinstaller/pyinstaller/issues/4506); You'll know if you forgot this if you get some message along the lines of NoneType has no method media_player_new()

# Credits

Thanks to Cuyoya for reacting positively to the original "How to get reactbot on linux" message which encouraged me to actually consider doing this
Thanks to u/MxPrime101 and u/ILikeMinecraft097 on the r/JacksFilms subreddit for making their posts about getting ReactBot on Linux

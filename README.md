# discord-tabu

Taboo about playing Discord?
This is now possible with this Python Discord bot.

Define own terms or let the server users add their own terms. Everything is possible. Easy to understand and simple to implement.

## Installation

**What is needed?**
* Python 3.X
* Discord-Server

**Which Python packages are needed?**
* discord 1.5.X
* matplotlib

**Everything available?**
1. Download all files
2. Set up the bot (settings-file)
3. Add your own terms (terms-file)
4. **And your are ready to play with your friends.**

## Commands


The following commands are only for the following channels.

**Join Channel:**
```
!tabu join                          - Join taboo
!tabu start [points to win]         - Start taboo [A score other than the default to win can be specified]
```

**Team-1 & Team-2 Channel:**
```
!tabu pause                         - Pause the game when changing teams
!tabu unpause                       - Unpause the game when changing teams
```

**Bot-Admin Channel:**
```
!tabu load cards                    - Loads all terms from the Add-Terms Channel (Shutdown the bot once to save it)
!tabu shutdown                      - Shutdown the bot and saves depending on the settings
!tabu shutdown without save         - Shutdown the bot and without saving
!tabu shutdown with save            - Shutdown the bot and with saving
```

## Wishes for new functions?

Make a pull request. :)
I try to realize your wishes.

## Issues found?
Make a pull request.
I try to fix it as soon as possible.

## Help needed?
Make a pull request. :D

## License
All code is under the [MIT](https://choosealicense.com/licenses/mit/) license.

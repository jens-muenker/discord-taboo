# discord-taboo

Taboo about playing Discord?
This is now possible with this Python Discord bot.

Define own terms or let the server users add their own terms. Everything is possible. Easy to understand and simple to implement.

[Not the right game? Try Color-Cards for Discord!](https://github.com/Frosch2010/discord-color-cards)

## Features

<img src="https://github.com/Frosch2010/discord-taboo/blob/main/Screenshots/explainer_react.png" height="290" width="423" align="right">

* The [declarer](https://github.com/Frosch2010/discord-taboo/blob/main/Screenshots/explainer_react.png) and the [opponent team](https://github.com/Frosch2010/discord-taboo/blob/main/Screenshots/team_react.png) control the game through the Reactions

* [Players can add terms without the admin](https://github.com/Frosch2010/discord-taboo/blob/main/Screenshots/ADD-Terms.png)
  * Automatic check whether a term already exists. If so, the forbidden words are added to the term, if they do not exist.
  * Edit-System: Even afterwards, the terms can be edited or deleted again via the Add-Terms channel.

* Multilingual thanks to language file

* After the win: [Graph for the score development](https://github.com/Frosch2010/discord-taboo/blob/main/Screenshots/win_graph.png)
  
* Revenges with the same teams are possible
  
* [Teams](https://github.com/Frosch2010/discord-taboo/blob/main/Screenshots/start_message.png) are created randomly  

* Used terms can be saved. Guarantees that a term will not come back until all others have been used.

* Completely freely configurable

* [Pause](https://github.com/Frosch2010/discord-taboo/blob/main/Screenshots/PauseGame.png) and [unpause](https://github.com/Frosch2010/discord-taboo/blob/main/Screenshots/Waiting.png) the game between a team change


## Installation

**What is needed?**
* Python 3.X
* Discord-Server

**Which Python packages are needed?**
* discord 1.5.X
* matplotlib
* termcolor
* colorama

**Everything available?**
1. Download all files and copy all into the same folder
2. Set up the bot [(settings-file)](https://github.com/Frosch2010/discord-taboo/blob/main/tabu-settings.txt)
3. Set up the [language-file](https://github.com/Frosch2010/discord-taboo/blob/main/tabu-language.txt) - [(Other languages?)](https://github.com/Frosch2010/discord-taboo/tree/main/other-languages)
4. Add your own terms [(terms-file)](https://github.com/Frosch2010/discord-taboo/blob/main/tabu-terms.txt)
5. **And your are ready to play with your friends.**

## Commands


The following commands are only for the following channels.

**Join Channel:**
```
!tabu join                          - Join taboo
!tabu start [points to win]         - Start taboo [A score other than the default to win can be specified]
```

**Team-1 & Team-2 Channel:**
```
!tabu revanche                      - Starts a vote on whether there should be a rematch
!tabu stop                          - Stops the game before a team has won
!tabu pause                         - Pause the game when changing teams
!tabu unpause                       - Unpause the game when changing teams
```

**Add-Terms Channel:**
```
!edit [term]                        - Calls the edit menu, through which a term can be edited
```

**Bot-Admin Channel:**
```
!tabu save                          - Saves the current game state
!tabu kick @Playername              - Kicks player out of the game
!tabu load cards                    - Loads all terms from the Add-Terms Channel (Shutdown the bot once to save it)
!tabu shutdown                      - Shutdown the bot and saves depending on the settings
!tabu shutdown without save         - Shutdown the bot and without saving
!tabu shutdown with save            - Shutdown the bot and with saving
```

## Edit-System

The Edit system is operated with the help of Reactions. The following emojis are available for the following operation:
```
✏️ = Edit the term or a forbidden word
✂️ = Delete a forbidden word
🗑 = Delete the term
✅ = Press this reaction as soon as you are done with the edit
```

## Bot-Permissions

The bot needs the following rights in each channel (Join, Admin etc.):
* view_channel
* send_messages

In the team channels, the following rights are also required:
* manage_messages
* read_message_history
* add_reactions
* attach_files


## Settings-file

```
Join Channel-ID       = Through this channel players can join taboo.
Team-1 Channel-ID     = Channel for team 1.
Team-2 Channel-ID     = Channel for team 2.
Add-Terms Channel-ID  = This channel allows players to add cards on their own. 
                        Scheme: "Term:forbidden word,forbidden word,..."
                        When the bot is online, the terms are automatically added to the game.
                        Otherwise they have to be reloaded with the Load command.
Out-Terms Channel-ID  = Comes in the future. Please specify the same channel as Add-Terms.
Bot-Admin Channel-ID  = Channel for the Bot-Admin commands, like shutdown.

Bot-Token             = Your Bot-Token
Server-ID             = Server-ID/Guild-ID
Default-Save-Terms    = Should the current state of the term pool etc. be saved when the bot is shut down without further arguments.
Save after Auto-ADD   = Automatically saves the terms as soon as a new one is added.
Save after Game       = Saves the terms and the score after each game played.
Message-Auto-Delete-Time = After how many seconds messages should be deleted automatically. (For example, if an argument was forgotten in a command).

Default-Points-To-Win = Points to win
Round-Lenght          = How long a team gets time to explain until it is the turn of the other team. (Seconds)
Switching-Lenght      = Time waited between team changes (Seconds)
Min-Players           = Minimum number of players for the start
```

## Wishes, Issues, Help needed?
Make a pull request. :)


## License
All code is under the [MIT](https://choosealicense.com/licenses/mit/) license.

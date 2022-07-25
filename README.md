# General Information

I'm not professional in programming and do this more like a hobby to have a great discord bot for my server.

At the moment i am using the version 3.10.5 of python and the discord.py beta 2.0

Feel free to use the code of the bot to create your own one.

Also the Discord Server has 2 roles that i will name "specific roles" in the file.
In the script they are the "Red Card" & "Yellow Card" roles.
More information see below at "Card System"

# Informations to the functions of the bot

What i mean with the functions are the things the bot is able to do.
Here is a list of everything:

-------------------------------------------------------------------
                                                                  V 1.0
-------------------------------------------------------------------
- displays the count of members on the server
- logging when someone leaves or joins the server
- displays the count of members with a specific role
- recognizes when someone gets a role of 2 specific ones, logs that & writes that in a json file
- deletes the role of the 2 when the timestamp is over 1 week old
- can create channels by command
  -> the creator will geht moved in the channel he created
  -> at the text version of the creation you can mention some user that also should be moved to the new channel
- can craete channels by reactions
- can search member that are playing a specific game by command
- can send infos of a user per message by command
- can give/remove roles by reaction
- can clear the messages in a channel
- displays how many players are currently playing a specific game

# Card System

The "Card System" is a system to "punish" members of the discord.
You can create a for example Red and Yellow Card role and give them restrictions like they cant send messages with a red card.

When someone receives either one of the roles they receive also a direct message of the bot as information that they got the role.
Also when someone loses a role of the 2 they will get a direct message, that they have lost the role.

When you give a user the Red Card Role and he has the Yellow Card already, the yellow will be removed. (they wont get a information about the removal here)

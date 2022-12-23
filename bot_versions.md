-------------------------------------------------------------------
                                                                 V 1.0
-------------------------------------------------------------------

published the bot on GitHub as it is at the moment

# Information about the functions of the bot

What i mean with the functions are the things the bot is able to do.
Here is a list of everything:

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


# commands

.create got commented out, because i replaced it by the creation with reactions
.search & .info also got commented out, because they never have been used

# general changes

i started to implement a new feature that should "track" if a member is active
  -> it will give a active member the role active and when he doesnt do anyhting for a specific time the role will be removed


-------------------------------------------------------------------
                                                                 V 2.0
-------------------------------------------------------------------

# New features

- implemented the "active" role
	-> you get it when you do a activity like writing a message or joining/leaving a channel
	-> it will be removed after 14 days
	-> all saved in a json file


# Bug fixes

- Stats for Rainbow didnt work quite well, because it had some issues i would say with the variable "guild", i now declared it directly in front of the call and not as a global variable


-------------------------------------------------------------------
                                                                 V 2.1
-------------------------------------------------------------------

# New

- Simpliefied the Creation of a Channel

-------------------------------------------------------------------
                                                                 V 2.2
-------------------------------------------------------------------

# Bug fixes

- Fixed the not working Activity Check on who is playing r6

-------------------------------------------------------------------
                                                                 V 2.3
-------------------------------------------------------------------

# New feature

- Now only the Member with the "Active User" Role are getting tracked for the active rainbow playing stat

-------------------------------------------------------------------
                                                                 V 2.4
-------------------------------------------------------------------

# Bug fixes

- Fixed that the Active Member roles won't be removed, because the first one in the list was someone who wasn't still on the server

# New

- added a new function, where i will specify all the parameters for better overview and management, more coming soon...
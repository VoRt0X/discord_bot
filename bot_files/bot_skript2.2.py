import discord
from discord.ext import commands
from discord.utils import get
import datetime
from datetime import timedelta
from datetime import datetime
import json
import asyncio
import logging

intents = discord.Intents.default()
intents.members = True
intents.messages = True
intents.presences = True
manage_guild = True
manage_roles = True
add_reaction = True
read_message_history = True
bot = commands.Bot(command_prefix='>', intents=intents)

#Setting the global Variables
c_channel_msg_id = 996482769578360942
guild = bot.get_guild(771495836701425725)


Token = 'OTQ3OTYzMzMyMDcyMTkwMDEy.GhVlPo.sz8izjMy3c_7b-yLSFpNQdONXCOa-rlCIF7JHQ'
bot_version_info = "Running on Version 2.2"

logging.basicConfig(filename='Logging.log', encoding='utf-8', level=logging.WARNING)

def check_active_file(member_id):
    with open("/home/pi/discordbot/active_member.json", "r") as f:
        data = json.load(f)
        active_member = data['timers']
        for content in active_member:
            if content == member_id:
                return True

def dump_active_member(member_id, name, nick_name):
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
    title = f"{member_id}"
    json_object = {"last_activity": f"{date_time}", "name": f"{name}",
                   "nick": f"{nick_name}", "member_id": f"{member_id}"}

    # Writing the Activity
    dump(title, json_object, "/home/pi/discordbot/active_member.json")

def dump(name, content, filename):
    with open(filename, "r") as f:
        data = json.load(f)

    data["timers"][name] = content

    with open(filename, "w") as f:
        json.dump(data, f, indent=2)


# Moving & Creating/Writing Channel
@bot.event
async def on_message(message):
    # From wich channel is the message from?
    # preparing for like everything
    message_split = message.content.split(' ')



    # clear command?
    if message_split[0] == ".clear":
        member = guild.get_member(message.author.id)
        channel = guild.get_channel(message.channel.id)

        results = []
        for role in member.roles:
            role_str = str(role)
            if "ADMIN" in role_str:
                results.append("yes")

            else:
                results.append("no")

        if "yes" in results:
            await channel.send(content="As you wish")
            await asyncio.sleep(1)
            await channel.send(content="Starting to clear.... Pls do not interrupt")
            messages_of_channel = await channel.history(limit=None).flatten()

            lenght = len(messages_of_channel)
            i = 0
            while i < lenght:
                msg_to_del = await channel.fetch_message(id=messages_of_channel[i].id)
                await msg_to_del.delete()
                i = i + 1

            await channel.send(content="Done")

        else:
            await channel.send(content="You don't have the permissions for that!")
            await message.delete()

    """# in Channel Commands?
    if message.channel.id == 977276355093872640:

        # Command?

        # Channel creating and getting moved in
        if message_split[0] == ".create":
            message_split = message.content.split()
            channel_max = message_split[1]

            category_id = guild.get_channel(940356081891287110)
            v_channel = await guild.create_voice_channel(f"Gaming Channel", category=category_id,
                                                         user_limit=channel_max)

            # Informations saved as a Variable
            date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
            title = f"{v_channel.id}"
            json_object = {"date": f"{date_time}", "channel_name": f"{v_channel}", "channel_id": f"{v_channel.id}"}

            # Writing the Channel creation
            dump(title, json_object, "/home/pi/discordbot/CCreated.json")

            # Moving the Creator in the Channel
            member = await guild.fetch_member(message.author.id)
            channel = guild.get_channel(v_channel.id)
            await member.move_to(channel)

            # Checking if someone got mentioned
            if message.raw_mentions:

                # moving them
                for mention in message.raw_mentions:
                    member = await guild.fetch_member(mention)
                    channel = guild.get_channel(v_channel.id)
                    await member.move_to(channel)

        elif message_split[0] == ".help":
            await message.channel.send(
                'Here are the commands you can use:\n_Please remember, that most importantly YOU have to be in a Channel, for the .create command and also the mentionend.'
                '\n\n.create X (optional you can @people to move them with u)  >>>>> X stands for an Number u can choose, something like 4 for example. '
                "It then will create a channel with a limit of 4 and you and the mentioned (if u did) are getting moved in.",
                reference=message)
            await message.delete()

        elif message_split[0] == ".info":

            # Looking if he wants to see his information or other
            if not message.raw_mentions:
                # Setting his information and sending it
                member = await guild.fetch_member(message.author.id)

                # Setting up a nice Join Date and Time on the Server
                joined_at_str = str(member.joined_at)
                joined_at = joined_at_str.split()
                joined_at_str = str(joined_at[0])
                date_swap = joined_at_str.split("-")
                joined_date = f"{date_swap[2]}.{date_swap[1]}.{date_swap[0]}"

                date_now = datetime.now()
                time_on_server_sec = timedelta.total_seconds(date_now - member.joined_at)

                # Sekunden / Tage
                time_on_server_days = time_on_server_sec / 86400
                time_on_server_short = round(time_on_server_days, 2)

                # Sending the info
                await message.channel.send(content=f"```\nInformation of Member: {member.nick}\n\n"
                                                   "General Information:\n"
                                                   f"Your Name: {member.name}\n"
                                                   f"Your ID: {member.id}\n"
                                                   f"Your Nick: {member.nick}\n"
                                                   "\n"
                                                   "Server Information:\n"
                                                   f"You joined at: {joined_date}\n"
                                                   f"Time you are on this Server: {time_on_server_short} Day(s)\n"
                                                   f"Your Top Role: {member.top_role}\n"
                                                   "```")
            else:
                # Setting the information of the specific user
                mention = message.raw_mentions[0]
                member = await guild.fetch_member(mention)

                # Setting up a nice Join Date and Time on the Server
                joined_at_str = str(member.joined_at)
                joined_at = joined_at_str.split()
                joined_at_str = str(joined_at[0])
                date_swap = joined_at_str.split("-")
                joined_date = f"{date_swap[2]}.{date_swap[1]}.{date_swap[0]}"

                date_now = datetime.now()
                time_on_server_sec = timedelta.total_seconds(date_now - member.joined_at)

                # Sekunden / Tage
                time_on_server_days = time_on_server_sec / 86400
                time_on_server_short = round(time_on_server_days, 2)

                # Sending the Info
                await message.channel.send(content=f"```\nInformation of Member: {member.nick}\n\n"
                                                   "General Information:\n"
                                                   f"Name: {member.name}\n"
                                                   f"ID: {member.id}\n"
                                                   f"Nick: {member.nick}\n"
                                                   "\n"
                                                   "Server Information:\n"
                                                   f"Joined at: {joined_date}\n"
                                                   f"Time on this Server: {time_on_server_short} Day(s)\n"
                                                   f"Top Role: {member.top_role}\n"
                                                   "```")

        # search command?
        # message syntax should be as following !search how many players (optional) which game
        # the game will be defined by the program if not given
        elif message_split[0] == ".search":
            pl_num = int(message_split[1])
            game_role = message.role_mentions if message.role_mentions else "None"
            game = "None"
            game_default = "None"

            # when he has no game mentioned
            if game_role == "None":
                author_id = int(message.author.id)
                dc_author_id = guild.fetch_member(author_id)
                author_activity = dc_author_id.activity
                author_activity_str = str(author_activity)
                author_activity_lw = author_activity_str.lower()
                game = author_activity
                game_default = author_activity_str

            else:
                dc_game_role_id = game_role[0].id

                game_id = str(dc_game_role_id)

                # Welches Game?
                if game_id == "843921623555768391":
                    game = "rainbow six siege"
                    game_default = "Rainbow Six Siege"
                if game_id == "940342181309337682":
                    game = "fortnite"
                    game_default = "Fortnite"
                if game_id == "940342260145483796":
                    game = "valorant"
                    game_default = "Valorant"
                if game_id == "940342335760379965":
                    game = "league of legends"
                    game_default = "League of Legends"
                if game_id == "940341888010055700":
                    game = "escape from tarkov"
                    game_default = "Escape from Tarkov"

            gamers = []
            if game != "None":
                # Loop through all members to find how many play the game rn
                for member in guild.members:
                    for act in member.activities:
                        if act.type is discord.ActivityType.playing and act.name.lower() == game:
                            gamers.append(f"{member.id}")

            # sending the people the notification for the search
            for member_id in gamers:
                member_id_int = int(member_id)
                user = await bot.fetch_user(member_id_int)
                await user.send(
                    f"{user.name} sucht {pl_num} Mitspieler für {game_default} auf dem Server Streammunity!!\nKomm gerne vorbei und spiel mit!")
            channel = await bot.fetch_channel(message.channel.id)
            await channel.send(content="Done")
            await message.delete()

        else:
            await message.delete()"""

    if message.channel.id == 996481469365092353: #new commands
        if message.author.id == 947963332072190012: #bot id
            await message.add_reaction("1️⃣")
            await message.add_reaction("2️⃣")
            await message.add_reaction("3️⃣")
            await message.add_reaction("4️⃣")
            await message.add_reaction("5️⃣")
            await message.add_reaction("6️⃣")
            await message.add_reaction("7️⃣")
            await message.add_reaction("8️⃣")
            await message.add_reaction("9️⃣")
            await message.add_reaction("🔟")

    # active file
    if message.author.id != 947963332072190012 & message.author.id != 846150781890854952:
        dump_active_member(message.author.id, message.author.name, message.author.nick)
        if not check_active_file(message.author.id):
            guild = bot.get_guild(771495836701425725)
            member = await guild.fetch_member(message.author.id)
            role = guild.get_role(1019253945941635302)
            await member.add_roles(role)




# Checking the channels
@bot.event
async def on_voice_state_update(member, before, after):

    # for activity
    if before.channel or after.channel:
        dump_active_member(member.id, member.name, member.nick)
        if not check_active_file(member.id):
            guild = bot.get_guild(771495836701425725)
            member = await guild.fetch_member(member.id)
            role = guild.get_role(1019253945941635302)
            await member.add_roles(role)

    # Checking the channels
    filename = "/home/pi/discordbot/CCreated.json"
    with open(filename, 'r') as f:
        channels_created = json.load(f)

    for content in channels_created['timers']:
        # find raiding
        channel_id = int(content)

        # finds the members (when noone is in)
        voice_channel = bot.get_channel(channel_id)
        voice_ch_str = str(voice_channel.members)
        # Testing if someone is in there
        if voice_ch_str == "[]":
            channel_get = bot.get_channel(channel_id)
            await channel_get.delete()

            with open(filename, "r") as f:
                data = json.load(f)

                data["timers"].pop(f"{data['timers'][content]['channel_id']}")

            with open(filename, "w") as f:
                json.dump(data, f, indent=2)



# Updating the Member count at join
@bot.event
async def on_member_join(member):
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
    logging.log(level=60, msg=f"{member} joined the Discord at {date_time}")

    # Getting User Count
    guild = bot.get_guild(771495836701425725)
    user_count = len(guild.members)  # includes bots
    true_user_count = len([m for m in Guild.members if not m.bot])  # doesn't include bots

    # Setting the new Stats
    user_stats = await bot.fetch_channel(968558391490400307)
    await user_stats.edit(name=f"\U0001F4CA USERS: {true_user_count}")
    logging.log(level=60, msg=f"User Count increased to {true_user_count} at {date_time}")


# Updating the Member count at leave
@bot.event
async def on_member_remove(member):
    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
    logging.log(level=60, msg=f"{member} left the Discord at {date_time}")

    # Getting User Count
    guild = bot.get_guild(771495836701425725)
    user_count = len(guild.members)  # includes bots
    true_user_count = len([m for m in guild.members if not m.bot])  # doesn't include bots

    # Setting the new Stats
    user_stats = await bot.fetch_channel(968558391490400307)
    await user_stats.edit(name=f"\U0001F4CA USERS: {true_user_count}")
    logging.log(level=60, msg=f"User Count changed to {true_user_count} at {date_time}")


# Role change checks
@bot.event
async def on_member_update(before: discord.Member, after: discord.Member):
    # Did he got a Role?
    if len(before.roles) < len(after.roles):
        # The Variable where the Change is saved in
        change = list(set(after.roles) - set(before.roles))

        # Which role?

        # Yellow Card?
        if {change[0].id} == {947898505744232488}:
            date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")

            # Informations saved as a Variable
            title1 = f"{before}"
            json_object = {"date": f"{date_time}", "role_name": f"{change[0].name}", "role_id": f"{change[0].id}",
                           "member_name": f"{before}", "member_id": f"{before.id}"}


            # Writing & Logging the Role update
            dump(title1, json_object, "/home/pi/discordbot/Yellow Card.json")
            logging.log(level=60, msg=f"{before} got a Yellow Card at {date_time}")

            # Sending the User a Info
            member_id_int = int(before.id)
            user = await bot.fetch_user(member_id_int)
            await user.send(f"Hello there,\nunfortunately you got the {change[0].name}.\n"
                            f"That could have one of the following reasons:\n"
                            f"Leaving while in game, insultnig other People on the Server\n"
                            f"For more information reach out to one of our Mods/Admins or to the Server Owner.")

        # Red Card?
        elif {change[0].id} == {946391448343945336}:
            date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")

            # Informations saved as a Variable
            filename2 = "Red Card.json"
            title2 = f"{before}"
            json_object2 = {"date": f"{date_time}", "name": f"{change[0].name}", "role_id": f"{change[0].id}",
                            "member_name": f"{before}", "member_id": f"{before.id}"}


            # Writing & Logging the Role update
            dump(title2, json_object2, "/home/pi/discordbot/Red Card.json")
            logging.log(level=60, msg=f"{before} got a Red Card at {date_time}")

            # Sending the User a Info
            member_id_int = int(before.id)
            user = await bot.fetch_user(member_id_int)
            await user.send(f"Hello there,\nunfortunately you got the {change[0].name}.\n"
                            f"That could have one of the following reasons:\n"
                            f"Leaving while in game, insulting other People on the Server, harassment \n"
                            f"For more information reach out to one of our Mods/Admin or to the Server Owner.")

        # Streamer?
        elif {change[0].id} == {841596562689097729}:
            date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
            logging.log(level=60, msg=f"Streamer got added at: {date_time}")

            # Getting Streamer Count
            role_id = 841596562689097729
            guild = bot.get_guild(771495836701425725)
            role = get(guild.roles, id=role_id)
            streamer_count = len(role.members)
            logging.log(level=60, msg=f"Streamer count now: {streamer_count}")

            # Setting the new Stats
            streamer_stats = await bot.fetch_channel(968570363103568012)
            await streamer_stats.edit(name=f"\U0001F4CA STREAMER: {streamer_count}")

    # Did he lose a Role?
    if len(before.roles) > len(after.roles):
        change = list(set(before.roles) - set(after.roles))

        # Streamer?
        if {change[0].id} == {841596562689097729}:
            date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
            logging.log(level=60, msg=f"A Streamer got removed at: {date_time}")

            # Getting Streamer Count
            role_id = 841596562689097729
            guild = bot.get_guild(771495836701425725)
            role = get(guild.roles, id=role_id)
            streamer_count = len(role.members)
            logging.log(level=60, msg=f"Streamer count now: {streamer_count}")

            # Setting the new Stats
            streamer_stats = await bot.fetch_channel(968570363103568012)
            await streamer_stats.edit(name=f"\U0001F4CA STREAMER: {streamer_count}")

        # Yellow Card?
        if {change[0].id} == {947898505744232488}:
            with open('Yellow Card.json', 'r') as f:
                data1 = json.load(f)

            # Checking every entry in the file
            for content in data1['timers']:

                # Getting both IDs and turning them into INT
                id_changed_user = int(before.id)
                member_id_json = int(data1['timers'][content]['member_id'])

                # Checking if the User has an entry in the File
                if member_id_json == id_changed_user:

                    # Deleting the entry
                    with open("Yellow Card.json", "r") as f:
                        data = json.load(f)

                        data["timers"].pop(f"{data1['timers'][content]['member_name']}")

                    with open("Yellow Card.json", "w") as f:
                        json.dump(data, f, indent=2)

                    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
                    logging.log(level=60,
                                msg=data1["timers"][content]["member_name"] + " got removed the Yellow Card. "
                                    + date_time)

                    guild = bot.get_guild(771495836701425725)
                    member = guild.get_member(after.id)
                    results = []
                    for role in member.roles:
                        role_str = str(role)
                        if "Red Card" in role_str:
                            results.append("yes")

                        else:
                            results.append("no")

                    if "yes" in results:
                        break

                    else:
                        await member.send("Hello there,\nCongrats!! Your Yellow Card got removed!")

        # Red Card?
        if {change[0].id} == {946391448343945336}:
            with open('/home/pi/discordbot/Red Card.json', 'r') as f:
                data1 = json.load(f)

            # Checking every entry in the file
            for content in data1['timers']:

                # Getting both IDs and turning them into INT
                id_changed_user = int(before.id)
                member_id_json = int(data1['timers'][content]['member_id'])

                # Checking if the User has an entry in the File
                if member_id_json == id_changed_user:
                    # Deleting the entry
                    with open("/home/pi/discordbot/Red Card.json", "r") as f:
                        data = json.load(f)

                        data["timers"].pop(f"{data1['timers'][content]['member_name']}")

                    with open("/home/pi/discordbot/Red Card.json", "w") as f:
                        json.dump(data, f, indent=2)

                    date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
                    logging.log(level=60,
                                msg=data1["timers"][content]["member_name"] + " got removed the Red Card. " + date_time)

                    # Sending the User a Info
                    user = await bot.fetch_user(id_changed_user)
                    await user.send("Hello there,\nCongrats!! Your Red Card got removed!")

# Activity Tracking
@bot.event
async def on_presence_update(before, after):
    if before.activity != after.activity:

        if before.activity:
            bfactivity_str = str(before.activity.name)
            bfactivity_lw = bfactivity_str.lower()

            if bfactivity_lw == "rainbow six siege":
                # Stats for Rainbow
                gamers = []
                game = "rainbow six siege"
                guild = bot.get_guild(771495836701425725)
                for member in guild.members:
                    for act in member.activities:
                        if act.type is discord.ActivityType.playing and act.name.lower() == game:
                            gamers.append(f"{member.id}")

                stats_channel = await bot.fetch_channel(971830717292101722)
                new_count = len(gamers)

                # Setting new stats
                await stats_channel.edit(name=f"\U0001F4CA Currently Playing: {new_count}")

        if after.activity:
            afactivity_str = str(after.activity.name)
            afactivity_lw = afactivity_str.lower()
            if afactivity_lw == "rainbow six siege":
                # Stats for Rainbow

                gamers = []
                game = "rainbow six siege"
                guild = bot.get_guild(771495836701425725)
                for member in guild.members:
                    for act in member.activities:
                        if act.type is discord.ActivityType.playing and act.name.lower() == game:
                            gamers.append(f"{member.id}")

                stats_channel = await bot.fetch_channel(971830717292101722)
                new_count = len(gamers)

                # Setting new stats
                await stats_channel.edit(name=f"\U0001F4CA Currently Playing: {new_count}")


# State setting, Card Check, Active Check
@bot.event
async def on_ready():
    # Set State
    logging.log(level=60, msg='Logged in as {0.user}'.format(bot))
    print('Logged in as {0.user}'.format(bot))
    await bot.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name="Alex Befehlen"))
    logging.log(level=60, msg=f'{bot_version_info}')
    print(f'{bot_version_info}')


    # Checking for Cards and Active Members
    while True:

        # Yellow Card Check
        with open('/home/pi/discordbot/Yellow Card.json', 'r') as f:
            data1 = json.load(f)

        for content in data1['timers']:
            time_str = json.dumps(data1["timers"][content]["date"])
            time_stre = time_str.replace('"', "")

            date_import = datetime.strptime(time_stre, "%m/%d/%Y, %H:%M")
            date_nowstr = datetime.now().strftime("%m/%d/%Y, %H:%M")
            date_now = datetime.strptime(date_nowstr, "%m/%d/%Y, %H:%M")

            totalseconds = timedelta.total_seconds(date_now - date_import)

            if totalseconds >= 1209600.0:

                # Converting to Int
                member_id = int(f"{data1['timers'][content]['member_id']}")

                # Defining the Variables
                guild = bot.get_guild(771495836701425725)
                role = guild.get_role(947898505744232488)
                member = await guild.fetch_member(member_id)

                # Removing the role
                await member.remove_roles(role)

                with open("/home/pi/discordbot/Yellow Card.json", "r") as f:
                    data = json.load(f)

                    data["timers"].pop(f"{data1['timers'][content]['member_name']}")

                with open("/home/pi/discordbot/Yellow Card.json", "w") as f:
                    json.dump(data, f, indent=2)

                date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
                logging.log(level=60,
                            msg=data1["timers"][content]["member_name"] + " got removed Yellow Card. " + date_time)

            else:
                date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
                logging.log(level=60, msg=data1["timers"][content][
                                              "member_name"] + "  Yellow Card not over 2 Weeks old. " + date_time)

        await asyncio.sleep(5)

        # Red Card Check
        with open('/home/pi/discordbot/Red Card.json', 'r') as f:
            data1 = json.load(f)

        for content in data1['timers']:
            time_str = json.dumps(data1["timers"][content]["date"])
            time_stre = time_str.replace('"', "")

            date_import = datetime.strptime(time_stre, "%m/%d/%Y, %H:%M")
            date_nowstr = datetime.now().strftime("%m/%d/%Y, %H:%M")
            date_now = datetime.strptime(date_nowstr, "%m/%d/%Y, %H:%M")

            totalseconds = timedelta.total_seconds(date_now - date_import)

            if totalseconds >= 604800.0:
                # logging.log(level=60,msg="Over 7 Days, beginning of the removal")
                # Converting to Int
                member_id = int(f"{data1['timers'][content]['member_id']}")

                # Defining the Variables
                guild = bot.get_guild(771495836701425725)
                role = guild.get_role(947898505744232488)
                member = await guild.fetch_member(member_id)

                # Removing the role
                await member.remove_roles(role)
                # logging.log(level=60, msg=f"Role has been removed from {data1['timers'][content]['member_name']}")
                with open("/home/pi/discordbot/Red Card.json", "r") as f:
                    data = json.load(f)

                    data["timers"].pop(f"{data1['timers'][content]['member_name']}")

                with open("/home/pi/discordbot/Red Card.json", "w") as f:
                    json.dump(data, f, indent=2)

                date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
                logging.log(level=60,
                            msg=data1["timers"][content]["member_name"] + " got removed Yellow Card. " + date_time)

            else:
                date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
                logging.log(level=60, msg=data1["timers"][content][
                                              "member_name"] + "  Red Card not over 1 Week old. " + date_time)

        await asyncio.sleep(3)

        # Active check
        path = "/home/pi/discordbot/active_member.json"
        with open(path, 'r') as f:
            active_member_jsn = json.load(f)

        for content in active_member_jsn['timers']:
            time_str = json.dumps(active_member_jsn["timers"][content]["last_activity"])
            time_stre = time_str.replace('"', "")

            date_import = datetime.strptime(time_stre, "%m/%d/%Y, %H:%M")
            date_nowstr = datetime.now().strftime("%m/%d/%Y, %H:%M")
            date_now = datetime.strptime(date_nowstr, "%m/%d/%Y, %H:%M")

            totalseconds = timedelta.total_seconds(date_now - date_import)
            if totalseconds >= 1209600.0:
                # logging.log(level=60,msg="Over 7 Days, beginning of the removal")
                # Converting to Int
                member_id = int(f"{active_member_jsn['timers'][content]['member_id']}")

                # Defining the Variables
                guild = bot.get_guild(771495836701425725)
                role = guild.get_role(1019253945941635302)
                member = await guild.fetch_member(member_id)

                # Removing the role
                await member.remove_roles(role)

                with open(path, "r") as f:
                    data = json.load(f)

                    data["timers"].pop(f"{active_member_jsn['timers'][content]['member_id']}")

                with open(path, "w") as f:
                    json.dump(data, f, indent=2)

        await asyncio.sleep(21600)


# Reaction Roles add and Creating a Channel
@bot.event
async def on_raw_reaction_add(payload):
    # Right channel?
    if payload.channel_id == 927015318424002680:
        # Wich message?
        if payload.message_id == 940347084316491877:

            # Wich Emoji?
            if payload.emoji.name == "Rainbow_six_by_patriotLV":  # Reaction for Role "Rainbow"
                guild = bot.get_guild(771495836701425725)
                # Defining Variables
                role = guild.get_role(843921623555768391)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "csgo":  # Reaction for Role "CSGO"

                # Defining Variables
                role = guild.get_role(940341838072647730)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "Apex_Legends":  # Reaction for Role "Apex"

                # Defining Variables
                role = guild.get_role(940341655431688203)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "Call_of_Duty_by_patriotLV":  # Reaction for Role "COD"

                # Defining Variables
                role = guild.get_role(940342074694332420)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "FortniteLogo":  # Reaction for Role "Fortnite"

                # Defining Variables
                role = guild.get_role(940342181309337682)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "League_of_legends":  # Reaction for Role "LOL"

                # Defining Variables
                role = guild.get_role(940342335760379965)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "Minecraft":  # Reaction for Role "Minecraft"

                # Defining Variables
                role = guild.get_role(940342150091132959)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "Valorant":  # Reaction for Role "Valorant"

                # Defining Variables
                role = guild.get_role(940342260145483796)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "ark":  # Reaction for Role "ARK"

                # Defining Variables
                role = guild.get_role(940350505744470027)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "battlefield2024":  # Reaction for Role "Battlefield"

                # Defining Variables
                role = guild.get_role(940349739554185357)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "pubg":  # Reaction for Role "PUBG"

                # Defining Variables
                role = guild.get_role(940341758330540112)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "rust_by_patriotLV":  # Reaction for Role "Rust"

                # Defining Variables
                role = guild.get_role(940349699951591434)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "tarkovkilla":  # Reaction for Role "EFT"

                # Defining Variables
                role = guild.get_role(940341888010055700)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "emoji_18":  # Reaction for Role "CIV6"

                # Defining Variables
                role = guild.get_role(946391534931148850)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "gmod":  # Reaction for Role "TTT"

                # Defining Variables
                role = guild.get_role(947875882637348895)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "✅":  # Reaction for Role "Gaming"

                # Defining Variables
                role = guild.get_role(940342464248680488)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "18":  # Reaction for Role "+18"

                # Defining Variables
                role = guild.get_role(927014360507908166)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

            if payload.emoji.name == "Twitch":  # Reaction for Role "Follower"

                # Defining Variables
                role = guild.get_role(927014768739504178)
                member = await guild.fetch_member(payload.member.id)
                await member.add_roles(role)

    elif payload.channel_id == 996481469365092353: #New commands
        if payload.message_id == 1023625020393652325: #Main Message

            if not payload.user_id == 947963332072190012:

                #Setting the variable for the channel max users
                emoji_str = payload.emoji.name
                channel_max = 0
                if emoji_str == "1️⃣":
                    channel_max = 1

                elif emoji_str == "2️⃣":
                    channel_max = 2

                elif emoji_str == "3️⃣":
                    channel_max = 3

                elif emoji_str == "4️⃣":
                    channel_max = 4

                elif emoji_str == "5️⃣":
                    channel_max = 5

                elif emoji_str == "6️⃣":
                    channel_max = 6

                elif emoji_str == "7️⃣":
                    channel_max = 7

                elif emoji_str == "8️⃣":
                    channel_max = 8

                elif emoji_str == "9️⃣":
                    channel_max = 9

                elif emoji_str == "🔟":
                    channel_max = 10


                #Creating the channel
                guild = bot.get_guild(771495836701425725)
                category_id = guild.get_channel(940356081891287110)
                v_channel = await guild.create_voice_channel(f"Gaming Channel", category=category_id,
                                                                 user_limit=channel_max)

                # Informations saved as a Variable
                date_time = datetime.now().strftime("%m/%d/%Y, %H:%M")
                filename1 = "/home/pi/discordbot/CCreated.json"
                title = f"{v_channel.id}"
                json_object = {"date": f"{date_time}", "channel_name": f"{v_channel}",
                               "channel_id": f"{v_channel.id}"}


                # Writing the Channel creation
                dump(title, json_object, "/home/pi/discordbot/CCreated.json")

                # Moving the Creator in the Channel
                guild = bot.get_guild(771495836701425725)
                member = await guild.fetch_member(payload.user_id)
                await member.move_to(v_channel)

                #Removing the Reaction
                channel = bot.get_channel(payload.channel_id)
                message = await channel.fetch_message(payload.message_id)
                user = await bot.fetch_user(payload.user_id)
                await message.remove_reaction(emoji=payload.emoji, member=user)


# Reaction Roles remove
@bot.event
async def on_raw_reaction_remove(payload):
    # Right channel?
    if payload.channel_id == 927015318424002680:
        # Wich message?
        if payload.message_id == 940347084316491877:

            # Wich Emoji?
            guild = bot.get_guild(771495836701425725)
            if payload.emoji.name == "Rainbow_six_by_patriotLV":  # Reaction for Role "Rainbow"

                # Defining Variables
                role = guild.get_role(843921623555768391)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "csgo":  # Reaction for Role "CSGO"

                # Defining Variables
                role = guild.get_role(940341838072647730)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "Apex_Legends":  # Reaction for Role "Apex"

                # Defining Variables
                role = guild.get_role(940341655431688203)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "Call_of_Duty_by_patriotLV":  # Reaction for Role "COD"

                # Defining Variables
                role = guild.get_role(940342074694332420)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "FortniteLogo":  # Reaction for Role "Fortnite"

                # Defining Variables
                role = guild.get_role(940342181309337682)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "League_of_legends":  # Reaction for Role "LOL"

                # Defining Variables
                role = guild.get_role(940342335760379965)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "Minecraft":  # Reaction for Role "Minecraft"

                # Defining Variables
                role = guild.get_role(940342150091132959)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "Valorant":  # Reaction for Role "Valorant"

                # Defining Variables
                role = guild.get_role(940342260145483796)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "ark":  # Reaction for Role "ARK"

                # Defining Variables
                role = guild.get_role(940350505744470027)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "battlefield2024":  # Reaction for Role "Battlefield"

                # Defining Variables
                role = guild.get_role(940349739554185357)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "pubg":  # Reaction for Role "PUBG"

                # Defining Variables
                role = guild.get_role(940341758330540112)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "rust_by_patriotLV":  # Reaction for Role "Rust"

                # Defining Variables
                role = guild.get_role(940349699951591434)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "tarkovkilla":  # Reaction for Role "EFT"

                # Defining Variables
                role = guild.get_role(940341888010055700)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "emoji_18":  # Reaction for Role "CIV6"

                # Defining Variables
                role = guild.get_role(946391534931148850)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "gmod":  # Reaction for Role "TTT"

                # Defining Variables
                role = guild.get_role(947875882637348895)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "✅":  # Reaction for Role "Gaming"

                # Defining Variables
                role = guild.get_role(940342464248680488)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "18":  # Reaction for Role "+18"

                # Defining Variables
                role = guild.get_role(927014360507908166)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)

            if payload.emoji.name == "Twitch":  # Reaction for Role "Follower"

                # Defining Variables
                role = guild.get_role(927014768739504178)
                member = await guild.fetch_member(payload.user_id)
                await member.remove_roles(role)


bot.run(Token)

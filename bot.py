import random
import discord
import dota2api
import youtube_dl
import subprocess
from secret import id_64
from random import randint as rnd
from discord.ext.commands import Bot
from validators import url as is_a_URL

my_bot = Bot(command_prefix = '!')

voice = ''
songs = []
titles = []
index = 0
current_player_index= 0
silence = False
insert_title = False
playing = False


@my_bot.event
async def on_ready():
    print ('Logged in as')
    print (my_bot.user.name)
    print (my_bot.user.id)


@my_bot.command()
async def test(*args):
    await my_bot.say('This is a test! Think im alive')


@my_bot.command(pass_context = True)
async def echo(ctx, *, echo: str):
    print (ctx.message.channel.type)
    await my_bot.delete_message(ctx.message)
    await my_bot.say(":grinning: " + echo)


@my_bot.command()
async def close(*args):
    await my_bot.say('Bye!')
    await my_bot.close()


@my_bot.command(pass_context = True)
async def clean(ctx, *args):
    channel = ctx.message.channel
    def is_me(m):
        return m.author == my_bot.user

    await my_bot.purge_from(channel, limit = 100, check = is_me)


@my_bot.command(pass_context = True)
async def clear(ctx, *, number: int):
    user = ctx.message.author
    channel = ctx.message.channel

    def is_user(m):
        return m.author == user
    await my_bot.purge_from(channel, limit = number, check=is_user)


@my_bot.command(pass_context = True)
async def tabula_rasa(ctx, *args):
    channel = ctx.message.channel
    await my_bot.purge_from(channel, limit = 100)


@my_bot.command(pass_context = True)
async def pin(ctx, position: int):
    lenght = len(my_bot.messages)
    message = my_bot.messages[lenght-(position + 1)]
    channel = ctx.message.channel
    await my_bot.pin_message(message)

    def is_me(m):
        return m.author == my_bot.user

    await my_bot.purge_from(channel, limit = 1, check = is_me)


@my_bot.command(pass_context = True)
async def kick(ctx, *, name: str):
    server = ctx.message.channel.server
    member = server.get_member_named(name)
    if member == None:
        await my_bot.say("Non ho trovato nessun utente con quel nome. Sai cosa? Le maiuscole, controlla le maiuscole.")
    else:
        try:
            await my_bot.kick(member)

        except:
            await my_bot.say("I don't have the permission to perform this action.")


@my_bot.command(pass_context = True)
async def rollercoster(ctx, name: str, times: int):
    server = ctx.message.channel.server
    member = server.get_member_named(name)

    for channels in server.channels:
        for members in channels.voice_members:
            if members.id == member.id:
                start_channel = channels


    for x in range(0, (times)):
        for channels in server.channels:
            if channels.type == discord.ChannelType.voice:

                await my_bot.move_member(member, channels)

    await my_bot.move_member(member, start_channel)



''' LIBRARY BOT SECTION '''




@my_bot.command(pass_context = True)
async def silence(ctx, *args):
    channel = ctx.message.channel
    await my_bot.send_message(channel,"Library-mode on.")
    global silence
    silence = True


@my_bot.command(pass_context = True)
async def no_silence(ctx, *args):
    global silence
    silence = False
    channel = ctx.message.channel
    await my_bot.send_message(channel, "Library-mode off.")


@my_bot.event
async def on_message(message):
    channel = message.channel
    if message.author.id != my_bot.user.id:
        if silence == True:
            await my_bot.send_message(channel, "Shh!")
            await my_bot.delete_message(message)
            await my_bot.process_commands(message)

    await my_bot.process_commands(message)



''' MUSIC BOT SECTION '''



def check_URL(string):
    global insert_title

    if is_a_URL(string):
        URL = string
        insert_title = False

    else:
        command = "ytsearch1:{}".format(string)
        URL = subprocess.check_output(['youtube-dl', '-g', '-f', 'best', command], shell = False).decode("utf-8")
        TITLE = subprocess.check_output(['youtube-dl', '--get-title', command], shell = False).decode("utf-8")
        titles.append(TITLE)
        insert_title = True

    return URL


def play_song():
    global index
    global playing
    global current_player_index

    try:
        songs[index].start()
        current_player_index = index
        index = index +1
        playing = True

    except:

        playing = False


def pausing():
    global current_player_index
    songs[current_player_index].pause()


def resuming():
    global current_player_index
    songs[current_player_index].resume()


@my_bot.command()
async def pause(*args):
    pausing()

@my_bot.command()
async def resume(*args):
    resuming()


@my_bot.command()
async def skip(*args):

    if len(songs)-1 > current_player_index:
        pausing()
        play_song()
        resuming()

    else:
        await my_bot.say("I can't skip. Playlist is empty")


@my_bot.command()
async def playlist(*args):

    if not titles:
        await my_bot.say("Playlist is empty")

    else:
        playlist = "```"

        for index in range(len(titles)):

            playlist += "{}:".format(index) + " {}".format(titles[index]) + ""

        playlist += "```" + "\n"
        await my_bot.say(playlist)



@my_bot.command()
async def skip_to(*, song_position: int):
    global index
    max_index = len(songs)-1

    if song_position <= max_index:
        index = song_position
        pausing()
        play_song()
        resuming()

    else:
        await my_bot.say("There is not a song in that position")


@my_bot.command()
async def clear_playlist(*args):
    global index
    global current_player_index

    for song in range(len(songs)):
        SONG = songs.pop(0)

        if song == current_player_index:
            songs.insert(0, SONG)

    for title in range(len(titles)):
        TITLE = titles.pop(0)

        if title == current_player_index:
            titles.insert(0, TITLE)

    index = 0
    current_player_index = 0
    await my_bot.say("Playlist is now empty")


@my_bot.command(pass_context = True)
async def play(ctx, *, title: str):
    global voice
    global songs
    global index
    global insert_title
    server = ctx.message.channel.server
    url = check_URL(title)

    for channel in server.channels:
        for member in channel.voice_members:
            if member.id == ctx.message.author.id:
                if isinstance(voice, str):
                    voice = await my_bot.join_voice_channel(channel)

                elif voice.channel != channel:
                    voice.move_to(channel)

    player = await voice.create_ytdl_player(url, after = play_song)
    songs.append(player)

    if not insert_title:
        titles.append(player.title)

    last_title = len(titles) -1

    if not playing:
        play_song()
        await my_bot.say('Now playing {}'.format(titles[last_title]))

    else:
        await my_bot.say('{} added to queue'.format(titles[last_title]))



""" DOTA BOT SECTION """



@my_bot.command(pass_context = True)
async def ID(ctx, value):
    ID_64 = id_64(value)
    if not ID_64:
        my_bot.say("Your imput can not be coverted in a 64-bit Steam ID.")

    await my_bot.say("Your Steam ID 64 bit is: {}".format(ID_64))


@my_bot.command(pass_context = True)
async def Save_ID(ctx, value):
    author = ctx.message.author.name
    ID_64 = id_64(value)

    if not ID_64:
        my_bot.say("Your imput can not be coverted in a 64-bit Steam ID.")

    FILE = open("/Users/andrea/Desktop/python/dota/ID_STORAGE.txt", "r+")

    if '{}'.format(ID_64) in FILE.read():
        await my_bot.say("ID already saved")

    FILE.write(ctx.message.author.name + '\n')
    FILE.write('{}'.format(ID_64) + '\n')

    FILE.close()
    await my_bot.say("Steam ID: {}".format(ID_64) + "Saved for the user: {}".format(author))






my_bot.run('MzY2Njg0MDcxMDM3ODk0NjU3.DL1B8g._iVIY5CN6wj7x2izKd50HVBapeg')

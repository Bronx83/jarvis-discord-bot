from discord.ext.commands import Bot
import secrets
from etc import *
from collections import Counter

vote = False
votes = dict()

jarvis = Bot(command_prefix="!")
one_time_generator = False

who_to_kick = ""
muted_author = ""

min_to_mute = 3
min_to_unmute = 3

cmd = dict()
cmd['votekick'] = '!votekick'
cmd['y'] = '!y'
cmd['n'] = '!n'
cmd['pyhelp'] = '!pyhelp'
cmd['ping'] = '!ping'
cmd['helpme'] = '!helpme'
cmd['voterules'] = '!vote_rules'
cmd['hello'] = '!hello'

@jarvis.event
async def on_read():
    print("Client logged in.")

def check_message(m):
    global muted_author
    return m.author == muted_author

@jarvis.event
async def on_message(message):
    global members
    global all_names
    global muted_author
    global cmd
    
    cont = message.content
    author = message.author.id
    print(message.author.id,message.author.name,message.content)
    answer =""

    if message.author.name == 'Jarvis':
        # !y
        if cont.startswith(cmd['y']):
            answer = vote_yn(author,1)   
        # !n
        if cont.startswith(cmd['n']):
            answer = vote_yn(author,0)   
        return;
        
    global one_time_generator
    if not one_time_generator:
        await jarvis.send_message(message.channel, "_[!] Jarvis Turned On._")
        one_time_generator = True
        members = list(jarvis.get_all_members())
        all_names = list( x.name for x in members )
        #emojis = jarvis.get_all_emojis()
        #print(list(emojis))

    
    """
        if message.author.name == "bronx83":
            await jarvis.add_reaction(message,100)
            print('added reaction')

        if message.author.name == "Alm0st":
            await jarvis.add_reaction(message,'ss')
            print('added reaction')

        if message.author.name == "bronx83":
            await jarvis.clear_reactions(message)
            print('reactions cleared.')
    """
    if str(message.author.id) == str(310473990906839051):
        if cont.startswith('!unmute'):
            muted_author = ""
            print(muted_author," unmuted.")
            return;
        
        elif cont.startswith('!mute'): 
            muted_author = message.content[len('!mute'):].strip()
            print(muted_author," is now muted.")
            return;
        
        elif cont.startswith('!doy'):
            return await jarvis.send_message(message.channel, "!y")
        
        elif cont.startswith('!don'):
            return await jarvis.send_message(message.channel, "!n")
        
        elif cont.startswith('!stop_vote'):
            global vote
            global votes
            global who_to_kick

            who_to_kick = ""
            vote = False
            votes = dict()
            print("vote stopped.")
            return;
 #   try:
    if muted_author == message.author:
        await jarvis.purge_from(message.channel,limit=2,check=check_message)
        message_to_user = "You ({}) can't write messages while muted.".format(muted_author)
        return await jarvis.send_message(muted_author, message_to_user, tts=True)
    
    # !votekick
    elif cont.startswith(cmd['votekick']):
        answer = votekick(author, message.content[len(cmd['votekick']):].strip())
    # !y
    elif cont.startswith(cmd['y']):
        answer = vote_yn(author,1)   
    # !n
    elif cont.startswith(cmd['n']):
        answer = vote_yn(author,0)   
    # !pyhelp
    elif cont.startswith(cmd['pyhelp']):
        answer = pyhelp(message.content[len(cmd['pyhelp']):].strip())
    # !ping
    elif cont.startswith(cmd['ping']):
        answer = ping()
    # !helpme
    elif cont.startswith(cmd['helpme']):
        top = "Usage: \n```"
        answer = list(str(cmd.values()))
        for i,char in enumerate(answer):
            if char == ',':
                answer[i] = '\n'
        answer = ''.join(answer).split('dict_values([')[1].split('])')[0]
        answer = top+" "+answer+'```\n'
    # !hello
    elif cont.startswith(cmd['hello']):
        answer = hello()
    # !helpme
    elif cont.startswith(cmd['voterules']):
        answer = vote_rules()
    
#    except NameError:
#            pass

    if answer:
        return await jarvis.send_message(message.channel, answer)

def votekick(author,args):
    global vote
    global who_to_kick
    global min_to_mute

    if args == 'Jarvis':
        return "You can't kick Jarvis..."
    if args not in all_names:
        return "User '{}' does not exist on this server.\n Users:\n{}".format(args,all_names)
    elif not vote:
        for x in members:
            if x.name == args: #or x.nick == args:
                who_to_kick = x
                break
        vote = True
        answer = "@here A vote to mute \"{}\" has started.\nYou need {} people to successfuly mute someone.\n!vote_rules to check the rules of the vote.\nTo enter the vote: !y = Yes, !n = No.\n".format(who_to_kick.name, min_to_mute)
        answer += vote_yn(author,1)
    else:
        answer = "Can't make another vote while there is aleady an active one. ([4])\n"
        answer += "Type !vote_rules for more information."
    return answer

def vote_yn(author,value):
    global vote
    global votes
    if vote:
        votes[author]=value
        print(votes)
        answer = print_answer(votes)
    else:
        votes = dict()
        answer = "There are no active votes right now."
    return answer

def print_answer(votes_dict):
    global who_to_kick
#    global members
    answer = "```Voting Table: to mute {}.\n".format(who_to_kick.name)
    for x in members:
        if x.id in votes_dict:
            answer +="{} | {}\n".format(x.name, bool(votes_dict[x.id]))
    answer +="```{}".format(checkFinish())
    return answer

def checkFinish():
    global vote
    global votes
    global who_to_kick
    global muted_author
    global min_to_mute
    global min_to_unmute

    answer = ""
    results = Counter(votes.values())
    if results[1] >= min_to_mute:
        muted_author = who_to_kick
        answer = "{} was muted!".format(who_to_kick.name)
        who_to_kick = ""
        vote = False
        votes = dict()
    elif results[0] >= min_to_unmute:
        answer = "The vote against \"{}\" got cancled.".format(who_to_kick.name)
        who_to_kick = ""
        muted_author = ""
        vote = False
        votes = dict()
    return answer

def vote_rules():
    rules = "*VOTEKICK RULES:*"
    rules += "```[1] To successfuly mute some one you need atleast 3 people to vote !y\n"
    rules += "[2] To end a vote you need 3 people to vote !n\n"
    rules += "[3] Adi is not gay.\n"
    rules += "[4] Can't start a vote when there is already an active one.\n```"
    return rules


jarvis.run(secrets.BOT_TOKEN)

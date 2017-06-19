from urllib.parse import urlencode
import random

def hello():
    return "Hello world!"

async def is_adi_gay(*args):
    answers = ["Adi is gay AFFF.", "Adi is super gay.", "```rust println!(\"Hacking in progress..\");```", "I predict that Adi is gay.", "Alm: 0st command not found.", "I think Adi is almost, gay.", "!votekick Alm0st.", "HA! GAYYYYYY!", "BURN ADI HE IS GAYYYY.", "OMG ADI YOU ARE GAY AF.", "Checking Google for this question.... Google found that Adi is gay, shock...", "Nope.", "Not today.", "49.387484968483% I'm sure he is..", "Obviously..", "NO NO NO NO.", "Hi, it's Adi, I hacked you. DIE MOTHERFUCKER.", "```python def Hack(person): \n\t return person.rootPassowrd()\n\n Hack(\"Halfon\")", "Nope, but I heard that Lionheart is gay AF.", "Not as much as you fucker.", "YOU MOTHERFUCKER.", "4REAL NOW?"]
    ans = answers[random.randrange(len(answers))]
    return await jarvis.say(ans)

def pyhelp(args):
    url = 'https://docs.python.org/3/search.html?{}&check_keywords=yes&area=default'.format(
            urlencode({'q': args}))
    return url 

def ping():
    return "pong"

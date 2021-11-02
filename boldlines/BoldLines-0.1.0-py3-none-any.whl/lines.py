import random


def getLine(type):
    if type == 'cute':
        x = ['I hope you know CPR, because you just took my breath away!',

             ' So, aside from taking my breath away, what do you do for a living?',

             'I ought to complain to Spotify for you not being named this week’s hottest single.',

             'Are you a parking ticket? ‘Cause you’ve got ‘fine’ written all over you.',

             'Your eyes are like the ocean; I could swim in them all day.',

             'When I look in your eyes, I see a very kind soul.',

             'If you were a vegetable, you’d be a ‘cute-cumber.’',

             'Do you happen to have a Band-Aid? ‘Cause I scraped my knees falling for you.',

             'I never believed in love at first sight, but that was before I saw you.',

             'I didn’t know what I wanted in a woman until I saw you',

             'I was wondering if you could tell me: If you’re here, who’s running Heaven?'

             'No wonder the sky is gray (or dark, if at night)—all the color is in your eyes.'

             'You’ve got everything I’ve been searching for, and believe me—I’ve been looking a long time.',

             'You’re like a fine wine. The more of you I drink in, the better I feel.',

             'You’ve got a lot of beautiful curves, but your smile is absolutely my favorite.',

             'Are you as beautiful on the inside as you are on the outside?',

             'If being sexy was a crime, you’d be guilty as charged.',

             'I was wondering if you’re an artist because you were so good at drawing me in.',

             'It says in the Bible to only think about what’s pure and lovely… So I’ve been thinking about you all day long.',

             'Do you have a map? I just got lost in your eyes',

             ]

        t = random.choice(x)
        return t

    elif type == 'cheesy':
        x = ['Your hand looks heavy—can I hold it for you?',

             'Are you a time traveler? Because I absolutely see you in my future.',

             'Do you know what my shirt is made of? Boyfriend material.',

             'I thought this was a (bar/restaurant/etc.), but I must be in a museum because you’re a piece of art.',

             'You know, your smile has been lighting up the room all night and I just had to come and say hello.',

             'Hi, I’m (your name). Do you remember me? Oh, that’s right—we’ve only met in my dreams.',

             'What does it feel like to be the most gorgeous girl in the room?',

             'I can’t tell if that was an earthquake, or if you just seriously rocked my world.',

             'I just had to tell you, your beauty made me truly appreciate being able to see.',

             'If you were a fruit, you’d be a ‘fine-apple',

             'I don’t know your name, but I’m sure it’s as beautiful as you are. I’m (your name).',

             'You are astoundingly gorgeous, but I can tell that’s the least interesting thing about you. I’d love to know more.',

             'The sparkle in your eyes is so bright, the sun must be jealous.',

             'One night I looked up at the stars and thought, ‘Wow, how beautiful.’ But now that I’m looking at you, nothing else can compare.',

             'If I had a nickel for every time I saw someone as beautiful as you, I’d still only have five cents.',

             'If beauty were time, you’d be eternity.',

             'I think the only way you could possibly be more beautiful is if I got to know you.',

             'I don’t know which is prettier today—the weather, or your eyes.',

             'I swear someone stole the stars from the sky and put them in your eyes.',

             'In my opinion, there are three kinds of beautiful: Cute, pretty, and sexy. Somehow, you manage to be all three.']

        t = random.choice(x)
        return t

    elif type == 'funny':
        x = ['I’d like to take you to the movies, but they don’t let you bring in your own snacks.',

             'You know what you would look really beautiful in? My arms.',

             'I would never play hide and seek with you because someone like you is impossible to find.',

             'Are you a magician? It’s the strangest thing, but every time I look at you, everyone else disappears.',

             'I think there’s something wrong with my phone. Could you try calling it to see if it works?',

             'Hi, I just wanted to thank you for the gift. (pause) I’ve been wearing this smile ever since you gave it to me.',

             'Are you an electrician? Because you’re definitely lighting up my day/night!',

             'I’ve heard it said that kissing is the ‘language of love.’ Would you care to have a conversation with me about it sometime?',

             'I always thought happiness started with an ‘h,’ but it turns out mine starts with ‘u.’',

             'I believe in following my dreams. Can I have your Instagram?'

             'Do you know what the Little Mermaid and I have in common? We both want to be part of your world.',

             'If you were a song, you’d be the best track on the album.',

             'On a scale of 1 to America, how free are you tonight?',

             'You know, I always thought that Disneyland was the ‘happiest place on Earth,’ but that was before I got a chance to stand here next to you.',

             'Want to go outside and get some fresh air with me? You just took my breath away.',

             'If you were a taser, you’d be set to ‘stun.’',

             'If you were a Transformer, you’d be ‘Optimus Fine.’',

             'Is your name Google? Because you have everything I’m searching for.',

             'Do you ever get tired from running through my thoughts all night?',

             'You know, they say that love is when you don’t want to sleep because reality is better than your dreams. And after seeing you, I don’t think I ever want to sleep again.']

        t = random.choice(x)
        return t

    else:
        x = ['cute','cheesy','funny']
        print('please pass among this thing as a type ' + str(x) + ' to get pickup lines')


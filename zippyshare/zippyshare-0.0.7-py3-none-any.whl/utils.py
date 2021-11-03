import random
import string
import requests
from lxml import html


s = requests.Session()


def gen_username(name):
    if random.randint(0, 1) == 0:
        name = name.lower()
    elif random.randint(0, 1) == 0:
        pass
    else:
        name = name.upper()
    _ = name.split(" ")
    if random.randint(0, 1) == 0:
        username = _[1]
        username += "" if random.randint(0, 1) == 0 else "_"
        username += _[0]
        username += "" if random.randint(0, 1) == 0 else "_"
    else:
        username = _[0]
        username += "" if random.randint(0, 1) == 0 else "_"
        username += _[1]
        username += "" if random.randint(0, 1) == 0 else "_"
    bday = gen_birthday()
    random.shuffle(bday)
    if random.randint(0, 1) == 0:
        username += str(bday[0])
        username += "" if random.randint(0, 1) == 0 else "_"
    if random.randint(0, 1) == 0:
        username += str(bday[1])
        username += "" if random.randint(0, 1) == 0 else "_"
    if random.randint(0, 1) == 0:
        username += str(bday[2])
        username += "" if random.randint(0, 1) == 0 else "_"
    if username.endswith("_"):
        username = username[:-1]
    return username


def gen_password(length=20):
    return "".join(random.SystemRandom().choices(string.ascii_letters+string.digits, k=length))


def gen_birthday():
    return [
        random.SystemRandom().choice([i for i in range(1970, 1990+1)]),
        random.SystemRandom().choice([i for i in range(1, 12+1)]),
        random.SystemRandom().choice([i for i in range(1, 28+1)]),
    ]


def gen_email(username):
    _ = ["gmail.com","yahoo.com","hotmail.com","aol.com","hotmail.co.uk","hotmail.fr","msn.com","yahoo.fr","wanadoo.fr","orange.fr","comcast.net","yahoo.co.uk","yahoo.com.br","yahoo.co.in","live.com","rediffmail.com","free.fr","gmx.de","web.de","yandex.ru","ymail.com","libero.it","outlook.com","uol.com.br","bol.com.br","mail.ru","cox.net","hotmail.it","sbcglobal.net","sfr.fr","live.fr","verizon.net","live.co.uk","googlemail.com","yahoo.es","ig.com.br","live.nl","bigpond.com","terra.com.br","yahoo.it","neuf.fr","yahoo.de","alice.it","rocketmail.com","att.net","laposte.net","facebook.com","bellsouth.net","yahoo.in","hotmail.es","charter.net","yahoo.ca","yahoo.com.au","rambler.ru","hotmail.de","tiscali.it","shaw.ca","yahoo.co.jp","sky.com","earthlink.net","optonline.net","freenet.de","t-online.de","aliceadsl.fr","virgilio.it","home.nl","qq.com","telenet.be","me.com","yahoo.com.ar","tiscali.co.uk","yahoo.com.mx","voila.fr","gmx.net","mail.com","planet.nl","tin.it","live.it","ntlworld.com","arcor.de","yahoo.co.id","frontiernet.net","hetnet.nl","live.com.au","yahoo.com.sg","zonnet.nl","club-internet.fr","juno.com","optusnet.com.au","blueyonder.co.uk","bluewin.ch","skynet.be","sympatico.ca","windstream.net","mac.com","centurytel.net","chello.nl","live.ca","aim.com","bigpond.net.au"]
    return username+"@"+random.SystemRandom().choice(_)


def gen_name(names=[]):
    if not names:
        r = s.get("https://www.name-generator.org.uk/quick/")
        r = html.fromstring(r.content.decode())
        names.extend([_.replace("-", "") for _ in r.xpath("////form/h2[1]/following-sibling::div/text()")[:10]])
    return names


def generate_account_info():
    template = "https://www.zippyshare.com/sites/registration.jsp\n\n"
    for i in range(0, 10):
        template += "{}\n{}\n{}\n{}\n{}\n\n".format(
            *gen_name()[i].split(" "),
            gen_username(gen_name()[i]),
            gen_password(),
            gen_email(gen_username(gen_name()[i])),
        )
    open("zippy.txt", "wb").write(template.encode())


def read_account_info(s):
    credentials = [[]]
    for line in s.splitlines()[2:]:
        if not line:
            credentials.append([])
            continue
        credentials[-1].append(line)
    return credentials


if __name__ == "__main__":
    generate_account_info()



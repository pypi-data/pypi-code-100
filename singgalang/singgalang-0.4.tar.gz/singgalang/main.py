import urwid
import time
import webbrowser
from singgalang.singgalang import main as singgalang


news = singgalang()
news = list(dict.fromkeys(news))
news_list = []
news_option = []

count = 0
for title in news:
    title = title['title'].encode('utf-8')
    news_list.append(title.title())
    news_option.append(count)

    count += 1
choices = news_list

def menu(title, choices):
    body = [urwid.Text(title), urwid.Divider()]
    for i in range(len(choices)):
        button = urwid.Button(choices[i].decode())
        urwid.connect_signal(button, 'click', item_chosen, str(news_option[i]))
        body.append(urwid.AttrMap(button, None, focus_map='reversed'))

        i += 1
    return urwid.ListBox(urwid.SimpleFocusListWalker(body))

def item_chosen(button, choice):
    link = news[int(choice)]['url']
    webbrowser.open(link)

main = urwid.Padding(menu(u'Harian Singgalang - ' + time.ctime(), choices), left=2, right=2)
top = urwid.Overlay(main, urwid.SolidFill(u'\N{MEDIUM SHADE}'),
    align='center', width=('relative', 90),
    valign='middle', height=('relative', 80),
    min_width=20, min_height=9)

def exit_on_unhandle(key):
    pass

def run():
    urwid.MainLoop(top, unhandled_input=exit_on_unhandle,palette=[("reversed","yellow","dark cyan")]).run()

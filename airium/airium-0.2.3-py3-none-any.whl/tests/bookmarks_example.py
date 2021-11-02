from airium import Airium

LOREM_TEXT = \
    'Lorem ipsum dolor sit amet, consectetur adipiscing elit, sed do' \
    'eiusmod tempor incididunt ut labore et dolore magna aliqua. Ut enim ad' \
    'minim veniam, quis nostrud exercitation ullamco laboris nisi ut aliquip' \
    'ex ea commodo consequat. Excepteur sint occaecat cupidatat non proident, ' \
    'sunt in culpa qui officia deserunt mollit anim id est laborum consectetur ' \
    'adipiscing elit, sed do eiusmod tempor incididunt ut labore et dolore magna ' \
    'aliqua. Ut enim ad minim veniam, quis nostrud exercitation ullamco laboris ' \
    'nisi ut aliquip ex ea commodo consequat.'

a = Airium()

with a.h1(style='padding: 66px', id='top'):  # <- here is the 'top' identifier (bookmark target)
    a('Bookmark example')

with a.div(style='width: 400px; margin: 30px;'):
    # The div is not necessary - it just makes a narrow column of text
    # in order to see the bookmarks working.

    a.h2(_t='INDEX')
    with a.ol():
        with a.a(href='#unique_identifier_1'):  # <- here is how to make a bookmark link
            a.li(_t='chapter 1')
        with a.a(href='#another_unique_identifier_2'):
            a.li(_t='chapter 2')
        with a.a(href='#unique_identifier_3'):
            a.li(_t='chapter 3')
        with a.a(href='#my_turbo_id'):
            a.li(_t='chapter 4')

    # CHAPTER 1
    a.h3(style='padding: 26px', id='unique_identifier_1', _t='Chapter 1')  # <- here is the 'unique_identifier_1'
    with a.p():
        a(LOREM_TEXT)
    a.a(href="#top", _t="back to top")

    # CHAPTER 2
    a.h3(style='padding: 26px', id='another_unique_identifier_2', _t='Chapter 2')
    with a.p():
        a(LOREM_TEXT)
    a.a(href="#top", _t="back to top")

    # CHAPTER 3
    a.h3(style='padding: 26px', id='unique_identifier_3', _t='Chapter 3')
    with a.p():
        a(LOREM_TEXT)
    a.a(href="#top", _t="back to top")

    # CHAPTER 4
    a.h3(style='padding: 26px', id='my_turbo_id', _t='Chapter 4')
    with a.p():
        a(LOREM_TEXT)
    a.a(href="#top", _t="back to top")

# Store the file:
with open('/tmp/file.html', 'w') as f:
    f.write(str(a))

print("Document generated in /tmp/file.html")

import muzzle

xml = '''<?xml version="1.0" encoding="UTF-8"?>
<document>
    <header>
        <fields>
            <field name="name">Muzzle</field>
            <field name="date">2021-11-02</field>
        </fields>
        <title>Hello, this is a title</title>
    </header>
    <body>
        <text>This is a text</text>
        <image url="https://example.com/test.png" title="Test-Image"></image>
    </body>
</document>
'''

xmlparser = muzzle.XMLParser()
obj = xmlparser.parse(xml)
print(obj)

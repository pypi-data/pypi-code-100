import xml.etree.ElementTree as ET
import message_profile_eng
tree = ET.parse('engine_profile/engine_profile_2.xml')
root = tree.getroot()
# d = {}
print(root.tag, root.attrib, '\n')
if 'HRIEngineProfile' in root.tag:
    e = message_profile_eng.HRI_Engine_Profile()
    for x in root:
        # d[x.tag] = x.text
        #print(x.tag, x.attrib)
        if 'identifier' in x.tag:
            e.identifier = x.text.lstrip()  #lstrip:左端の文字列を削除
                                            # ただ引数に何もない。必要性は？
        if 'name' in x.tag:
            e.name = x.text.lstrip()
        if 'SubProfile' in x.tag:
            #e.sub_profile = x.text.lstrip()
            s = message_profile_eng.HRI_Engine_Profile()
            for y in x:
                #print('y', y.tag, y.attrib)
                if 'identifier' in y.tag:
                    #print(y.text)
                    s.identifier = y.text.lstrip()
                    #e.add_engine(y.text)
                    #e.sub_profile = y.text.lstrip()
                if 'name' in y.tag:
                    #print(y.text)
                    s.name = y.text.lstrip()
                    e.add_engine(s)
                    #e.add_engine(y.text)
                    #e.sub_profile = y.text.lstrip()
                if 'HRIComponent' in y.tag:
                    c = message_profile_eng.HRI_Component_Profile()
                    c.identifier = y.text.lstrip() #これをprintすればコンポーネントのIDが出力できる
                    s.add_component(c) 
                    #e.component = y.text.lstrip()
                    #e.add_component(y.text)
                    #print(y.text.lstrip())
        elif 'HRIComponent' in x.tag:
            c = message_profile_eng.HRI_Component_Profile()
            c.identifier = x.text.lstrip()
            e.add_component(c)
                
e.show()

# e = message_profile.HRI_Engine_Profile(d["{http://www.opengis.net/gml/3.2}identifier"], d["{http://www.opengis.net/gml/3.2}name"])
# print(e)
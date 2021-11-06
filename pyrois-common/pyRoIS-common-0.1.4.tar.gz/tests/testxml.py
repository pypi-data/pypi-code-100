import xml.etree.ElementTree as ET
import message_profile
tree = ET.parse('component_profile/component_profile.xml')
root = tree.getroot()
# d = {}
print(root.tag, root.attrib)
if 'HRIComponentProfile' in root.tag:
    p = message_profile.HRI_Component_Profile()
    for x in root:
        # d[x.tag] = x.text
        print(x.tag, x.attrib)
        if 'identifier' in x.tag:
            p.identifier = x.text.lstrip()
        if 'name' in x.tag:
            p.name = x.text.lstrip()
        if 'MessageProfile' in x.tag:
            m = message_profile.Message_Profile()
            m.name = x.attrib["{http://www.omg.org/spec/RoIS/20151201}name"]
            m.type = x.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"]
            p.add_message(m)
            for y in x:
                print('y', y.tag, y.attrib)
                if 'Results' in y.tag:
                    r = message_profile.Parameter_Profile()
                    r.name = y.attrib["{http://www.omg.org/spec/RoIS/20151201}name"]
                    m.add_result(r)
                    for z in y:
                        print(z.tag, z.attrib)
                        if 'data_type_ref' in z.tag:
                            r.data_type_ref = z.attrib["{http://www.omg.org/spec/RoIS/20151201}code"]


p.show()

# e = message_profile.HRI_Engine_Profile(d["{http://www.opengis.net/gml/3.2}identifier"], d["{http://www.opengis.net/gml/3.2}name"])
# print(e)
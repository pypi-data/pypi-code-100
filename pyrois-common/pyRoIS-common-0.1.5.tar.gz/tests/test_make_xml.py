import message_profile_test
import xml.etree.ElementTree as ET

tree = ET.parse('engine_profile/engine_profile_binding.xml')
root = tree.getroot()
ET.register_namespace('rois','http://www.omg.org/spec/RoIS/20151201')
ET.register_namespace('gml','http://www.opengis.net/gml/3.2')

doc1 = ET.Element('{http://www.omg.org/spec/RoIS/20151201}HRIEngineProfile')
# doc2 = ET.Element('{http://www.omg.org/spec/RoIS/20151201}SubProfile')
# doc3 = ET.Element('{http://www.opengis.net/gml/3.2}name')
doc1.set('{http://www.opengis.net/gml/3.2}id', 'engine_profile')

# sub_pro = ET.SubElement(doc1, '{http://www.omg.org/spec/RoIS/20151201}SubProfile')
# sub_id = ET.SubElement(sub_pro, '{http://www.opengis.net/gml/3.2}identifier')
# sub_id.text = ('urn:x-rois:def:HRIEngine:ATR::SubEng01')
# ET.dump(doc1)

e = message_profile_test.HRI_Engine_Profile()

# print(root.tag, root.attrib)
for x in root:
    if 'identifier' in x.tag:
        # x.text = e.identifier
        x.text = "urn:x-rois:def:HRIEngine:ATR::MainHRI"
    if 'name' in x.tag:
    #     x.text = e.name
        x.text = "mainHRI"
    if len(e.sub_profile) >= 1:
        s = message_profile_test.HRI_Engine_Profile()
        sub_pro = ET.SubElement(doc1, '{http://www.omg.org/spec/RoIS/20151201}SubProfile')
        print('OK')

        # for a in e.sub_profile:
        #     sub_pro = ET.SubElement(doc1, '{http://www.omg.org/spec/RoIS/20151201}SubProfile')
         
           
    #         sub_id = ET.SubElement(doc1,'gml:identifier')
    #         sub_name = ET.SubElement(doc1,'gml:name')
    #         for y in x:    
    #             if 'identifier' in y.tag:
    #                 y.text = s.identifier[y-1] #要確認
    #             if 'name' in y.tag:
    #                 y.text = s.name #message_profileに関数/配列を追加する必要あり
    #                 for b in s.component:
    #                     comp_id = ET.SubElement('doc2,'rois:HRIComponent')
    #                 if 'HRIComponent' in y.tag:
    #                     y.text = s.component[y-1]
    else:
        pass
    #     for c in e.component:
    #         comp_id2 = ET.SubElement(a,'rois:HRIComponent')
    #     if 'HRIComponent' in x.tag:
    #         x.text = s.component[x-1]

test = ET.ElementTree(doc1)
test.write('engine_profile/engine_profile_binding_2.xml',xml_declaration=True,encoding="UTF-8",short_empty_elements=False)
# tree = ET.ElementTree(root)
# tree.write('engine_profile/engine_profile_binding_2.xml',xml_declaration=True,encoding="UTF-8")
import message_profile
import xml.etree.ElementTree as ET
import xml.dom.minidom


ET.register_namespace('rois','http://www.omg.org/spec/RoIS/20151201')
ET.register_namespace('gml','http://www.opengis.net/gml/3.2')


e = message_profile.HRI_Engine_Profile(
identifier = "urn:x-rois:def:HRIEngine:Kyutech::mainEng",
name = "mainEng"
)

# comp0 = ["urn:x-rois:def:HRIComponent:Kyutech:main:SystemInformation",
#         "urn:x-rois:def:HRIComponent:Kyutech:main:Move"]
# for x in comp0:
#     e.add_component(x)

s1 = message_profile.HRI_Engine_Profile(
identifier = "urn:x-rois:def:HRIEngine:Kyutech::SubEng01",
name = "subEng01"
)
e.add_engine(s1)

# s1.add_component("urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonDetection")
# s1.add_component("urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification")
c1 = message_profile.HRI_Component_Profile()
comp1 = ["urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonDetection",
        "urn:x-rois:def:HRIComponent:Kyutech:sub01:PersonIdentification"]
for x in comp1:
    s1.add_component(x)
    c1.identifier = x
    c1.show()



s2 = message_profile.HRI_Engine_Profile(
identifier = "urn:x-rois:def:HRIEngine:Kyutech::SubEng02",
name = "subEng02"
)
e.add_engine(s2)

c2 = message_profile.HRI_Component_Profile()
comp2 = ["urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceDetection",
        "urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization",
        "urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation"]
for x in comp2:
    s2.add_component(x)
    c2.identifier = x
    c2.show()

print(e.toxml())


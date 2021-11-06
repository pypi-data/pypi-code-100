# message_profile.py
#
# Copyright 2019 Eiichi Inohira
# Copyright 2019 Ryota Higashi

import xml.etree.ElementTree as ET
import xml.dom.minidom
import re
import sys

class IO_IdentifiedObject:
    def __init__(self):
        self.identifier = None
        self.name = None

class Parameter_Profile:
    def __init__(self):
        self.name = None
        self.data_type_ref = None
        self.default_value = None
        self.description = None
    def show(self):
        print('Parameter_Profile')
        print('+ name', self.name)
        print('+ data_type_ref', self.data_type_ref)

class Message_Profile:
    def __init__(self):
        self.name = None
        self.type = None
        self.results = []
    def add_result(self, r):
        self.results.append(r)
    def show(self):
        print('Message_Profile')
        print('+ name', self.name)
        print('type', self.type)
        if len(self.results) > 0:
            print('results')
            for x in self.results:
                x.show()

class HRI_Component_Profile(IO_IdentifiedObject):
    def __init__(self):
        self.identifier = None
        self.name = None
        self.parameter = []
        self.subcomponent = []
        self.message = []
    def add_parameter(self, p):
        self.parameter.append(p)
    def add_subcomponent(self, s):
        self.subcomponent.append(s)
    def add_message(self, m):
        self.message.append(m)
    def show(self):
        print('HRI_Component_Profile')
        print('identifier', self.identifier)
        print('name', self.name)
        print('p:s:m',len(self.parameter), len(self.subcomponent), len(self.message))
        for x in self.parameter:
            x.show()
        for x in self.subcomponent:
            x.show()
        for x in self.message:
            x.show()
        print("---")

class HRI_Engine_Profile(IO_IdentifiedObject):
    def __init__(self,identifier=None,name=None):
        self.identifier = identifier
        self.name = name
        self.component = []
        self.sub_profile = []
    def add_component(self, c):
        self.component.append(c)
    def add_engine(self, e):
        self.sub_profile.append(e)
    def show(self):
        for x in self.component:
            x.show()
        for x in self.sub_profile:
            x.show()
    def toxml(self,doc1=None):
        if doc1 is None:
            ET.register_namespace('rois','http://www.omg.org/spec/RoIS/20151201')
            ET.register_namespace('gml','http://www.opengis.net/gml/3.2')
            root = ET.Element('{http://www.omg.org/spec/RoIS/20151201}HRIEngineProfile')
            root.set('{http://www.opengis.net/gml/3.2}id', 'engine_profile')
        else:
            root = ET.SubElement(doc1, 'rois:SubProfile')

        ET.SubElement(root, 'gml:identifier').text = self.identifier
        ET.SubElement(root, 'gml:name').text = self.name
        if len(self.component) >= 1:
            for x in self.component:
                ET.SubElement(root, 'rois:HRIComponent').text = x
                #print(a)
        else:
            pass
        # for x in self.component:
        #         x.toxml(root)
        for x in self.sub_profile:
            x.toxml(root)
        if doc1 is None:
            # ET.dump(root)
            s = ET.tostring(root,encoding='utf-8').decode('utf-8')
            x = xml.dom.minidom.parseString(s)
            return x.toprettyxml()

# class Search_Component():
#     def __init__(self):
#         self.eng_pro = None
#     def analysis(self):
#         file_name = 'engine_profile/' + self.eng_pro + '.xml'
#         tree = ET.parse(file_name)
#         root = tree.getroot()
#         comp_list = []
#         if 'HRIEngineProfile' in root.tag:
#             for x in root:
#                 if 'SubProfile' in x.tag:
#                     for y in x:
#                         if 'HRIComponent' in y.tag:
#                             comp_list.append(y.text.lstrip())
#                 elif 'HRIComponent' in x.tag:
#                     comp_list.append(x.text.lstrip())

#         return comp_list


class Analyze_Engine_Profile:
    def __init__(self, file_name, my_engine_urn=None):
        self.file_name = file_name
        self.my_engine_urn = my_engine_urn
        self.comp_list = []
        self.main_eng_urn = ""
        self.main_comp = []
        self.sub_eng_urn = ""
        self.sub_comp = []
        self.eng_comp_urn = {}
        self.address = self.file_name + '.xml'
        with open(self.address,'r') as f:
            self.profile = f.read()

    def analysis(self):
        # try:
        tree = ET.parse(self.address)
        root = tree.getroot()
        if 'HRIEngineProfile' in root.tag:
            for x in root:
                if 'identifier' in x.tag:
                    self.main_eng_urn = x.text.lstrip()
                elif 'HRIComponent' in x.tag:
                    self.main_comp.append(x.text.lstrip())
                elif 'SubProfile' in x.tag:
                    for y in x:
                        if 'identifier' in y.tag:
                            self.sub_eng_urn = y.text.lstrip()
                        elif 'HRIComponent' in y.tag:
                            self.sub_comp.append(y.text.lstrip())
                    if self.sub_eng_urn == self.my_engine_urn:
                        self.eng_comp_urn = {}
                        self.eng_comp_urn[self.sub_eng_urn] = self.sub_comp
                        return (self.profile, self.eng_comp_urn, self.sub_comp)
                    self.eng_comp_urn[self.sub_eng_urn] = self.sub_comp
                    self.sub_comp = []

                self.eng_comp_urn[self.main_eng_urn] = self.main_comp
        
        if self.my_engine_urn in self.eng_comp_urn.keys() or self.my_engine_urn == None:
            pass
        else:
            print("my_engine_urn error: Specified URN does not exist")
            sys.exit()
        # エンジンとコンポーネントの対応辞書からコンポーネントの一覧リストを作成する方法
        for c in self.eng_comp_urn.values():
            self.comp_list.extend(c)
        return (self.profile, self.eng_comp_urn, self.comp_list)


class Analyze_Component_Profile:
    def __init__(self, comp_name):
        self.comp_name = comp_name
        self.profile = []
        # self.profile_list = {}
    
    def get_profile(self):
        comp_pro = {'SystemInformation':'component_profile_SI','PersonDetection':'component_profile_PD',
                    'PersonLocalization':'component_profile_PL','PersonIdentification':'component_profile_PI',
                    'FaceDetection':'component_profile_FD','FaceLocalization':'component_profile_FL',
                    'SoundDetection':'component_profile_SD','SoundLocalization':'component_profile_SL',
                    'SpeechRecognition':'component_profile_SR','GestureRecognition':'component_profile_GR',
                    'SpeechSynthesis':'component_profile_SS','Reaction':'component_profile_R',
                    'Navigation':'component_profile_N','Follow':'component_profile_F','Move':'component_profile_M'}
        try:
            self.address = 'tests/component_profile/' + comp_pro[self.comp_name] + '.xml'
            with open(self.address,'r') as f:
                self.profile = [f.read()]
        except:
            self.profile = None
        
        # for x in comp_pro.values():
        #     self.profile_list[x] = open('component_profile/' + x + '.xml','r').read()

        # return (self.profile, self.profile_list)
        return self.profile



# class Get_Parameter(): # 同じ種類のコンポーネントで接続するエンジンが違うものを区別できていない
#     # エンジンごとにコンポーネントのフォルダを作るべきか，xmlファイルじゃなくて大きなリスト，2次元は配列で管理するか…
#     def __init__(self, comp_ref):
#         self.comp_ref = comp_ref
#         self.file_name = None
#     def get_parameter(self):
#         # m = re.search(r'(\w+)\:(\w+)\:(\w+)\:(\w+)\:(\w+)\:(\w+)',self.comp_ref)
#         # comp_name = m.group(6)        
#         m = self.comp_ref.split(':')
#         comp_name = m[6]
#         comp_pro = {'SystemInformation':'component_profile_SI','PersonDetection':'component_profile_PD',
#                     'PersonLocalization':'component_profile_PL','PersonIdentification':'component_profile_PI',
#                     'FaceDetection':'component_profile_FD','FaceLocalization':'component_profile_FL',
#                     'SoundDetection':'component_profile_SD','SoundLocalization':'component_profile_SL',
#                     'SpeechRecognition':'component_profile_SR','GestureRecognition':'component_profile_GR',
#                     'SpeechSynthesis':'component_profile_SS','Reaction':'component_profile_R',
#                     'Navigation':'component_profile_N','Follow':'component_profile_F','Move':'component_profile_M'}
#         self.file_name = 'component_profile/' + comp_pro[comp_name] + '.xml'
#         tree = ET.parse(self.file_name)
#         root = tree.getroot()
#         para_list = []
#         if 'HRIComponentProfile' in root.tag:
#             # p = HRI_Component_Profile()
#             for x in root:
#                 # if 'identifier' in x.tag:
#                 #     p.identifier = x.text.lstrip()
#                 # if 'name' in x.tag:
#                 #     p.name = x.text.lstrip()
#                 # if 'MessageProfile' in x.tag:
#                 #     m = Message_Profile()
#                 #     m.name = x.attrib["{http://www.omg.org/spec/RoIS/20151201}name"]
#                 #     m.type = x.attrib["{http://www.w3.org/2001/XMLSchema-instance}type"]
#                 #     p.add_message(m)
#                 #     for y in x:
#                 #         print('y', y.tag, y.attrib)
#                 #         if 'Results' in y.tag:
#                 #             r = Parameter_Profile()
#                 #             r.name = y.attrib["{http://www.omg.org/spec/RoIS/20151201}name"]
#                 #             m.add_result(r)
#                 #             for z in y:
#                 #                 print(z.tag, z.attrib)
#                 #                 if 'data_type_ref' in z.tag:
#                 #                     r.data_type_ref = z.attrib["{http://www.omg.org/spec/RoIS/20151201}code"]
#                 if 'ParameterProfile' in x.tag:
#                     pp = Parameter_Profile()
#                     pp.name = x.attrib["{http://www.omg.org/spec/RoIS/20151201}name"]
#                     pp.default_value = x.attrib["{http://www.omg.org/spec/RoIS/20151201}default_value"]
#                     pp.description = x.attrib["{http://www.omg.org/spec/RoIS/20151201}description"]
#                     for y in x:
#                         if 'data_type_ref' in y.tag:
#                             pp.data_type_ref = y.attrib["{http://www.omg.org/spec/RoIS/20151201}code"]
#                     # exec("para%d = [%s,%s,%s]" %(x,pp.name,pp.data_type_ref,pp.default_value))
#                     # para_list.append("para%d"%(x))
#                     para_list.append(pp.name)
#                     para_list.append(pp.data_type_ref)
#                     para_list.append(pp.default_value)

#         return para_list

# class Set_Parameter():
#     def __init__(self, comp_ref, para):
#         self.comp_ref = comp_ref
#         self.para = para
#     def set_parameter(self):
#         a = Get_Parameter(self.comp_ref)
#         a.get_parameter()
#         tree = ET.parse(a.file_name)
#         root = tree.getroot()
#         if 'HRIComponentProfile' in root.tag:
#             for x in root:
#                 if 'ParameterProfile' in x.tag:
#                     x.set("{http://www.omg.org/spec/RoIS/20151201}name",self.para[x][0])
#                     x.set("{http://www.omg.org/spec/RoIS/20151201}default_value",self.para[x][2])
#                     # x.attrib["{http://www.omg.org/spec/RoIS/20151201}description"]
#                     for y in x:
#                         if 'data_type_ref' in y.tag:
#                             y.set("{http://www.omg.org/spec/RoIS/20151201}code",self.para[x][1])
        



if __name__ == "__main__":
    # test = Get_Parameter("urn:x-rois:def:HRIComponent:Kyutech:eng1:SpeechRecognition") # ":(none):"の時対応できない 文字の指定を(\s+)にすればスペースは検索できる
    # print(test.get_parameter())
    # print(test.file_name)
    # test = Set_Parameter("urn:x-rois:def:HRIComponent:Kyutech:eng1:SpeechRecognition",
    # [['rule', 'string', 'default'], ['languages', 'string[]', 'jp'], ['grammar', 'string', 'default']])
    # test.set_parameter()

    test = Analyze_Engine_Profile("engine_profile_2","urn:x-rois:def:HRIEngine:Kyutech::SubEng01")
    (profile,eng_comp,comp_list) = test.analysis()
    print(profile, eng_comp, comp_list)

    test2 = Analyze_Engine_Profile("engine_profile_2","")
    (profile,eng_comp,comp_list) = test2.analysis()
    print(profile, eng_comp, comp_list)
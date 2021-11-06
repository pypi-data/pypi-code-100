# command_message_test.py

import command_message
import json
import itertools

# c_ri = command_message.RoIS_Identifier("","")
# c_p1 = command_message.Parameter("detection_threshold", c_ri, 555)
# c_p2 = command_message.Parameter("minimum_interval", c_ri, 222)
# c_al = command_message.ArgumentList([c_p1,c_p2])
# c_cb = command_message.CommandBase(5) # 反映されない気がする ソースいじる必要がある？
# c_cm = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:main:PersonLocalization',"set_parameter","",c_al) # command_id引数いらない
# c_cm.delay_time = 5
# c_b = command_message.Branch([c_cm])
# c_cc = command_message.ConcurrentCommands([c_b])
# c_cc.delay_time =10
# c_cus = command_message.CommandUnitSequence([c_cm,c_cc])
# print(c_cus.__dict__)
# print(c_cus.command_unit_list[0].__class__.__name__)
# print(vars(c_cus.command_unit_list[0].arguments))
# # print(vars(c_cus.command_unit_list[0].arguments[0]))

def object_to_json(item):
    if isinstance(item, object) and hasattr(item, '__dict__'):
        return item.__dict__
    else:
        raise TypeError



# j=json.dumps(c_cus, default=object_to_json, indent=4)
# print(j)

# obj=json.loads(j)
# print(obj)

# class ObjectLike(dict):
#     __getattr__ = dict.get
  
# obj = json.loads(j, object_hook=ObjectLike)
# print(obj)
# print(obj.command_unit_list[0].arguments.parameters[0].name)


c_ri = command_message.RoIS_Identifier("","")
c_p_ss1 = command_message.Parameter("speech_text", c_ri, "aaa")
c_p_ss2 = command_message.Parameter("SSML_text", c_ri, "ssml")
c_p_ss3 = command_message.Parameter("volume", c_ri, 50)
c_p_ss4 = command_message.Parameter("languages", c_ri, "japanese")
c_p_ss5 = command_message.Parameter("character", c_ri, "m1")
c_al1 = command_message.ArgumentList([c_p_ss1,c_p_ss2,c_p_ss3,c_p_ss4,c_p_ss5])
c_cm1 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis',"set_parameter","",c_al1)
c_cm1.delay_time = 0

c_p = command_message.Parameter("", c_ri, "")
c_al2 = command_message.ArgumentList([c_p])
c_cm2 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub01:SpeechSynthesis',"get_parameter","",c_al2)
c_cm2.delay_time = 0

c_p_fl1 = command_message.Parameter("detection_threshold", c_ri, 3)
c_p_fl2 = command_message.Parameter("minimum_interval", c_ri, 2)
c_al3_1_1 = command_message.ArgumentList([c_p_fl1,c_p_fl2])
c_cm3_1_1 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization',"set_parameter","",c_al3_1_1)
c_cm3_1_1.delay_time = 3000

c_p_n1 = command_message.Parameter("target_position", c_ri, [100.0,200.0])
c_p_n2 = command_message.Parameter("time_limit", c_ri, 60000)
c_p_n3 = command_message.Parameter("routing_policy", c_ri, "time priority")
c_al3_1_2 = command_message.ArgumentList([c_p_n1,c_p_n2,c_p_n3])
c_cm3_1_2 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub02:Navigation',"set_parameter","",c_al3_1_2)
c_cm3_1_2.delay_time = 4000

c_p_m1 = command_message.Parameter("line", c_ri, [1000,360])
c_p_m2 = command_message.Parameter("curve", c_ri, [1000,90])
c_p_m3 = command_message.Parameter("time", c_ri, 1000)
c_al3_2 = command_message.ArgumentList([c_p_m1,c_p_m2,c_p_m3])
c_cm3_2 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub03:Move',"set_parameter","",c_al3_2)
c_cm3_2.delay_time = 5000
# c_p_fl3 = command_message.Parameter("detection_threshold", c_ri, 3)
# c_p_fl4 = command_message.Parameter("minimum_interval", c_ri, 2)
# c_al3_2 = command_message.ArgumentList([c_p_fl3,c_p_fl4])
# c_cm3_2 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub02:FaceLocalization',"set_parameter","",c_al3_2)
# c_cm3_2.delay_time = 3000

c_b1 = command_message.Branch([c_cm3_1_1,c_cm3_1_2])
c_b2 = command_message.Branch([c_cm3_2])
c_cc = command_message.ConcurrentCommands([c_b1,c_b1,c_b2,c_b2])
c_cc.delay_time = 0

c_p_f1 = command_message.Parameter("target_object_ref", c_ri, "human1")
c_p_f2 = command_message.Parameter("distance", c_ri, 500)
c_p_f3 = command_message.Parameter("time_limit", c_ri, 60000)
c_al4 = command_message.ArgumentList([c_p_f1,c_p_f2,c_p_f3])
c_cm4 = command_message.CommandMessage('urn:x-rois:def:HRIComponent:Kyutech:sub01:Follow',"set_parameter","",c_al4)
c_cm4.delay_time = 1000    

c_cus1 = command_message.CommandUnitSequence([c_cm1,c_cm2,c_cc,c_cc,c_cm4])

j=json.dumps(c_cus1, default=object_to_json, indent=4)
d=json.loads(j)

# print(d)
# print(next(iter(d.values())))

# d = {}

# 変数名は要変更
# if next(iter(d)) == "command_unit_list":
branch_list_num = 0
is_correct = True
if "command_unit_list" in d.keys():
    command_list = d["command_unit_list"]
    for command in command_list:
        if "branch_list" in command.keys():
            branch_list_num += 1
            branch_num = 0
            all_branch_comprefs = {}
            for branch in command["branch_list"]:
                branch_num += 1
                branch_command_list = branch["command_list"]
                component_refs = [branch_command["component_ref"] for branch_command in branch_command_list if branch_command["command_type"] == "set_parameter"]
                all_branch_comprefs[branch_num] = component_refs
            print(all_branch_comprefs)
            for combi in itertools.combinations(all_branch_comprefs.keys(),2):
                # print(combi)
                common = set(all_branch_comprefs[combi[0]]).intersection(set(all_branch_comprefs[combi[1]]))
                # print(common)
                if len(common) > 0:
                    is_correct = False
                    print("Execute(~~~) [BranchList_num:{}, Branch_Combination:{}, Same_Components:{}]: Cannot access the set_parameter in the same component from different branches.".format(branch_list_num,combi,common))
    if is_correct == False:
        print("False")
    else:
        print("True")
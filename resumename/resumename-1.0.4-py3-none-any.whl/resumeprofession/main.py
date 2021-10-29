# encoding=utf-8
# @Author=zhukai@eccom.com.cn
# @Date=2021/10/29
# @Utility: 抽取专业名称

import os
import re
import logging

# logging configuration
logger = logging.getLogger(__name__)
logging.basicConfig(format="%(asctime)s-%(name)s-%(levelname)s-%(message)s", level=logging.INFO)


def load_zhuanye(data_dir=os.path.join(os.path.dirname(os.path.abspath(__file__)), "zhuanye.txt")):
    zy = list()
    with open(data_dir, "rt", encoding="utf-8") as fp:
        for line in fp.readlines():
            if not line.startswith("#"):
                line = line.strip().split()
                if line:
                    zy.append(line[0].strip())

    return zy


class ProfessionParser(object):
    """ Extract profession name from resume. """

    def __init__(self):
        self.zy = load_zhuanye()
        logger.info(f"Total profession has {len(self.zy)}, and Top10 is {', '.join(self.zy[:10])}......")

        pattern_str = r"\b(" + "|".join(self.zy) + r")(?:专业)?\b"
        self.zy_pattern = re.compile(pattern_str)

    def parse(self, content):
        if not content:
            return None

        # match = re.search(r"专\s*业[:：]\s*(?P<profession>\w{2,12})\b", content)
        # if match:
        #     return match.group("profession")

        # remove noise from curriculum
        content = re.sub(r"((主修|核心|主要|专业)课程|专业描述|主修)[:：]\s*([\w，、,;；。+ \t\r]+(\n)*){1,3}", "", content)

        edu_flag = re.search("教育背景|教育经历|学习经历|求学经历|教育概况|教育与培训|学历教育", content)
        if edu_flag:
            edu_start = edu_flag.start()

            # split resume by keywords
            positions = set()
            positions.add(edu_start)

            work_flag = re.search(r"工作经历|工作经验|工作背景|工作历史|工作简介|工作能力", content)
            if work_flag:
                positions.add(work_flag.start())

            project_flag = re.search(r"项目经历|项目总结|项目经验", content)
            if project_flag:
                positions.add(project_flag.start())

            school_flag = re.search(r"校园经历|在校经历|在校情况|实习经历|实习经验|实践经历|社团(与|和)组织经历", content)
            if school_flag:
                positions.add(school_flag.start())

            evaluate_flag = re.search(r"个人评级|自我评级|个人优势|个人总结|个人综述|自我总结", content)
            if evaluate_flag:
                positions.add(evaluate_flag.start())

            skill_flag = re.search(r"专业技能|个人技能|职业技能|技能(与|及)证书|技能/证书及其他|"
                                   r"获奖证书|职业证书|技能证书|相关技能|相关证书|奖项/证书", content)
            if skill_flag:
                positions.add(skill_flag.start())

            positions = sorted(positions)

            # get span of education information based split positions
            idx = positions.index(edu_start)
            if idx < len(positions) - 1:
                edu_span = content[edu_start: positions[idx+1]]
            else:
                edu_span = content[edu_start:]

            match_ls = re.findall(self.zy_pattern, edu_span)

            if match_ls:
                return ', '.join(set(match_ls))
            # else:
            #     temp = re.split(r"\s+", edu_span)
            #     candidates = list()
            #     for item in temp:
            #         prefix = tuple([str(_) for _ in range(1, 10)])
            #         if item.startswith(prefix):
            #             continue
            #         elif "大学" in item or "学院" in item:
            #             continue
            #         else:
            #             candidates.append(item)
            #
            #     if candidates:
            #         return "; ".join(candidates)

        match = re.search(self.zy_pattern, content)  # search only one item
        if match:
            return match.group()

        return None


if __name__ == "__main__":
    boss_txt_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "boss_txt")
    files = os.listdir(boss_txt_dir)

    parser = ProfessionParser()

    for file in files:
        with open(os.path.join(boss_txt_dir, file), "rt") as fp:
            ct = fp.read()
            print(f"{file.strip('.txt')}", parser.parse(ct))

            # print(file.strip(".txt"))
            # match = re.search(r"(主修|核心|主要|专业)课程[:：]\s*([\w，、,;；。+ \t\r]+(\n)*){1,3}", ct)
            # if match:
            #     print(match.group())
            print('**************\n')
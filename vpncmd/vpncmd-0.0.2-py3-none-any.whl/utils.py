import requests
from lxml import html
import re
import os


def gen_helper(url):
    def convert_namespace(v):
        if v.startswith("/"):
            v = "_"+v[1:]
        if ":" in v:
            v = v.replace(":", "_")
        if "|" in v:
            v = v.replace("|", "_")
        if re.search(r"^[0-9]", v):
            v = "_"+v
        return v
    r = s.get(url)
    r = html.fromstring(r.content.decode())
    commands = r.xpath("//div[starts-with(@id, 'section_')]//table")
    template = '''    def {}(self{}):
        # {}
        _cmd = [_ for _ in (None, {}) if _]
        return self.cmd("{}", *_cmd)

'''
    classname = url.split("6.")[-1][2:].replace("_Command_Reference_", "").replace("_Command_Reference", "")
    classname = classname.replace("%2F", "").replace("(", "_").replace(")", "").replace("__", "_")
    code = "class {}:\n".format(classname)
    for _ in commands:
        anchor = _.xpath("./preceding-sibling::span/@id")[0]
        command = _.xpath("./tbody/tr[1]/td[2]//*/text()")[0]
        args = _.xpath("./tbody//*[contains(text(), 'Arguments for \"{}\"')]/../../following-sibling::tr/td[1]".format(command))
        if args[0].xpath("./text()"):
            args = []
        else:
            args = [_.xpath(".//*/text()")[0] for _ in args]
        code += template.format(
            command,
            (", " if args else "")+", ".join(convert_namespace(_)+"=None" for _ in args),
            url+"#"+anchor,
            ", ".join('"{a}:"+{b} if {b} else None'.format(a=_, b=convert_namespace(_)) if _.startswith("/") else convert_namespace(_) for _ in args) if args else "",
            command,
        )
    code += "    def cmd(self, *args, **kwargs):\n        pass\n\n"
    return code


if __name__ == "__main__":
    s = requests.Session()
    base = "https://www.softether.org/4-docs/1-manual/6._Command_Line_Management_Utility_Manual/"
    urls = [
        "6.3_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Entire_Server)",
        "6.4_VPN_Server_%2F%2F_VPN_Bridge_Management_Command_Reference_(For_Virtual_Hub)",
        "6.5_VPN_Client_Management_Command_Reference",
        "6.6_VPN_Tools_Command_Reference",
    ]
    codes = ""
    for _ in urls:
        codes += gen_helper(base+_)+"\n"
    open(os.path.join(os.path.dirname(os.path.abspath(__file__)), "helper.py"), "wb").write(codes.encode())


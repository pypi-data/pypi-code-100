import vpncmd
import re
import time


vc = vpncmd.VPNCMD(r"C:\Program Files\SoftEther VPN Client\vpncmd_x64.exe", True)
vc.setup_cmd("/client", "localhost")
# vc.VPN_Client_Management.NicCreate("VPN2")
preferred_vpns = [_[:-1] for _ in vc.filter_vpns(
    column="IP",
    value=re.compile(r"219\.100\.37\."),
    sort="NumVpnSessions",
    order="asc"
)]
print(preferred_vpns)
_SERVER = "{}:{}".format(preferred_vpns[0][1], 443)
name = "VPN@{}".format(_SERVER)
vc.VPN_Client_Management.AccountCreate(
    name=name,
    _SERVER=_SERVER,
    _HUB="vpngate",
    _USERNAME="vpn",
    _NICNAME="VPN2"
)
vc.VPN_Client_Management.AccountConnect(name=name)


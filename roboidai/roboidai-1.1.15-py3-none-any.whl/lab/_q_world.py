# Part of the ROBOID project - http://hamster.school
# Copyright (C) 2016 Kwang-Hyun Park (akaii@kw.ac.kr)
# 
# This library is free software; you can redistribute it and/or
# modify it under the terms of the GNU Lesser General Public
# License as published by the Free Software Foundation; either
# version 2.1 of the License, or (at your option) any later version.
# 
# This library is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY; without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE.  See the GNU
# Lesser General Public License for more details.
# 
# You should have received a copy of the GNU Lesser General
# Public License along with this library; if not, write to the
# Free Software Foundation, Inc., 59 Temple Place, Suite 330,
# Boston, MA  02111-1307  USA

import base64, codecs
magic = 'IyBQYXJ0IG9mIHRoZSBST0JPSUQgcHJvamVjdCAtIGh0dHA6Ly9oYW1zdGVyLnNjaG9vbA0KIyBDb3B5cmlnaHQgKEMpIDIwMTYgS3dhbmctSHl1biBQYXJrIChha2FpaUBrdy5hYy5rcikNCiMgDQojIFRoaXMgbGlicmFyeSBpcyBmcmVlIHNvZnR3YXJlOyB5b3UgY2FuIHJlZGlzdHJpYnV0ZSBpdCBhbmQvb3INCiMgbW9kaWZ5IGl0IHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgR05VIExlc3NlciBHZW5lcmFsIFB1YmxpYw0KIyBMaWNlbnNlIGFzIHB1Ymxpc2hlZCBieSB0aGUgRnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uOyBlaXRoZXINCiMgdmVyc2lvbiAyLjEgb2YgdGhlIExpY2Vuc2UsIG9yIChhdCB5b3VyIG9wdGlvbikgYW55IGxhdGVyIHZlcnNpb24uDQojIA0KIyBUaGlzIGxpYnJhcnkgaXMgZGlzdHJpYnV0ZWQgaW4gdGhlIGhvcGUgdGhhdCBpdCB3aWxsIGJlIHVzZWZ1bCwNCiMgYnV0IFdJVEhPVVQgQU5ZIFdBUlJBTlRZOyB3aXRob3V0IGV2ZW4gdGhlIGltcGxpZWQgd2FycmFudHkgb2YNCiMgTUVSQ0hBTlRBQklMSVRZIG9yIEZJVE5FU1MgRk9SIEEgUEFSVElDVUxBUiBQVVJQT1NFLiAgU2VlIHRoZSBHTlUNCiMgTGVzc2VyIEdlbmVyYWwgUHVibGljIExpY2Vuc2UgZm9yIG1vcmUgZGV0YWlscy4NCiMgDQojIFlvdSBzaG91bGQgaGF2ZSByZWNlaXZlZCBhIGNvcHkgb2YgdGhlIEdOVSBMZXNzZXIgR2VuZXJhbA0KIyBQdWJsaWMgTGljZW5zZSBhbG9uZyB3aXRoIHRoaXMgbGlicmFyeTsgaWYgbm90LCB3cml0ZSB0byB0aGUNCiMgRnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uLCBJbmMuLCA1OSBUZW1wbGUgUGxhY2UsIFN1aXRlIDMzMCwNCiMgQm9zdG9uLCBNQSAgMDIxMTEtMTMwNyAgVVNBDQoNCmZyb20gcm9ib2lkIGltcG9ydCAqDQpmcm9tIHJvYm9pZGFpIGltcG9ydCBLZXlFdmVudA0KaW1wb3J0IHJhbmRvbQ0KDQoNCmNsYXNzIFFXb3JsZDoNCiAgICBfTEVGVCA9ICdsZWZ0Jw0KICAgIF9SSUdIVCA9ICdyaWdodCcNCiAgICBfVVAgPSAndXAnDQogICAgX0RPV04gPSAnZG93bicNCiAgICBfQUNUSU9OUyA9IChfTEVGVCwgX1JJR0hULCBfVVAsIF9ET1dOKQ0KDQogICAgZGVmIF9faW5pdF9fKHNlbGYsIGdyaWRfcm9ib3QpOg0KICAgICAgICBzZWxmLl9yb2JvdCA9IGdyaWRfcm9ib3QNCiAgICAgICAgc2VsZi5fcSA9IFsgWyBOb25lLCBOb25lLCBOb25lLCBOb25lIF0sDQogICAgICAgICAgICAgICAgICAgWyBOb25lLCBOb25lLCBOb25lLCBOb25lIF0sDQogICAgICAgICAgICAgICAgICAgWyBOb25lLCBOb25lLCBOb25lLCBOb25lIF0sDQogICAgICAgICAgICAgICAgICAgWyBOb25lLCBOb25lLCBOb25lLCBOb25lIF0gXQ0KICAgICAgICBmb3IgeSBpbiByYW5nZSg0KToNCiAgICAgICAgICAgIGZvciB4IG'
love = 'yhVUWuozqyXQDcBt0XVPNtVPNtVPNtVPNtVPNtVUAyoTLhK3SorI1orS0tCFO7W2kyMaDaBvNjYPNapzyanUDaBvNjYPNaqKNaBvNjYPNaMT93ovp6VQO9QDbtVPNtVPNtVRgyrHI2MJ50YaA0LKW0XPxAPt0XVPNtVTEyMvO3LJy0K3AjLJAyK2gyrFumMJkzXGbAPvNtVPNtVPNtq2ucoTHtIUW1MGbAPvNtVPNtVPNtVPNtVTgyrFN9VRgyrHI2MJ50YzqyqS9lMJkyLKAyMS9eMKxbXD0XVPNtVPNtVPNtVPNtnJLtn2I5VQ09VRgyrHI2MJ50YyADDHASVT9lVTgyrFN9CFOYMKySqzIhqP5SH0Z6QDbtVPNtVPNtVPNtVPNtVPNtpzI0qKWhVTgyrD0XVPNtVPNtVPNtVPNtMJkcMvOeMKxtCG0tW3VaBt0XVPNtVPNtVPNtVPNtVPNtVUAyoTLhK3WiLz90YaWyp2I0XPxAPvNtVPNtVPNtVPNtVUqunKDbZwNcQDbAPvNtVPOxMJLtq2ScqS9eMKxbp2IfMvx6QDbtVPNtVPNtVUqbnJkyVSElqJH6QDbtVPNtVPNtVPNtVPOeMKxtCFOYMKySqzIhqP5aMKEspzIfMJSmMJEsn2I5XPxAPvNtVPNtVPNtVPNtVTyzVTgyrFN9CFOYMKySqzIhqP5GHRSQEFOipvOeMKxtCG0tF2I5EKMyoaDhEIAQVT9lVTgyrFN9CFNaolpto3Vtn2I5VQ09VPq4WmbAPvNtVPNtVPNtVPNtVPNtVPOlMKE1pz4tn2I5QDbtVPNtVPNtVPNtVPOyoTyzVTgyrFN9CFNapvp6QDbtVPNtVPNtVPNtVPNtVPNtp2IfMv5spz9vo3DhpzImMKDbXD0XVPNtVPNtVPNtVPNtq2ScqPtlZPxAPt0XVPNtVTEyMvOsnKAsqzSfnJEsLJA0nJ9hXUAyoTLfVUtfVUxfVTSwqTyiovx6QDbtVPNtVPNtVTyzVTSwqTyiovN9CFOEI29loTDhK0kSEyD6VUWyqUIlovO4VQ4tZN0XVPNtVPNtVPOyoTyzVTSwqTyiovN9CFOEI29loTDhK1WWE0uHBvOlMKE1pz4trPN8VQZAPvNtVPNtVPNtMJkcMvOuL3Eco24tCG0tHIqipzkxYy9IHQbtpzI0qKWhVUxtCPNmQDbtVPNtVPNtVTIfp2H6VUWyqUIlovO5VQ4tZN0XQDbtVPNtMTIzVS9cp19ipUOip2y0MI9uL3Eco24bp2IfMvjtLJA0nJ9hXGbAPvNtVPNtVPNtMTylMJA0nJ9hVQ0tp2IfMv5spz9vo3DhM2I0K2EcpzIwqTyiovtcQDbtVPNtVPNtVTyzVTSwqTyiovN9CFOEI29loTDhK0kSEyD6VUWyqUIlovOxnKWyL3Eco24tCG0tHIqipzkxYy9FFHqVIN0XVPNtVPNtVPOyoTyzVTSwqTyiovN9CFOEI29loTDhK1WWE0uHBvOlMKE1pz4tMTylMJA0nJ9hVQ09VSSKo3WfMP5sGRITIN0XVPNtVPNtVPOyoTyzVTSwqTyiovN9CFOEI29loTDhK1IDBvOlMKE1pz4tMTylMJA0nJ9hVQ09VSSKo3WfMP5sER9KGt0XVPNtVPNtVPOyoUAyBvOlMKE1pz4tMTylMJA0nJ9hVQ09VSSKo3WfMP5sIINAPt0XVPNtVTEyMvOaMKEsoJS4K3SsLJA0nJ9hXUAyoTLfVUtfVUxcBt0XVPNtVPNtVPOkK3MuoUIyplN9VSgqQDbtVPNtVPNtVUMuoTyxK2SwqTyioaZtCFOoKD0XVPNtVPNtVPOz'
god = 'b3IgYSBpbiBRV29ybGQuX0FDVElPTlM6DQogICAgICAgICAgICBpZiBzZWxmLl9pc192YWxpZF9hY3Rpb24oeCwgeSwgYSkgYW5kIHNlbGYuX2lzX29wcG9zaXRlX2FjdGlvbihhKSA9PSBGYWxzZToNCiAgICAgICAgICAgICAgICBxX3ZhbHVlcy5hcHBlbmQoc2VsZi5fcVt5XVt4XVthXSkNCiAgICAgICAgICAgICAgICB2YWxpZF9hY3Rpb25zLmFwcGVuZChhKQ0KICAgICAgICBxX21heCA9IG1heChxX3ZhbHVlcykNCiAgICAgICAgY2FuZGlkYXRlcyA9IFtdDQogICAgICAgIGZvciBhIGluIHZhbGlkX2FjdGlvbnM6DQogICAgICAgICAgICBpZiBzZWxmLl9xW3ldW3hdW2FdID09IHFfbWF4Og0KICAgICAgICAgICAgICAgIGNhbmRpZGF0ZXMuYXBwZW5kKGEpDQogICAgICAgIHJldHVybiByYW5kb20uY2hvaWNlKGNhbmRpZGF0ZXMpDQoNCiAgICBkZWYgZ2V0X21heF9xKHNlbGYsIHgsIHkpOg0KICAgICAgICBxX3ZhbHVlcyA9IFtdDQogICAgICAgIGZvciBhIGluIFFXb3JsZC5fQUNUSU9OUzoNCiAgICAgICAgICAgIGlmIHNlbGYuX2lzX3ZhbGlkX2FjdGlvbih4LCB5LCBhKToNCiAgICAgICAgICAgICAgICBxX3ZhbHVlcy5hcHBlbmQoc2VsZi5fcVt5XVt4XVthXSkNCiAgICAgICAgcmV0dXJuIG1heChxX3ZhbHVlcykNCg0KICAgIGRlZiBnZXRfbmV4dF9tYXhfcShzZWxmLCB4LCB5LCBhY3Rpb24pOg0KICAgICAgICBpZiBzZWxmLl9pc192YWxpZF9hY3Rpb24oeCwgeSwgYWN0aW9uKToNCiAgICAgICAgICAgIGlmIGFjdGlvbiA9PSBRV29ybGQuX0xFRlQ6DQogICAgICAgICAgICAgICAgcmV0dXJuIHNlbGYuZ2V0X21heF9xKHgtMSwgeSkNCiAgICAgICAgICAgIGVsaWYgYWN0aW9uID09IFFXb3JsZC5fUklHSFQ6DQogICAgICAgICAgICAgICAgcmV0dXJuIHNlbGYuZ2V0X21heF9xKHgrMSwgeSkNCiAgICAgICAgICAgIGVsaWYgYWN0aW9uID09IFFXb3JsZC5fVVA6DQogICAgICAgICAgICAgICAgcmV0dXJuIHNlbGYuZ2V0X21heF9xKHgsIHkrMSkNCiAgICAgICAgICAgIGVsc2U6DQogICAgICAgICAgICAgICAgcmV0dXJuIHNlbGYuZ2V0X21heF9xKHgsIHktMSkNCiAgICAgICAgcmV0dXJuIDANCg0KICAgIGRlZiBzZXRfcShzZWxmLCB4LCB5LCBhY3Rpb24sIHZhbHVlKToNCiAgICAgICAgc2VsZi5fcVt5XVt4XVthY3Rpb25dID0gdmFsdWUNCg0KDQpjbGFzcyBRR2FtZToNCiAgICBkZWYgX19pbml0X18oc2VsZik6DQogICAgICAgIGRpc3Bvc2VfYWxsKCkNCg0KICAgIGRlZiBzdGFydChzZWxmLCBncmlkX3JvYm90KToNCiAgICAgICAgd29ybGQgPSBRV29ybGQoZ3JpZF9yb2JvdCkNCiAgICAgICAgaWYgd29ybGQud2FpdF9zcGFjZV9rZXkoKSA9PSBLZXlFdmVudC5FU0M6DQogICAgICAgICAgICBncmlkX3JvYm'
destiny = '90YzEcp3Oip2HbXD0XVPNtVPNtVPNtVPNtpzI0qKWhQDbtVPNtVPNtVN0XVPNtVPNtVPO0o3EuoS9wo3IhqUZtCFOoKD0XVPNtVPNtVPOgo3MyK2AiqJ50VQ0tZN0XVPNtVPNtVPNAPvNtVPNtVPNtq2ucoTHtIUW1MGbAPvNtVPNtVPNtVPNtVUttCFOapzyxK3WiLz90YzqyqS94XPxAPvNtVPNtVPNtVPNtVUxtCFOapzyxK3WiLz90YzqyqS95XPxAPvNtVPNtVPNtVPNtVTSwqTyiovN9VUqipzkxYzqyqS9gLKuspI9uL3Eco24brPjtrFxAPvNtVPNtVPNtVPNtVT5yrUEsoJS4K3RtCFO3o3WfMP5aMKEsozI4qS9gLKuspFu4YPO5YPOuL3Eco24cQDbtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVUOlnJ50XTSwqTyiovxAPvNtVPNtVPNtVPNtVTqlnJEspz9vo3DhoJ92MFuuL3Eco24cQDbtVPNtVPNtVPNtVPOgo3MyK2AiqJ50VPf9VQRAPvNtVPNtVPNtVPNtVTgyrFN9VUqipzkxYaqunKEsn2I5XPxAPvNtVPNtVPNtVPNtVTyzVTgyrFN9CFOYMKySqzIhqP5SH0Z6VTWlMJSeQDbtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVUWyq2SlMPN9VQNAPvNtVPNtVPNtVPNtVTyzVTgyrFN9CFNaolp6VUWyq2SlMPN9VQRAPvNtVPNtVPNtVPNtVTIfnJLtn2I5VQ09VPq4WmbtpzI3LKWxVQ0tYGRAPvNtVPNtVPNtVPNtVN0XVPNtVPNtVPNtVPNtq29loTDhp2I0K3RbrPjtrFjtLJA0nJ9hYPOlMKqupzDtXlNjYwxtXvOhMKu0K21urS9kXD0XVPNtVPNtVPNtVPNtnJLtn2I5VQ09VPqiWlOipvOeMKxtCG0tW3taBt0XVPNtVPNtVPNtVPNtVPNtVTyzVTgyrFN9CFNaolp6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVUEiqTSfK2AiqJ50pl5upUOyozDboJ92MI9wo3IhqPxAPvNtVPNtVPNtVPNtVPNtVPNtVPNtoJ92MI9wo3IhqPN9VQNAPvNtVPNtVPNtVPNtVPNtVPNtVPNtpUWcoaDbqT90LJksL291oaEmXD0XVPNtVPNtVPNtVPNtVPNtVPNtVPOapzyxK3WiLz90YzI4pUWyp3AsM29iMPtcQDbtVPNtVPNtVPNtVPNtVPNtMJkmMGbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtM3WcMS9lo2WiqP5yrUOlMKAmK2WuMPtcQDbtVPNtVPNtVPNtVPNtVPNtM3WcMS9lo2WiqP5lMKAyqPtcQDbtVPNtVPNtVPNtVPNtVPNtnJLtq29loTDhq2ScqS9mpTSwMI9eMKxbXFN9CFOYMKySqzIhqP5SH0Z6VTWlMJSeQDbtVPNtVPNtVPNtVPNAPvNtVPNtVPNtVPNtVUqunKDbZwNcQDbtVPNtVPNtVN0XVPNtVPNtVPOapzyxK3WiLz90YzEcp3Oip2HbXD0XQDbAPzEyMvOjoTS5K3SsM2SgMI9bLJ1mqTIlXPx6QDbtVPNtHHquoJHbXF5mqTSlqPuUpzyxFTSgp3Eypvu5K2S4nKAsqKN9IUW1MFxcQDbAPt0XMTIzVUOfLKyspI9aLJ1yK2uuoKA0MKWspluwpz9mpm1HpaIyXGbAPvNtVPOEE2SgMFtcYaA0LKW0XRqlnJEVLJ1mqTIlHlu5K2S4nKAsqKN9IUW1MFjtL3Wip3Z9L3Wip3ZcXD0X'
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))
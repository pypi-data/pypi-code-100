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
magic = 'IyBQYXJ0IG9mIHRoZSBST0JPSUQgcHJvamVjdCAtIGh0dHA6Ly9oYW1zdGVyLnNjaG9vbA0KIyBDb3B5cmlnaHQgKEMpIDIwMTYgS3dhbmctSHl1biBQYXJrIChha2FpaUBrdy5hYy5rcikNCiMgDQojIFRoaXMgbGlicmFyeSBpcyBmcmVlIHNvZnR3YXJlOyB5b3UgY2FuIHJlZGlzdHJpYnV0ZSBpdCBhbmQvb3INCiMgbW9kaWZ5IGl0IHVuZGVyIHRoZSB0ZXJtcyBvZiB0aGUgR05VIExlc3NlciBHZW5lcmFsIFB1YmxpYw0KIyBMaWNlbnNlIGFzIHB1Ymxpc2hlZCBieSB0aGUgRnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uOyBlaXRoZXINCiMgdmVyc2lvbiAyLjEgb2YgdGhlIExpY2Vuc2UsIG9yIChhdCB5b3VyIG9wdGlvbikgYW55IGxhdGVyIHZlcnNpb24uDQojIA0KIyBUaGlzIGxpYnJhcnkgaXMgZGlzdHJpYnV0ZWQgaW4gdGhlIGhvcGUgdGhhdCBpdCB3aWxsIGJlIHVzZWZ1bCwNCiMgYnV0IFdJVEhPVVQgQU5ZIFdBUlJBTlRZOyB3aXRob3V0IGV2ZW4gdGhlIGltcGxpZWQgd2FycmFudHkgb2YNCiMgTUVSQ0hBTlRBQklMSVRZIG9yIEZJVE5FU1MgRk9SIEEgUEFSVElDVUxBUiBQVVJQT1NFLiAgU2VlIHRoZSBHTlUNCiMgTGVzc2VyIEdlbmVyYWwgUHVibGljIExpY2Vuc2UgZm9yIG1vcmUgZGV0YWlscy4NCiMgDQojIFlvdSBzaG91bGQgaGF2ZSByZWNlaXZlZCBhIGNvcHkgb2YgdGhlIEdOVSBMZXNzZXIgR2VuZXJhbA0KIyBQdWJsaWMgTGljZW5zZSBhbG9uZyB3aXRoIHRoaXMgbGlicmFyeTsgaWYgbm90LCB3cml0ZSB0byB0aGUNCiMgRnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uLCBJbmMuLCA1OSBUZW1wbGUgUGxhY2UsIFN1aXRlIDMzMCwNCiMgQm9zdG9uLCBNQSAgMDIxMTEtMTMwNyAgVVNBDQoNCmltcG9ydCBudW1weSBhcyBucA0KaW1wb3J0IGN2Mg0KDQpucC5zZXRfcHJpbnRvcHRpb25zKHN1cHByZXNzPVRydWUpDQoNCg0KY2xhc3MgVG1JbWFnZToNCiAgICBkZWYgX19pbml0X18oc2VsZiwgc3F1YXJlPSdjZW50ZXInKToNCiAgICAgICAgc2VsZi5fbG9hZGVkID0gRmFsc2UNCiAgICAgICAgc2VsZi5fbW9kZWwgPSBOb25lDQogICAgICAgIHNlbGYuX2RhdGEgPSBucC5uZGFycmF5KHNoYXBlPSgxLCAyMjQsIDIyNCwgMyksIGR0eXBlPW5wLmZsb2F0MzIpDQogICAgICAgIHNlbGYuc2V0X3NxdWFyZShzcXVhcmUpDQogICAgICAgIHNlbGYuX2NsZWFyKCkNCg0KICAgIGRlZiBfY2xlYXIoc2VsZik6DQogI'
love = 'PNtVPNtVUAyoTLhK2Wyp3EsoTSvMJjtCFNaWj0XVPNtVPNtVPOmMJkzYy9vMKA0K2AiozMcMTIhL2HtCFNjQDbtVPNtVPNtVUAyoTLhK2kuLzIfplN9VSgqQDbtVPNtVPNtVUAyoTLhK2AiozMcMTIhL2ImVQ0tJ10APt0XVPNtVTEyMvOfo2SxK21iMTIfXUAyoTLfVTMioTEypvx6QDbtVPNtVPNtVTygpT9lqPOipj0XVPNtVPNtVPOcoKOipaDtqTIhp29lMzkiqlOuplO0Mt0XVPNtVPNtVPOmMJkzYy9fo2SxMJDtCFOTLJkmMD0XVPNtVPNtVPO0pax6QDbtVPNtVPNtVPNtVPOgo2EyoS9jLKEbVQ0to3ZhpTS0nP5do2yhXTMioTEypvjtW2gypzSmK21iMTIfYzt1WlxAPvNtVPNtVPNtVPNtVTkuLzIfK3OuqTttCFOipl5jLKEbYzcinJ4bMz9fMTIlYPNaoTSvMJkmYaE4qPpcQDbtVPNtVPNtVPNtVPOmMJkzYy9go2EyoPN9VUEzYzgypzSmYz1iMTIfpl5fo2SxK21iMTIfXT1iMTIfK3OuqTtcQDbtVPNtVPNtVPNtVPOfLJWyoUZtCFOhpP5aMJ5zpz9gqUu0XTkuLzIfK3OuqTtfVTIhL29xnJ5aCFq1qTL4WljtMUE5pTH9Gz9hMFxAPvNtVPNtVPNtVPNtVUAyoTLhK2kuLzIfplN9VT5jYzSlpzS5XSgfLJWyoPOzo3VtKljtoTSvMJjtnJ4toTSvMJkmKFxAPvNtVPNtVPNtVPNtVUAyoTLhK2kiLJEyMPN9VSElqJHAPvNtVPNtVPNtVPNtVUWyqUIlovOHpaIyQDbtVPNtVPNtVTI4L2IjqQbAPvNtVPNtVPNtVPNtVUWyqUIlovOTLJkmMD0XQDbtVPNtMTIzVS9wpz9jK2ygLJqyXUAyoTLfVTygLJqyXGbAPvNtVPNtVPNtq2yxqTttCFOcoJSaMF5mnTSjMIfkKD0XVPNtVPNtVPObMJyanUDtCFOcoJSaMF5mnTSjMIfjKD0XVPNtVPNtVPOcMvObMJyanUDtCvO3nJE0nQbAPvNtVPNtVPNtVPNtVTyzVUAyoTLhK3AkqJSlMFN9CFNaoTIzqPp6QDbtVPNtVPNtVPNtVPNtVPNtp3EupaDtCFNjQDbtVPNtVPNtVPNtVPOyoTyzVUAyoTLhK3AkqJSlMFN9CFNapzyanUDaBt0XVPNtVPNtVPNtVPNtVPNtVUA0LKW0VQ0tnTIcM2u0VP0tq2yxqTtAPvNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtp3EupaDtCFNbnTIcM2u0VP0tq2yxqTtcVP8iVQVAPvNtVPNtVPNtVPNtVTygLJqyVQ0tnJ1uM2Iop3EupaD6p3EupaDeq2yxqTtfVQcqQDbtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPOcMvOmMJkzYy9mpKIupzHtCG0tW2kyMaDaBt0XVPNtVPNtVPNtVPNtVPNtVUA0LKW0VQ0tZN0XVPNtVPNtVPNtVPNtMJkcMvOmMJkzYy9mpKIupzHtCG'
god = '0gJ3JpZ2h0JzoNCiAgICAgICAgICAgICAgICBzdGFydCA9IHdpZHRoIC0gaGVpZ2h0DQogICAgICAgICAgICBlbHNlOg0KICAgICAgICAgICAgICAgIHN0YXJ0ID0gKHdpZHRoIC0gaGVpZ2h0KSAvLyAyDQogICAgICAgICAgICBpbWFnZSA9IGltYWdlWzosIHN0YXJ0OnN0YXJ0K2hlaWdodF0NCiAgICAgICAgcmV0dXJuIGN2Mi5yZXNpemUoaW1hZ2UsIGRzaXplPSgyMjQsIDIyNCkpDQoNCiAgICBkZWYgcHJlZGljdChzZWxmLCBpbWFnZSwgdGhyZXNob2xkPTAuNSk6DQogICAgICAgIGlmIGltYWdlIGlzIE5vbmU6DQogICAgICAgICAgICBzZWxmLl9jbGVhcigpDQogICAgICAgIGVsaWYgc2VsZi5fbG9hZGVkOg0KICAgICAgICAgICAgcmVzaXplZF9pbWFnZSA9IHNlbGYuX2Nyb3BfaW1hZ2UoaW1hZ2UpDQogICAgICAgICAgICBzZWxmLl9kYXRhWzBdID0gKHJlc2l6ZWRfaW1hZ2UuYXN0eXBlKG5wLmZsb2F0MzIpIC8gMTI3LjApIC0gMQ0KICAgICAgICAgICAgY29uZmlkZW5jZXMgPSBzZWxmLl9jb25maWRlbmNlcyA9IHNlbGYuX21vZGVsLnByZWRpY3Qoc2VsZi5fZGF0YSlbMF0NCiAgICAgICAgICAgIGlmIGNvbmZpZGVuY2VzLnNpemUgPiAwOg0KICAgICAgICAgICAgICAgIGluZGV4ID0gY29uZmlkZW5jZXMuYXJnbWF4KCkNCiAgICAgICAgICAgICAgICBpZiBjb25maWRlbmNlc1tpbmRleF0gPCB0aHJlc2hvbGQ6DQogICAgICAgICAgICAgICAgICAgIHNlbGYuX2Jlc3RfbGFiZWwgPSAnJw0KICAgICAgICAgICAgICAgICAgICBzZWxmLl9iZXN0X2NvbmZpZGVuY2UgPSAwDQogICAgICAgICAgICAgICAgZWxzZToNCiAgICAgICAgICAgICAgICAgICAgc2VsZi5fYmVzdF9sYWJlbCA9IHNlbGYuX2xhYmVsc1tpbmRleF0NCiAgICAgICAgICAgICAgICAgICAgc2VsZi5fYmVzdF9jb25maWRlbmNlID0gY29uZmlkZW5jZXNbaW5kZXhdDQogICAgICAgICAgICAgICAgICAgIHJldHVybiBUcnVlDQogICAgICAgIHJldHVybiBGYWxzZQ0KDQogICAgZGVmIHNldF9zcXVhcmUoc2VsZiwgc3F1YXJlKToNCiAgICAgICAgaWYgc3F1YXJlIGlzIE5vbmU6DQogICAgICAgICAgICBzZWxmLl9zcXVhcmUgPSAnY2VudGVyJw0KICAgICAgICBlbGlmIGlzaW5zdGFuY2Uoc3F1YXJlLCBzdHIpOg0KICAgICAgICAgICAgc2VsZi5fc3F1YXJlID0gc3F1YXJlLmxvd2VyKCkNCg0KICAgIGRlZiBkcmF3X3NxdWFyZShzZWxmLCBpbWF'
destiny = 'aMFjtL29fo3V9XQNfZwH1YQNcYPO0nTywn25yp3Z9ZvjtL2kiozH9EzSfp2HcBt0XVPNtVPNtVPOcMvOcoJSaMFOcplOho3DtGz9hMGbAPvNtVPNtVPNtVPNtVTyzVTAfo25yBt0XVPNtVPNtVPNtVPNtVPNtVTygLJqyVQ0tnJ1uM2HhL29jrFtcQDbtVPNtVPNtVPNtVPO3nJE0nPN9VTygLJqyYaAbLKOyJmSqQDbtVPNtVPNtVPNtVPObMJyanUDtCFOcoJSaMF5mnTSjMIfjKD0XVPNtVPNtVPNtVPNtnJLtnTIcM2u0VQ4tq2yxqTt6QDbtVPNtVPNtVPNtVPNtVPNtnJLtp2IfMv5sp3S1LKWyVQ09VPqfMJM0WmbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtp3EupaDtCFNjQDbtVPNtVPNtVPNtVPNtVPNtMJkcMvOmMJkzYy9mpKIupzHtCG0tW3WcM2u0WmbAPvNtVPNtVPNtVPNtVPNtVPNtVPNtp3EupaDtCFObMJyanUDtYFO3nJE0nN0XVPNtVPNtVPNtVPNtVPNtVTIfp2H6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVUA0LKW0VQ0tXTuynJqbqPNgVUqcMUEbXFNiYlNlQDbtVPNtVPNtVPNtVPNtVPNtL3LlYaWyL3EuozqfMFucoJSaMFjtXQNfVUA0LKW0XFjtXUqcMUEbYPOmqTSlqPg3nJE0nPxfVTAioT9lYPO0nTywn25yp3ZcQDbtVPNtVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtVPNtVTyzVUAyoTLhK3AkqJSlMFN9CFNaoTIzqPp6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVUA0LKW0VQ0tZN0XVPNtVPNtVPNtVPNtVPNtVTIfnJLtp2IfMv5sp3S1LKWyVQ09VPqlnJqbqPp6QDbtVPNtVPNtVPNtVPNtVPNtVPNtVUA0LKW0VQ0tq2yxqTttYFObMJyanUDAPvNtVPNtVPNtVPNtVPNtVPOyoUAyBt0XVPNtVPNtVPNtVPNtVPNtVPNtVPOmqTSlqPN9VPu3nJE0nPNgVTuynJqbqPxtYl8tZt0XVPNtVPNtVPNtVPNtVPNtVTA2Zv5lMJA0LJ5aoTHbnJ1uM2HfVPumqTSlqPjtZPxfVPumqTSlqPgbMJyanUDfVTuynJqbqPxfVTAioT9lYPO0nTywn25yp3ZcQDbtVPNtVPNtVUWyqUIlovOcoJSaMD0XQDbtVPNtMTIzVTqyqS9fLJWyoPumMJkzXGbAPvNtVPNtVPNtpzI0qKWhVUAyoTLhK2Wyp3EsoTSvMJjAPt0XVPNtVTEyMvOaMKEsL29hMvumMJkzXGbAPvNtVPNtVPNtpzI0qKWhVUAyoTLhK2Wyp3EsL29hMzyxMJ5wMD0XQDbtVPNtMTIzVTqyqS9uoTksoTSvMJkmXUAyoTLcBt0XVPNtVPNtVPOlMKE1pz4tp2IfMv5soTSvMJkmQDbAPvNtVPOxMJLtM2I0K2SfoS9wo25zplumMJkzXGbAPvNtVPNtVPNtpzI0qKWhVUAyoTLhK2AiozMcMTIhL2ImQDb='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))
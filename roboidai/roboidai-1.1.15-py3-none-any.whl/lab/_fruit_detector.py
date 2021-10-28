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
magic = 'IyBQYXJ0IG9mIHRoZSBST0JPSUQgcHJvamVjdCAtIGh0dHA6Ly9oYW1zdGVyLnNjaG9vbAojIENvcHlyaWdodCAoQykgMjAxNiBLd2FuZy1IeXVuIFBhcmsgKGFrYWlpQGt3LmFjLmtyKQojIAojIFRoaXMgbGlicmFyeSBpcyBmcmVlIHNvZnR3YXJlOyB5b3UgY2FuIHJlZGlzdHJpYnV0ZSBpdCBhbmQvb3IKIyBtb2RpZnkgaXQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBHTlUgTGVzc2VyIEdlbmVyYWwgUHVibGljCiMgTGljZW5zZSBhcyBwdWJsaXNoZWQgYnkgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbjsgZWl0aGVyCiMgdmVyc2lvbiAyLjEgb2YgdGhlIExpY2Vuc2UsIG9yIChhdCB5b3VyIG9wdGlvbikgYW55IGxhdGVyIHZlcnNpb24uCiMgCiMgVGhpcyBsaWJyYXJ5IGlzIGRpc3RyaWJ1dGVkIGluIHRoZSBob3BlIH'
love = 'EbLKDtnKDtq2yfoPOvMFO1p2IzqJjfPvZtLaI0VSqWIRuCIIDtDH5MVSqOHyWOGyEMBlO3nKEbo3I0VTI2MJ4tqTuyVTygpTkcMJDtq2SlpzShqUxto2LXVlOAEIWQFRSBIRSPFHkWISxto3VtExyHGxIGHlOTG1VtDFODDIWHFHAIGRSFVSOIHyOCH0HhVPOGMJHtqTuyVRqBIDbwVRkyp3AypvOUMJ5ypzSfVSO1LzkcLlOZnJAyoaAyVTMipvOgo3WyVTEyqTScoUZhPvZtPvZtJJ91VUAbo3IfMPObLKMyVUWyL2IcqzIxVTRtL29jrFOiMvO0nTHtE05IVRkyp3AypvOUMJ5ypzSfPvZtHUIvoTywVRkcL2Ihp2HtLJkiozptq2y0nPO0nTymVTkcLaWupax7VTyzVT5iqPjtq3WcqTHtqT8tqTuyPvZtEaWyMFOGo2M0q2SlMFOTo3IhMTS0nJ9hYPOWozZhYPN1BFOHMJ1joTHtHTkuL2HfVSA1nKEyVQZmZPjXVlOPo3A0o24fVR1OVPNjZwRk'
god = 'MS0xMzA3ICBVU0EKCmZyb20gcm9ib2lkYWkuX2ltYWdlLl9vYmplY3RfZGV0ZWN0b3IgaW1wb3J0IE9iamVjdERldGVjdG9yCgpfb2JqX2RldGVjdG9yID0gTm9uZQoKCmRlZiB3YWl0X3VudGlsX2ZydWl0KGNhbSwgZnJ1aXRzLCBpbnRlcnZhbF9tc2VjPTEsIGxhbmc9J2VuJyk6CiAgICBnbG9iYWwgX29ial9kZXRlY3RvcgogICAgCiAgICBpZiBfb2JqX2RldGVjdG9yIGlzIE5vbmU6CiAgICAgICAgX29ial9kZXRlY3RvciA9IE9iamVjdERldGVjdG9yKFRydWUsIGxhbmcpCiAgICAgICAgX29ial9kZXRlY3Rvci5kb3dubG9hZF9tb2RlbCgpCiAgICAgICAgX29ial9kZXRlY3Rvci5sb2FkX21vZGVsKCkKICAgIGlmIG5vdCBpc2luc3RhbmNlKGZydWl0cywgKGxpc3QsIHR1cGxlKSk6CiAgICAgICAgZnJ1aXRzID0gKGZydW'
destiny = 'y0pljcPvNtVPNXVPNtVT9vnvN9VR5iozHXVPNtVUqbnJkyVT9vnvOcplOBo25yBtbtVPNtVPNtVTygLJqyVQ0tL2SgYaWyLJDbXDbtVPNtVPNtVTyzVS9iLzcsMTI0MJA0o3VhMTI0MJA0XTygLJqyXGbXVPNtVPNtVPNtVPNtnJ1uM2HtCFOso2WdK2EyqTIwqT9lYzElLKqspzImqJk0XTygLJqyXDbtVPNtVPNtVPNtVPOzo3VtrPOcovOzpaIcqUZ6PvNtVPNtVPNtVPNtVPNtVPOcMvO4VTyhVS9iLzcsMTI0MJA0o3VhM2I0K2kuLzIfXPx6PvNtVPNtVPNtVPNtVPNtVPNtVPNto2WdVQ0trNbtVPNtVPNtVPNtVPNtVPNtVPNtVTWlMJSePvNtVPNtVPNtL2SgYaAbo3pbnJ1uM2HcPvNtVPNtVPNtnJLtL2SgYzAbMJAeK2gyrFucoaEypaMuoS9gp2IwXFN9CFNaMKAwWmbtLaWyLJfXVPNtVTAuoF5bnJEyXPxXVPNtVUWyqUIlovOiLzbX'
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))
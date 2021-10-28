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
magic = 'IyBQYXJ0IG9mIHRoZSBST0JPSUQgcHJvamVjdCAtIGh0dHA6Ly9oYW1zdGVyLnNjaG9vbAojIENvcHlyaWdodCAoQykgMjAxNiBLd2FuZy1IeXVuIFBhcmsgKGFrYWlpQGt3LmFjLmtyKQojIAojIFRoaXMgbGlicmFyeSBpcyBmcmVlIHNvZnR3YXJlOyB5b3UgY2FuIHJlZGlzdHJpYnV0ZSBpdCBhbmQvb3IKIyBtb2RpZnkgaXQgdW5kZXIgdGhlIHRlcm1zIG9mIHRoZSBHTlUgTGVzc2VyIEdlbmVyYWwgUHVibGljCiMgTGljZW5zZSBhcyBwdWJsaXNoZWQgYnkgdGhlIEZyZWUgU29mdHdhcmUgRm91bmRhdGlvbjsgZWl0aGVyCiMgdmVyc2lvbiAyLjEgb2YgdGhlIExpY2Vuc2UsIG9yIChhdCB5b3VyIG9wdGlvbikgYW55IGxhdGVyIHZlcnNpb24uCiMgCiMgVGhpcyBsaWJyYXJ5IGlzIGRpc3RyaWJ1dGVkIGluIHRoZSBob3BlIHRoYXQgaXQgd2lsbCBiZSB1c2VmdWwsCiMgYnV0IFdJVEhPVVQgQU5ZIFdBUlJBTlRZOyB3aXRob3V0IGV2ZW4gdGhlIGltcGxpZWQgd2FycmFudHkgb2YKIyBNRVJDSEFOVEFCSUxJVFkgb3IgRklUTkVTUyBGT1IgQSBQQVJUSUNVTEFSIFBVUlBPU0UuICBTZWUgdGhlIEdOVQojIExlc3NlciBHZW5lcmFsIFB1YmxpYyBMaWNlbnNlIGZvciBtb3JlIGRldGFpbHMuCiMgCiMgWW91IHNob3VsZCBoYXZlIHJlY2VpdmVkIGEgY29weSBvZiB0aGUgR05VIExlc3NlciBHZW5lcmFsCiMgUHVibGljIExpY2Vuc2UgYWxvbmcgd2l0aCB0aGlzIGxpYnJhcnk7IGlmIG5vdCwgd3JpdGUgdG8gdGhlCiMgRnJlZSBTb2Z0d2FyZSBGb3VuZGF0aW9uLCBJbmMuLCA1OSBUZW1wbGUgUGxhY2UsIFN1aXRlIDMzMCwKIyBCb3N0b24sIE1BICAwMjExMS0xMzA3ICBVU0EKCmltcG9ydCBjdjIKaW1wb3J0IG51bXB5IGFzIG5wCmltcG9ydCBtZWRpYXBpcGUgYXMgbXAKZnJvbSAuX3V0aWwgaW1wb3J0IFV0aWwKCgpjbGFzcyBGYWNlRGV0ZWN0b3I6CiAgICBkZWYgX19pbml0X18oc2VsZiwgdGhyZXNob2xkPTAuNSk6CiAgICAgICAgc2VsZi5fY2xlYXIoKQogICAgICAgIHRyeToKICAgICAgICAgICAgc2VsZi5fbW9kZWwgPSBtcC5zb2x1dGlvbnMuZmFjZV9kZXRlY3Rpb24uRmFjZURldGVjdGlvbihtaW5fZGV0ZWN0aW9uX2NvbmZpZGVuY2U9dGhyZXNob2xkKQogICAgICAgIGV4Y2VwdDoKICAgICAgICAgICAgc2VsZi5fbW9kZWwgPSBOb25lCgogICAgZGVmIF9jbGVhcihzZWxmKToKICAgICAgICBzZWxmLl9wb2ludHMgPSB7CiAgICAgICAgICAgICdsZWZ0IGV5ZSc6IE5vbmUsCiAgICAgICAgICAgICdyaWdodCBleWUnOiBOb25lLAogICAgICAgICAgICAnbGVmdCBlYXInOiBOb25lLAogICAgICAgICAgICAncmlnaHQgZWFyJzogTm9uZSwKICAgICAgICAgICAgJ25vc2UnOiBOb25lLAogICAgICAgICAgICAnbW91dGgnOiBOb25lCiAgICAgICAgfQogICAgICAgIHNlbGYuX2JveCA9IE5vbmUKICAgICAgICBzZWxmLl93aWR0aCA9IDAKICAgICAgICBzZWxmLl9oZWlnaHQgPSAwCiAgICAgICAgc2VsZi5fYXJlYSA9IDAKICAgICAgI'
love = 'POmMJkzYy9wo25znJEyozAyVQ0tZNbtVPNtVPNtVUAyoTLhK2ElLKqcozqmVQ0tGz9hMDbXVPNtVTEyMvOxMKEyL3Dbp2IfMvjtnJ1uM2HfVUOuMTEcozp9ZPx6PvNtVPNtVPNtnJLtnJ1uM2HtnKZtoz90VR5iozHtLJ5xVUAyoTLhK21iMTIfVTymVT5iqPOBo25yBtbtVPNtVPNtVPNtVPOcoJSaMFN9VTA2Zv5wqaEQo2kipvucoJSaMFjtL3LlYxACGR9FK0WUHwWFE0VcPvNtVPNtVPNtVPNtVTygLJqyYzMfLJqmYaqlnKEyLJWfMFN9VRMuoUAyPvNtVPNtVPNtVPNtVUWyp3IfqUZtCFOmMJkzYy9go2EyoP5jpz9wMKAmXTygLJqyXDbtVPNtVPNtVPNtVPOcMvOlMKA1oUEmVTShMPOlMKA1oUEmYzEyqTIwqTyioaZtLJ5xVTkyovulMKA1oUEmYzEyqTIwqTyioaZcVQ4tZQbXVPNtVPNtVPNtVPNtVPNtVTEyqTIwqTyiovN9VUWyp3IfqUZhMTI0MJA0nJ9hp1fjKDbtVPNtVPNtVPNtVPNtVPNtoT9wLKEco24tCFOxMKEyL3Eco24hoT9wLKEco25sMTS0LDbtVPNtVPNtVPNtVPNtVPNtnJLtoT9wLKEco246PvNtVPNtVPNtVPNtVPNtVPNtVPNtLz91ozEcozqsLz94VQ0toT9wLKEco24hpzIfLKEcqzIsLz91ozEcozqsLz94PvNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtLz91ozEcozqsLz94BtbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOcoKqcMUEbVQ0tnJ1uM2Hhp2uupTIoZI0XVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJ1bMJyanUDtCFOcoJSaMF5mnTSjMIfjKDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOvo3ttCFOmMJkzYy9vo3tXVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtnJLtLz94VTymVR5iozH6VTWirPN9VT5jYacypz9mXQDcPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTWirSfjKFN9VT1urPtjYPOvo3IhMTyhM19vo3thrT1covNdVTygq2yxqTttYFOjLJExnJ5aXDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOvo3uoZI0tCFOgLKtbZPjtLz91ozEcozqsLz94YaygnJ4tXvOcoJuynJqbqPNgVUOuMTEcozpcPvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVTWirSflKFN9VT1covtbLz91ozEcozqsLz94YaugnJ4tXlOvo3IhMTyhM19vo3thq2yxqTtcVPbtnJ13nJE0nPNeVUOuMTEcozpfVTygq2yxqTttYFNkXDbtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPOvo3uoZ10tCFOgnJ4bXTWiqJ5xnJ5aK2WirP55oJyhVPftLz91ozEcozqsLz94YzuynJqbqPxtXvOcoJuynJqbqPNeVUOuMTEcozpfVTygnTIcM2u0VP0tZFxXVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtLz94VQ0tLz94YzSmqUyjMFuhpP5coaDmZvxXVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtp2IfMv5sLz94VQ0tLz94PvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUAyoTLhK3qcMUEbVQ0tLJWmXTWirSflKFNgVTWirSfjKFxXVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtp2IfMv5snTIcM2u0VQ0tLJWmXTWirSfmKFNgVTWirSfkKFxXVPNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtp2IfMv5sLKWyLFN9VUAyoTLhK3qcMUEbVPbtp2IfMv5snTIcM2u0PvNtVPNtVPNtVPNtVPNtVPNtVPNtVPNtVUttCF'
god = 'Bba2V5cG9pbnQueCBmb3Iga2V5cG9pbnQgaW4gbG9jYXRpb24ucmVsYXRpdmVfa2V5cG9pbnRzXQogICAgICAgICAgICAgICAgICAgICAgICB5ID0gW2tleXBvaW50LnkgZm9yIGtleXBvaW50IGluIGxvY2F0aW9uLnJlbGF0aXZlX2tleXBvaW50c10KICAgICAgICAgICAgICAgICAgICAgICAgYXJyID0gbnAudHJhbnNwb3NlKG5wLnN0YWNrKCh4LHkpKSkgKiAoaW13aWR0aCwgaW1oZWlnaHQpCiAgICAgICAgICAgICAgICAgICAgICAgIGFyciA9IGFyci5hc3R5cGUobnAuaW50MzIpCiAgICAgICAgICAgICAgICAgICAgICAgIHBvaW50cyA9IHNlbGYuX3BvaW50cwogICAgICAgICAgICAgICAgICAgICAgICBwb2ludHNbJ2xlZnQgZXllJ10gPSBhcnJbMF0KICAgICAgICAgICAgICAgICAgICAgICAgcG9pbnRzWydyaWdodCBleWUnXSA9IGFyclsxXQogICAgICAgICAgICAgICAgICAgICAgICBwb2ludHNbJ2xlZnQgZWFyJ10gPSBhcnJbNF0KICAgICAgICAgICAgICAgICAgICAgICAgcG9pbnRzWydyaWdodCBlYXInXSA9IGFycls1XQogICAgICAgICAgICAgICAgICAgICAgICBwb2ludHNbJ25vc2UnXSA9IGFyclsyXQogICAgICAgICAgICAgICAgICAgICAgICBwb2ludHNbJ21vdXRoJ10gPSBhcnJbM10KICAgICAgICAgICAgICAgICAgICAgICAgc2VsZi5fY29uZmlkZW5jZSA9IGRldGVjdGlvbi5zY29yZVswXQogICAgICAgICAgICAgICAgICAgICAgICBzZWxmLl9kcmF3aW5ncyA9IG5wLmNvbmNhdGVuYXRlKChib3gsIGFyci5yZXNoYXBlKC0xKSksIGF4aXM9Tm9uZSkKICAgICAgICAgICAgICAgICAgICAgICAgcmV0dXJuIFRydWUKICAgICAgICBzZWxmLl9jbGVhcigpCiAgICAgICAgcmV0dXJuIEZhbHNlCgogICAgZGVmIF9kcmF3KHNlbGYsIGltYWdlLCBwdCwgY29sb3IsIHRoaWNrbmVzcyk6CiAgICAgICAgY3YyLnJlY3RhbmdsZShpbWFnZSwgKHB0WzBdLCBwdFsxXSksIChwdFsyXSwgcHRbM10pLCBjb2xvciwgdGhpY2tuZXNzKQogICAgICAgIGN2Mi5jaXJjbGUoaW1hZ2UsIChwdFs0XSwgcHRbNV0pLCB0aGlja25lc3MsIGNvbG9yLCAtMSkgIyBsZWZ0IGV5ZQogICAgICAgIGN2Mi5jaXJjbGUoaW1hZ2UsIChwdFs2XSwgcHRbN10pLCB0aGlja25lc3MsIGNvbG9yLCAtMSkgIyByaWdodCBleWUKICAgICAgICBjdjIuY2lyY2xlKGltYWdlLCAocHRbOF0sIHB0WzldKSwgdGhpY2tuZXNzLCBjb2xvciwgLTEpICMgbm9zZQogICAgICAgIGN2Mi5jaXJjbGUoaW1hZ2UsIChwdFsxMF0sIHB0WzExXSksIHRoaWNrbmVzcywgY29sb3IsIC0xKSAjIG1vdXRoCiAgICAgICAgY3YyLmNpcmNsZShpbWFnZSwgKHB0WzEyXSwgcHRbMTNdKSwgdGhpY2tuZXNzLCBjb2xvciwgLTEpICMgbGVmdCBlYXIKICAgICAgICBjdjIuY2lyY2xlKGltYWdlLCAocHRbMTRdLCBwdFsxNV0pLCB0aGlja25lc3MsIGNvbG9yLCAtMSkgIyByaWdodCBlYXIKCiAgICBkZWYgZHJhd19yZXN1bHQoc2VsZiwgaW1hZ2UsIGNvbG9yPSgwLDI1NSwwKSwgdGhpY2t'
destiny = 'hMKAmCGVfVTAfo25yCHMuoUAyXGbXVPNtVPNtVPOcMvOcoJSaMFOcplOho3DtGz9hMGbXVPNtVPNtVPNtVPNtnJLtL2kiozH6PvNtVPNtVPNtVPNtVPNtVPOcoJSaMFN9VTygLJqyYzAipUxbXDbtVPNtVPNtVPNtVPOcMvOmMJkzYy9xpzS3nJ5aplOcplOho3DtGz9hMGbXVPNtVPNtVPNtVPNtVPNtVUAyoTLhK2ElLKpbnJ1uM2HfVUAyoTLhK2ElLKqcozqmYPOwo2kipvjtqTucL2ghMKAmXDbtVPNtVPNtVUWyqUIlovOcoJSaMDbXVPNtVTEyMvOaMKEsrUxbp2IfMvjtnJD9W2SfoPpcBtbtVPNtVPNtVTyzVTymnJ5mqTShL2HbnJDfVUA0pvx6PvNtVPNtVPNtVPNtVTyxVQ0tnJDhoT93MKVbXDbtVPNtVPNtVPNtVPOcMvOcMPN9CFNaLJkfWmbXVPNtVPNtVPNtVPNtVPNtVUWyqUIlovOmMJkzYy9jo2yhqUZXVPNtVPNtVPNtVPNtMJkcMvOcMPOcovOmMJkzYy9jo2yhqUZ6PvNtVPNtVPNtVPNtVPNtVPOlMKE1pz4tp2IfMv5spT9coaEmJ2yxKDbtVPNtVPNtVUWyqUIlovOBo25yPtbtVPNtMTIzVTqyqS9vo3tbp2IfMvx6PvNtVPNtVPNtpzI0qKWhVUAyoTLhK2WirNbXVPNtVTEyMvOaMKEsq2yxqTtbp2IfMvx6PvNtVPNtVPNtpzI0qKWhVUAyoTLhK3qcMUEbPtbtVPNtMTIzVTqyqS9bMJyanUDbp2IfMvx6PvNtVPNtVPNtpzI0qKWhVUAyoTLhK2uynJqbqNbXVPNtVTEyMvOaMKEsLKWyLFumMJkzXGbXVPNtVPNtVPOlMKE1pz4tp2IfMv5sLKWyLDbXVPNtVTEyMvOaMKEsL29hMvumMJkzXGbXVPNtVPNtVPOlMKE1pz4tp2IfMv5sL29hMzyxMJ5wMDbXVPNtVTEyMvOaMKEso3WcMJ50LKEco24bp2IfMvjtMTIapzIyCHMuoUAyXGbXVPNtVPNtVPOfMJM0K2I5MFN9VUAyoTLhM2I0K3u5XPqfMJM0VTI5MFpcPvNtVPNtVPNtpzyanUEsMKyyVQ0tp2IfMv5aMKEsrUxbW3WcM2u0VTI5MFpcPvNtVPNtVPNtnJLtMTIapzIyBtbtVPNtVPNtVPNtVPOlMKE1pz4tIKEcoP5xMJqlMJHboTIzqS9yrJHfVUWcM2u0K2I5MFxXVPNtVPNtVPOyoUAyBtbtVPNtVPNtVPNtVPOlMKE1pz4tIKEcoP5lLJEcLJ4boTIzqS9yrJHfVUWcM2u0K2I5MFxXPvNtVPOxMJLtL3WipPumMJkzYPOcoJSaMFjtL2kiozH9EzSfp2HcBtbtVPNtVPNtVTyzVTygLJqyVTymVR5iozHto3Vtp2IfMv5sLz94VTymVR5iozH6VUWyqUIlovOBo25yPvNtVPNtVPNtnJLtL2kiozH6VTygLJqyVQ0tnJ1uM2HhL29jrFtcPvNtVPNtVPNtLz94VQ0tp2IfMv5sLz94PvNtVPNtVPNtpzI0qKWhVTygLJqyJ2WirSfkKGcvo3uoZ10fVTWirSfjKGcvo3uoZy1qPtbtVPNtDUA0LKEcL21yqTuiMNbtVPNtMTIzVTEcp3EuozAyXUO0ZFjtpUDlXGbXVPNtVPNtVPOlMKE1pz4tIKEcoP5xnKA0LJ5wMFujqQRfVUO0ZvxXPvNtVPONp3EuqTywoJI0nT9xPvNtVPOxMJLtMTIapzIyXUO0ZFjtpUDlXGbXVPNtVPNtVPOlMKE1pz4tIKEcoP5xMJqlMJHbpUDkYPOjqQVcPtbtVPNtDUA0LKEcL21yqTuiMNbtVPNtMTIzVUWuMTyuovujqQRfVUO0Zvx6PvNtVPNtVPNtpzI0qKWhVSI0nJjhpzSxnJShXUO0ZFjtpUDlXDb='
joy = '\x72\x6f\x74\x31\x33'
trust = eval('\x6d\x61\x67\x69\x63') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x6c\x6f\x76\x65\x2c\x20\x6a\x6f\x79\x29') + eval('\x67\x6f\x64') + eval('\x63\x6f\x64\x65\x63\x73\x2e\x64\x65\x63\x6f\x64\x65\x28\x64\x65\x73\x74\x69\x6e\x79\x2c\x20\x6a\x6f\x79\x29')
eval(compile(base64.b64decode(eval('\x74\x72\x75\x73\x74')),'<string>','exec'))
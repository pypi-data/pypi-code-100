from omnitools import ApacheHeadersDict, Obj, dumpobj
import json


test = {
    "content-type": "text/html",
    "accesS controL alloW origiN": "*",
    "CACHE_CONTROL": "max-age=0, must-revalidate",
    "HTTP_ACCEPT": "*",
}
headers = ApacheHeadersDict(test)
print("headers.items()", headers.items())
print("headers[\"acCEpt\"]", headers["acCEpt"])
print("headers[\"http_acCEpt\"]", headers["http_acCEpt"])
del headers["accepT"]
print("headers", headers)
print("test", test)


zz = Obj({
    "a": (
        0,
        [
            1,
            Obj({
                "b": Obj({
                    "c": True,
                    "d": b"3" * 100
                })
            })
        ],
        (
            2,
            Obj({
                "e": False
            }),
        )
    )
})
print(zz, zz.a[1][1].b.c, zz.a[2][1].e)
print(json.dumps(zz, default=repr))
# print(json.dumps(zz))


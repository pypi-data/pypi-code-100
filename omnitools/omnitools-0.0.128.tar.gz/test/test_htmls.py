from omnitools import encodeURI, encodeURIComponent, decodeURI, decodeURIComponent


domain = "https://my.d/"
path = "哇/asd"
e_os = encodeURI(domain+path)
e_ec = domain+encodeURIComponent(path)
print(e_os)
print(e_ec)
print(decodeURIComponent(e_os))
print(decodeURIComponent(e_ec))
print(decodeURI(e_os))
print(decodeURI(e_ec))
os = encodeURIComponent(domain+path)
print(os)
print(decodeURIComponent(os))
print(decodeURI(os))
os = encodeURI(path)
ec = encodeURIComponent(path)
print(os)
print(ec)
print(decodeURIComponent(os))
print(decodeURIComponent(ec))
print(decodeURI(os))
print(decodeURI(ec))

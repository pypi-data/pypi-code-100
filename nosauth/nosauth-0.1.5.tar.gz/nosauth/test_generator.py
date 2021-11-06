import hashlib

account = "3dcaf8dc-dbd5-4865-8810-047b98bf0675"
installation_id = "c6d454ba-945f-4d1a-88da-054adf7b5912"

account = "fb50ca7a-6ba2-11eb-9439-0242ac130002"
installation_id = "a777c5e7-c9ac-407b-99b4-1a5934137f43"

cert = open("cert.pem", mode="rb").read()
version = "C2.1.22.784"


def getFirstNumber(uuid):
    for char in uuid:
        if char.isdigit():
            return char
    return None
    
def generateSecondTypeUserAgent(cer, installation_id, version):
    firstLetter = getFirstNumber(installation_id)
    
    if firstLetter == None or int(firstLetter) % 2 == 0:
        hashOfCert = hashlib.sha256(cert).hexdigest()
        hashOfVersion = hashlib.sha1(version.encode("ascii")).hexdigest()
        hashOfInstallationId = hashlib.sha256(installation_id.encode("ascii")).hexdigest()
        hashOfSum = hashlib.sha256((hashOfCert + hashOfVersion + hashOfInstallationId).encode("ascii")).hexdigest()
        return hashOfSum[:8]
        
    else:
        hashOfCert = hashlib.sha1(cert).hexdigest()
        hashOfVersion = hashlib.sha256(version.encode("ascii")).hexdigest()
        hashOfInstallationId = hashlib.sha1(installation_id.encode("ascii")).hexdigest()
        hashOfSum = hashlib.sha256((hashOfCert + hashOfVersion + hashOfInstallationId).encode("ascii")).hexdigest()
        return hashOfSum[-8:]
        
def generateThirdTypeUserAgent(cer, installation_id, version, account_id):
    firstLetter = getFirstNumber(installation_id)
    firstTwoLettersOfAccountId = account_id[:2]
    
    if firstLetter == None or int(firstLetter) % 2 == 0:
        hashOfCert = hashlib.sha256(cert).hexdigest()
        hashOfVersion = hashlib.sha1(version.encode("ascii")).hexdigest()
        hashOfInstallationId = hashlib.sha256(installation_id.encode("ascii")).hexdigest()
        hashOfAccountId = hashlib.sha1(account_id.encode("ascii")).hexdigest()
        hashOfSum = hashlib.sha256((hashOfCert + hashOfVersion + hashOfInstallationId + hashOfAccountId).encode("ascii")).hexdigest()
        return firstTwoLettersOfAccountId + hashOfSum[:8]
        
    else:
        hashOfCert = hashlib.sha1(cert).hexdigest()
        hashOfVersion = hashlib.sha256(version.encode("ascii")).hexdigest()
        hashOfInstallationId = hashlib.sha1(installation_id.encode("ascii")).hexdigest()
        hashOfAccountId = hashlib.sha256(account_id.encode("ascii")).hexdigest()
        hashOfSum = hashlib.sha256((hashOfCert + hashOfVersion + hashOfInstallationId + hashOfAccountId).encode("ascii")).hexdigest()
        return firstTwoLettersOfAccountId + hashOfSum[-8:]
        
print(generateSecondTypeUserAgent(cert, installation_id, version))

print(generateThirdTypeUserAgent(cert, installation_id, version, account))

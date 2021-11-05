def getNamespace():
    with open("/var/run/secrets/kubernetes.io/serviceaccount/namespace") as f:
        lines = f.readlines()
        return lines[0]

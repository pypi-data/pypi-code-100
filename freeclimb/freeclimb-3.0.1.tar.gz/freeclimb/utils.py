from urllib.parse import parse_qsl
import time, hmac, hashlib

class Utils:
    @staticmethod
    def verify_request(requestBody, signatureHeader, signingSecret, tolerance=5*60*1000):
        """Verify a request's signature.
   
        :param requestBody: The request's body after the json is stringified without trailing white space after keys or values.
        :type: str
        :param signatureHeader: The request's `freeclimb-signature` header.
        :type: str
        :param signingSecret: A signing secret from the FreeClimb account.
        :type: str
        :param tolerance: Acceptable duration threshold represented in milliseconds,  defaulting to 5 minutes
        :type: int
        """
        splitSignatureHeader = signatureHeader.split(",")
        signatureHeaderObj = {}
        for querystring in splitSignatureHeader:
            result = dict(parse_qsl(querystring))
            key = list(result.keys())[0]
            if key in signatureHeaderObj:
                old_value = signatureHeaderObj.get(key)
                result[key] = [old_value, result.get(key)]
            signatureHeaderObj.update(result)

        # timestamp (t) on the `FreeClimb-Signature` header is represented by a unix timestamp (in seconds)
        currentTime = time.time()
        signatureAge = (float(currentTime) - float(signatureHeaderObj['t'])) * 1000
        if tolerance < signatureAge:
            raise Exception("Request rejected - signature's timestamp failed against current tolerance of {} milliseconds. Signature age: {} milliseconds".format(tolerance, signatureAge))

        data = signatureHeaderObj['t'] + '.' + requestBody
        computed_sha = hmac.new(bytes(signingSecret, 'utf-8'), data.encode('utf-8'), digestmod=hashlib.sha256).hexdigest()
        print(computed_sha)
        print(signatureHeaderObj['v1'])
        if computed_sha not in signatureHeaderObj['v1']:
            raise Exception("Unverified Request Signature - FreeClimb was unable to verify that this request originated from FreeClimb. If this request was unexpected, it may be from a bad actor. Please proceed with caution. If this request was expected, to fix this issue try checking for any typos or misspelling of your signing secret.")
        return None

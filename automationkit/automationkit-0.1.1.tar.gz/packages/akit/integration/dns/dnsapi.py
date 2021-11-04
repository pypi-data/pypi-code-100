
from akit.integration.dns.dnsconst import DnsRecordClass, DnsRecordType

from akit.integration.dns.dnsquestion import DnsQuestion

def dnsquery(name: str, rtype: DnsRecordType, rclass: DnsRecordClass):

    question = DnsQuestion(name, rtype, rclass)

    query_str = question.as_dns_string()

    return
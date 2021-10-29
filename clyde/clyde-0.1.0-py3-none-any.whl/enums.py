import enumb

class Method(enumb.AutoName):
    PUT:     str
    GET:     str
    POST:    str
    HEAD:    str
    PATCH:   str
    DELETE:  str
    OPTIONS: str

class Header(enumb.AutoNameSlugTitle):
    USER_AGENT:      str
    REFERER:         str
    CONTENT_TYPE:    str
    ACCEPT_LANGUAGE: str
    AUTHORIZATION:   str

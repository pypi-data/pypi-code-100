import casbin
from casbin import persist
import firebase_admin
from firebase_admin import credentials
from firebase_admin import firestore


class CasbinRule(object):
    '''
    CasbinRule model
    '''

    def __init__(self, ptype=None, v0=None, v1=None, v2=None, v3=None, v4=None, v5=None):
        self.ptype = ptype
        self.v0 = v0
        self.v1 = v1
        self.v2 = v2
        self.v3 = v3
        self.v4 = v4
        self.v5 = v5

    @staticmethod
    def from_dict(source):
        return CasbinRule(source['ptype'], source['v0'], source['v1'], source['v2'], source['v3'], source['v4'], source['v5'])

    def to_dict(self):
        return {
            'ptype': self.ptype or None,
            'v0': self.v0 or None,
            'v1': self.v1 or None,
            'v2': self.v2 or None,
            'v3': self.v3 or None,
            'v4': self.v4 or None,
            'v5': self.v5 or None
        }

    def __str__(self):
        arr = [self.ptype]
        for v in (self.v0, self.v1, self.v2, self.v3, self.v4, self.v5):
            if v is None:
                break
            arr.append(v)
        return ", ".join(arr)

    def __repr__(self):
        return '{} {} {} {} {} {} {}'.format(self.ptype, self.v0, self.v1, self.v2, self.v3, self.v4, self.v5)


class Filter:
    ptype = []
    v0 = []
    v1 = []
    v2 = []
    v3 = []
    v4 = []
    v5 = []


class Adapter(persist.Adapter, persist.adapters.UpdateAdapter):
    """the interface for Casbin adapters."""

    def __init__(self, firebaseCredPath=None, filtered=False):
        '''
        Initialize the adapter
        '''
        if(firebaseCredPath is not None):
            cred = credentials.Certificate(firebaseCredPath)
        else:
            cred = credentials.ApplicationDefault()

        firebase_admin.initialize_app(cred)
        self._collection = 'casbin'
        self._document = 'rules'

        self.db = firestore.client()
        self.rulesRef = self.db.collection(
            self._collection).document(self._document)

        self._filtered = filtered

    def load_policy(self, model):
        '''
        implementing add Interface for casbin \n
        load all policy rules from firebase firestore \n
        '''

        # get the rules from the collection document
        rulesFromDB = self.rulesRef.get().to_dict()
        if rulesFromDB is None:
            rules = []
        else:
            rules = rulesFromDB["rules"]

        for rule in rules:
            casbinRule = CasbinRule.from_dict(rule)
            persist.load_policy_line(str(casbinRule), model)

    def _save_policy_line(self, ptype, rule):
        casbinRule = CasbinRule(ptype, *rule)
        self.rulesRef.update(
            {"rules": firestore.ArrayUnion([casbinRule.to_dict()])})

    def save_policy(self, model):
        '''
        implementing add Interface for casbin \n
        save the policy in firestore \n
        '''
        for sec in ["p", "g"]:
            if sec not in model.model.keys():
                continue
            for ptype, ast in model.model[sec].items():
                for rule in ast.policy:
                    self._save_policy_line(ptype, rule)

    def add_policy(self, sec, ptype, rule):
        """add policy rules to firebase"""
        self._save_policy_line(ptype, rule)

    def add_policies(self, sec, ptype, rules):
        """adds a policy rules to the storage."""
        for rule in rules:
            self._save_policy_line(ptype, rule)

    def remove_policies(self, sec, ptype, rules):
        """delete policy rules from firebase"""
        ruleList = []
        for rule in rules:
            casbinRule = CasbinRule(ptype, *rule)
            ruleList.append(casbinRule.to_dict())
            self.rulesRef.update(
                {"rules": firestore.ArrayRemove(ruleList)})

    def remove_policy(self, sec, ptype, rule):
        """delete policy rules from firebase"""
        casbinRule = CasbinRule(ptype, *rule)
        self.rulesRef.update(
            {"rules": firestore.ArrayRemove([casbinRule.to_dict()])})

    def remove_filtered_policy(self, sec, ptype, field_index, *field_values):
        """
        delete policy rules for matching filters from firebase
        """
        pass

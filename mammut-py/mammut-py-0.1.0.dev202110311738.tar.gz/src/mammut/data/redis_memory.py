# coding=utf-8
import redis

class ThoughtTuple:
    def __init__(self, user_id:int, id: int, need: str, offers: [], tokenized_need=None, tokenized_offers=None, need_target_vector=None, offers_target_vector=None):
        self.user_id = user_id
        self.id = id
        self.need = need
        self.offers = offers
        self.tokenized_need = tokenized_need
        self.tokenized_offers = tokenized_offers
        self.need_target_vector = need_target_vector
        self.offers_target_vector = offers_target_vector

    def print(self):
        print(f'\t-> ThoughtTuple: {self.id}')
        print(f'\t\tOffers:')
        for o in self.offers:
            print(f'\t\t\t{o}')
        print(f'\t\tNeed:\n\t\t\t{self.need}')


class RedisMemory:
    def __init__(self, host: str, port:int):
        self.host = host
        self.port = port
        self.r = redis.StrictRedis(host=self.host, port=self.port, db=0)

    def set_key (self, key: str, value: str, pipe=None):
        if pipe is None:
            return self.r.set(key, value)
        else:
            return pipe.set(key, value)

    def set_hash (self, key: str, items: {}, pipe=None):
        if pipe is None:
            return self.r.hmset(key, items)
        else:
            return pipe.hmset(key, items)

    def save_tuple(self, tuple: ThoughtTuple, pipe=None):
        #save hash

        tupleid = "tuple:" + str(tuple.user_id) + ":" + str(tuple.id)

        #To-Do: Switch NEED/OFFER keys
        tuple_data = {}
        tuple_data["OFFER"] = tuple.offers[0]
        tuple_data["NEED"] = tuple.need

        self.set_hash (tupleid, tuple_data, pipe)

        #save extended corpus

        for offer in tuple.offers:
            offer_message =  str(tuple.user_id) + ":" + offer
            self.set_key(offer_message, tuple.id, pipe)

    def save_thought_tuple_list(self, data):# data -> ThoughtTuple array
        #instance pipeline
        pipe = self.r.pipeline()
        for i in data:
            self.save_tuple(i, pipe)
        pipe_result = pipe.execute()

    def save_variables(self, variables):#variables ->dict
        pipe = self.r.pipeline()
        for variable in variables:
            self.set_key(variable, variables[variable], pipe)
        pipe.execute()

    def save_data(self, data, command):
        cases = {'set': self.save_variables,
                 'thoughts-hmset': self.save_thought_tuple_list #TODO: no es hmset estrictamente hablando
                 }
        try:
            cases[command](data)
        except Exception as ex:
            print(ex)

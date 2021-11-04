from littlenn.optimizers.rmsprop import RMSProp

class RMSPropFactory:
    def create_instance(self, params):
        learning_rate = params['lr']
        try:
            beta = params['beta']
        except KeyError:
            beta = .9
        return RMSProp(learning_rate, beta)


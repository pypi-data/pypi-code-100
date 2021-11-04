from littlenn.optimizers.adam import Adam

class AdamFactory:
    def create_instance(self, params):
        learning_rate = params['lr']
        try:
            exponential_weight = params['ew']
        except KeyError:
            exponential_weight = 0.9
        try:
            beta = params['beta']
        except KeyError:
            beta = .999
        return Adam(learning_rate, exponential_weight, beta)
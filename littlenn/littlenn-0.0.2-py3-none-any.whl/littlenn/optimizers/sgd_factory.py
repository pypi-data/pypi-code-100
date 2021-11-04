from littlenn.optimizers.sgd import SGD

class SGDFactory:
    def create_instance(self, params):
        learning_rate = params['lr']
        try:
            exponential_weight = params['ew']
        except KeyError:
            exponential_weight = None
        return SGD(learning_rate, exponential_weight)


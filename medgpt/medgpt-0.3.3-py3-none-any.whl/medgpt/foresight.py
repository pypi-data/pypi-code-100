import torch.nn as nn

class Foresight(object):
    def __init__(self, tokenizer, device, model):
        self.tokenizer = tokenizer
        self.device = device
        self.model = model

    def mcq(self, question, options, do_print=False):
        self.model.eval()
        option2p = {}
        q_data = self.tokenizer(question, return_tensors=True, device=self.model.device)
        logits = self.model.forward(**q_data)['logits']
        smax = nn.Softmax(dim=0)

        ps = smax(logits[0, -1, :]).detach().cpu().numpy()

        for option in options:
            tkn_id = self.tokenizer.tkn2id[option]
            option2p[option] = {'original': ps[tkn_id],
                                'cnt': self.tokenizer.global_token_cnt[option]}

        p_sum = sum([v['original'] for v in option2p.values()])

        for option in options:
            tkn_id = self.tokenizer.tkn2id[option]
            option2p[option]['norm'] = ps[tkn_id] / p_sum

        if do_print:
            for tkn in question:
                print("{:5}: {:20} - {}".format(
                    self.tokenizer.global_token_cnt.get(tkn, 0),
                    self.tokenizer.tkn2name[tkn],
                    tkn))
            print()
            for option in options:
                option_name = self.tokenizer.tkn2name[option]
                print("{:5}: {:50} - {:20}- {:.2f} - {:.2f}".format(
                                                       option2p[option]['cnt'],
                                                       option_name[:50],
                                                       option,
                                                       option2p[option]['original'],
                                                       option2p[option]['norm']))


        return option2p

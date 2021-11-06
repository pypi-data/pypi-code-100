import torch
import torch.nn as nn
from cogdl.layers import FSGCNLayer

from .. import BaseModel


class FSGCN(BaseModel):

    @staticmethod
    def add_args(parser):
        """Add model-specific arguments to the parser."""
        # fmt: off
        parser.add_argument("--num-features", type=int)
        parser.add_argument("--num-classes", type=int)
        parser.add_argument("--num-layers", type=int, default=2)
        parser.add_argument("--hidden-size", type=int, default=64)
        parser.add_argument("--dropout", type=float, default=0.5)
        parser.add_argument("--residual", action="store_true")
        parser.add_argument("--norm", type=str, default=None)
        parser.add_argument("--activation", type=str, default="relu")
        parser.add_argument("--sample-size", type=int, default=2)
        # fmt: on

    @classmethod
    def build_model_from_args(cls, args):
        return cls(
            args.num_features,
            args.hidden_size,
            args.num_classes,
            args.num_layers,
            args.dropout,
            args.activation,
            args.residual,
            args.norm,
            args.actnn,
            args.rp_ratio,
            args.sample_size,
        )

    def __init__(
        self,
        in_feats,
        hidden_size,
        out_feats,
        num_layers,
        dropout,
        activation="relu",
        residual=False,
        norm=None,
        actnn=False,
        rp_ratio=1,
        sample_size=2,
    ):
        super(FSGCN, self).__init__()
        self.hist = []
        self.first_epoch = True
        self.sample_size = sample_size
        self.hidden_size = hidden_size
        self.out_feats = out_feats
        shapes = [in_feats] + [hidden_size] * (num_layers - 1) + [out_feats]
        Layer = FSGCNLayer
        self.layers = nn.ModuleList(
            [
                Layer(
                    shapes[i],
                    shapes[i + 1],
                    dropout=dropout if i != num_layers - 1 else 0,
                    residual=residual if i != num_layers - 1 else None,
                    norm=norm if i != num_layers - 1 else None,
                    activation=activation if i != num_layers - 1 else None,
                    rp_ratio=rp_ratio,
                )
                for i in range(num_layers)
            ]
        )
        self.num_layers = num_layers

    def forward(self, graph):
        graph.sym_norm()
        h = graph.x
        if not self.training:
            for i in range(self.num_layers):
                h = self.layers[i](graph, h)
            return h
        if self.first_epoch:
            for i in range(self.num_layers):
                self.hist.append(h.clone().detach().cpu())
                h = self.layers[i](graph, h)
            self.first_epoch = False
        else:
            self.curr_hist = []
            idx = torch.randint(self.hidden_size, (self.sample_size,)).to(h.device)
            for i in range(self.num_layers):
                hx = self.hist[i]
                if i > 0:
                    hx[:, idx.cpu()] = h.clone().detach().cpu()
                self.curr_hist.append(hx)
                if i < self.num_layers - 1:
                    # cur_idx = torch.randint(self.hidden_size, (self.sample_size,)).to(h.device)
                    cur_idx = idx
                else:
                    cur_idx = torch.arange(self.out_feats).to(h.device)
                if i > 0:
                    h = self.layers[i](graph, h, self.hist[i], idx, cur_idx)
                else:
                    h = self.layers[i](graph, h, self.hist[i], None, cur_idx)
                # idx = cur_idx
            self.hist = self.curr_hist
        return h

    def predict(self, data):
        return self.forward(data)

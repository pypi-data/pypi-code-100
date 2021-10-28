from random import random

from lassonet.prox import prox
import torch

if __name__ == "__main__":

    k = 3
    cols = (
        ["lambda", "M", "beta_in"]
        + [f"theta_{i}_in" for i in range(k)]
        + ["beta_out"]
        + [f"theta_{i}_out" for i in range(k)]
    )
    print(*cols, sep=", ")
    for _ in range(1000):
        v = torch.randn(size=(1,))
        u = torch.randn(size=(k,))
        lambda_ = random()
        lambda_bar = random()
        M = random()
        beta, theta = prox(v, u, lambda_=lambda_, lambda_bar=0, M=M)
        print(
            lambda_, M, *v.numpy(), *u.numpy(), *beta.numpy(), *theta.numpy(), sep=", "
        )

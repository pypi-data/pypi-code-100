def _marginal_utility(self,c):

    # Compute gradient
    x = torch.tensor(c,requires_grad=True,dtype=torch.float)

    U = self.utility(x)
    U.backward()

    return x.grad.detach().numpy()

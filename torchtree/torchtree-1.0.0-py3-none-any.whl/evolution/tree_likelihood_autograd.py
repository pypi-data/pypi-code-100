import torch

# inside constructor of TreeLikelihood
# self.calculator = calculate_treelikelihood_discrete

# def _call(self):
# like = TreeLikelihoodAutogradFunction.apply
# return like(self, self.tree_model.branch_lengths(),
#             self.clock_model.rates,
#             self.subst_model._rates.parameters()[0].tensor,
#             self.subst_model._frequencies.parameters()[0].tensor,
#             self.site_model._shape.tensor if hasattr(self.site_model, '_shape') else None)


class TreeLikelihoodAutogradFunction(torch.autograd.Function):
    @staticmethod
    def centered_finite_difference(function, parameters, delta):
        g = []
        for i in range(parameters.shape[0]):
            ff = parameters.clone()
            ff[i] += delta
            p = function(ff)
            ff[i] -= 2.0 * delta
            m = function(ff)
            g.append(torch.unsqueeze((p - m) / (2.0 * delta), -1))
        return torch.cat(g)

    @staticmethod
    def evaluate(treelikelihood, subst_rates=None, frequencies=None):
        rates = treelikelihood.site_model.rates().reshape(1, -1)
        probs = treelikelihood.site_model.probabilities().reshape((-1, 1, 1))

        branch_lengths = treelikelihood.tree_model.branch_lengths()

        if treelikelihood.clock_model is None:
            bls = torch.unsqueeze(
                torch.cat(
                    (branch_lengths, torch.zeros(1, dtype=torch.float64))
                ).reshape(-1, 1)
                * rates,
                -1,
            )
        else:
            bls = torch.unsqueeze(
                treelikelihood.clock_model.rates.reshape(-1, 1)
                * branch_lengths.reshape(-1, 1)
                * rates,
                -1,
            )

        if frequencies is not None:
            treelikelihood.subst_model._frequencies.field.tensor = frequencies
            treelikelihood.subst_model._frequencies.field.fire_parameter_changed()

        if subst_rates is not None:
            treelikelihood.subst_model._rates.field.tensor = subst_rates
            treelikelihood.subst_model._rates.field.fire_parameter_changed()

        mats = treelikelihood.subst_model.p_t(bls)

        log_prob = treelikelihood.calculator(
            treelikelihood.site_pattern.partials,
            treelikelihood.site_pattern.weights,
            treelikelihood.tree_model.postorder,
            mats,
            treelikelihood.subst_model.frequencies,
            probs,
        )
        return log_prob

    @staticmethod
    def forward(
        ctx,
        treelikelihood,
        branch_lengths,
        clock=None,
        subst_rates=None,
        frequencies=None,
        weibull_shape=None,
    ):
        ctx.treelikelihood = treelikelihood

        if branch_lengths.grad_fn is not None:

            with torch.enable_grad():

                if weibull_shape is not None:
                    treelikelihood.site_model.shape = (
                        weibull_shape.detach().requires_grad_(True)
                    )
                    treelikelihood.site_model.shape.fire_model_changed()
                    ctx.shape = treelikelihood.site_model.shape

                rates = treelikelihood.site_model.rates().reshape(1, -1)
                probs = treelikelihood.site_model.probabilities().reshape((-1, 1, 1))

                used_branch_lengths = branch_lengths.detach().requires_grad_(True)
                if clock is None:
                    bls = torch.unsqueeze(
                        torch.cat(
                            (used_branch_lengths, torch.zeros(1, dtype=torch.float64))
                        ).reshape(-1, 1)
                        * rates,
                        -1,
                    )
                else:
                    used_clock = clock.detach().requires_grad_(True)
                    ctx.clock = used_clock
                    bls = torch.unsqueeze(
                        used_clock.reshape(-1, 1)
                        * used_branch_lengths.reshape(-1, 1)
                        * rates,
                        -1,
                    )
                ctx.branch_lengths = used_branch_lengths

                if frequencies is not None:
                    treelikelihood.subst_model._frequencies.field.tensor = (
                        frequencies.detach()
                    )
                    treelikelihood.subst_model._frequencies.field.fire_parameter_changed()
                    ctx.frequencies = (
                        treelikelihood.subst_model._frequencies.field.tensor
                    )

                if subst_rates is not None:
                    treelikelihood.subst_model._rates.field.tensor = (
                        subst_rates.detach()
                    )
                    treelikelihood.subst_model._rates.field.fire_parameter_changed()
                    ctx.subst_model_rates = (
                        treelikelihood.subst_model._rates.field.tensor
                    )

                mats = treelikelihood.subst_model.p_t(bls)

                log_prob = treelikelihood.calculator(
                    treelikelihood.site_pattern.partials,
                    treelikelihood.site_pattern.weights,
                    treelikelihood.tree_model.postorder,
                    mats,
                    treelikelihood.subst_model.frequencies,
                    probs,
                )

                # Now we restore the old "attached" tensors
                if frequencies is not None:
                    treelikelihood.subst_model._frequencies.field.tensor = frequencies
                    treelikelihood.subst_model._frequencies.field.fire_parameter_changed()

                if subst_rates is not None:
                    treelikelihood.subst_model._rates.field.tensor = subst_rates
                    treelikelihood.subst_model._rates.field.fire_parameter_changed()

                ctx.save_for_backward(log_prob)
                return log_prob.detach()
        else:
            return TreeLikelihoodAutogradFunction.evaluate(treelikelihood)

    @staticmethod
    def backward(ctx, grad_output):
        (log_prob,) = ctx.saved_tensors
        with torch.enable_grad():
            log_prob.backward(grad_output)

        if hasattr(ctx, 'shape'):
            weibull_grad = ctx.shape.grad
        else:
            weibull_grad = None

        branch_grad = ctx.branch_lengths.grad

        if hasattr(ctx, 'clock'):
            clock_grad = ctx.clock.grad
        else:
            clock_grad = None

        delta = 1.0e-7
        if hasattr(ctx, 'frequencies'):
            like = lambda x: TreeLikelihoodAutogradFunction.evaluate(
                ctx.treelikelihood, None, x
            )
            frequencies_grad = (
                TreeLikelihoodAutogradFunction.centered_finite_difference(
                    like, ctx.frequencies, delta
                )
                * grad_output
            )
            ctx.treelikelihood.subst_model._frequencies.field.tensor = ctx.frequencies
            ctx.treelikelihood.subst_model._frequencies.field.fire_parameter_changed()
        else:
            frequencies_grad = None

        if hasattr(ctx, 'subst_model_rates'):
            like = lambda x: TreeLikelihoodAutogradFunction.evaluate(
                ctx.treelikelihood, x, None
            )
            subst_rates_grad = (
                TreeLikelihoodAutogradFunction.centered_finite_difference(
                    like, ctx.subst_model_rates, delta
                )
                * grad_output
            )
            ctx.treelikelihood.subst_model._rates.field.tensor = ctx.subst_model_rates
            ctx.treelikelihood.subst_model._rates.field.fire_parameter_changed()
        else:
            subst_rates_grad = None

        return (
            None,
            branch_grad,
            clock_grad,
            subst_rates_grad,
            frequencies_grad,
            weibull_grad,
        )

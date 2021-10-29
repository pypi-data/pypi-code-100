import time
import torch

# Gradient descent with annealing step sizes
def graddescent(X, Y, sigma2_prior, C, 
                stepsize = .1, tol = 10**(-10), max_iterations = 10**5):
  C_half = torch.linalg.cholesky(C)
  C_inv = torch.cholesky_inverse(C_half)
  bceloss = torch.nn.BCEWithLogitsLoss(reduction="sum")

  b = torch.zeros(1)
  theta = torch.zeros(X.size(1))

  old_loss = bceloss(b + X @ theta, Y.double()) \
             + 1/(2.0 * sigma2_prior) * theta @ C_inv @ theta

  for t in range(1, max_iterations):
    grad_loss_b = torch.ones(X.size(0)) @ (torch.sigmoid(b + X @ theta) - Y)
    grad_loss_theta = X.T @ (torch.sigmoid(b + X @ theta) - Y) + 1/(sigma2_prior) * C_inv @ theta

    if torch.any(torch.isnan(grad_loss_b)) or torch.any(torch.isnan(grad_loss_theta)):
      raise Exception("NAN value in gradient descent.")
    else:
      b_new = b - stepsize * grad_loss_b
      theta_new = theta - stepsize * grad_loss_theta
      new_loss = bceloss(b_new + X @ theta_new, Y.double()) \
                 + 1/(2.0 * sigma2_prior) * theta_new @ C_inv @ theta_new
      
      # New loss worse than old loss? Reduce step size and try again.
      if (new_loss > old_loss):
        stepsize = stepsize * (.99)
      else:
        # Stopping criterion
        if (old_loss - new_loss) < tol:
          return b, theta

        # Update
        b = b_new
        theta = theta_new
        old_loss = new_loss

  raise Exception("Gradient descent failed to converge.")



# MHI sampler using 'centered' proposal for Bayesian logistic regression
def bayesian_logistic_regression(X, Y, sigma2_prior, C,
                                 n_iterations, h,
                                 stepsize_opt = .1, tol_opt = 10**(-10), max_iterations_opt = 10**5):
  accepts = torch.zeros(n_iterations)
  bceloss = torch.nn.BCEWithLogitsLoss(reduction="sum")
  C_half = torch.linalg.cholesky(C)
  C_inv = torch.cholesky_inverse(C_half)

  # Optimize target
  b_opt, theta_opt = graddescent(X, Y, sigma2_prior, C,
                                 stepsize_opt, tol_opt, max_iterations_opt)
  # Compute the previous theta using the opt
  f_target_theta = bceloss(b_opt + X @ theta_opt, Y.double()) \
                   + 1/(2.0 * sigma2_prior) * theta_opt @ C_inv @ theta_opt
  f_proposal_theta = torch.zeros(1)

  thetas = torch.zeros(n_iterations, X.size(1))
  thetas[0] = theta_opt
  for t in range(1, n_iterations):
    xi = torch.zeros(theta_opt.size(0)).normal_(0, 1)
    theta_new = theta_opt + h**(1/2) * C_half @ xi

    # MH step
    f_proposal_theta_new = 1/(2.0) * xi.pow(2).sum()
    f_target_theta_new = bceloss(b_opt + X @ theta_new, Y.double()) \
                         + 1/(2.0 * sigma2_prior) * theta_new @ C_inv @ theta_new
    u_sample = torch.zeros(1).uniform_(0, 1)
    if torch.log(u_sample) <= f_proposal_theta_new - f_target_theta_new + f_target_theta - f_proposal_theta:  
      thetas[t] = theta_new

      # Update the previous iteration values if accepted
      f_proposal_theta = f_proposal_theta_new
      f_target_theta = f_target_theta_new

      accepts[t] = 1
    else:
      thetas[t] = thetas[t-1]

  return b_opt, thetas, accepts



def bayesian_logistic_regression_with_iteration_times(X, Y, sigma2_prior, C,
                                                      n_iterations, h,
                                                      stepsize_opt = .1, tol_opt = 10**(-10), max_iterations_opt = 10**5):
  iteration_times = torch.zeros(n_iterations)
  accepts = torch.zeros(n_iterations)
  bceloss = torch.nn.BCEWithLogitsLoss(reduction="sum")
  C_half = torch.linalg.cholesky(C)
  C_inv = torch.cholesky_inverse(C_half)

  # Optimize target
  b_opt, theta_opt = graddescent(X, Y, sigma2_prior, C,
                                 stepsize_opt, tol_opt, max_iterations_opt)
  # Compute the previous theta using the opt
  f_target_theta = bceloss(b_opt + X @ theta_opt, Y.double()) \
                   + 1/(2.0 * sigma2_prior) * theta_opt @ C_inv @ theta_opt
  f_proposal_theta = torch.zeros(1)

  thetas = torch.zeros(n_iterations, X.size(1))
  thetas[0] = theta_opt
  for t in range(1, n_iterations):
    # Record iteration time
    timestart = time.time()

    xi = torch.zeros(theta_opt.size(0)).normal_(0, 1)
    theta_new = theta_opt + h**(1/2) * C_half @ xi

    # MH step
    f_proposal_theta_new = 1/(2.0) * xi.pow(2).sum()
    f_target_theta_new = bceloss(b_opt + X @ theta_new, Y.double()) \
                         + 1/(2.0 * sigma2_prior) * theta_new @ C_inv @ theta_new
    u_sample = torch.zeros(1).uniform_(0, 1)
    if torch.log(u_sample) <= f_proposal_theta_new - f_target_theta_new + f_target_theta - f_proposal_theta:  
      thetas[t] = theta_new

      # Update the previous iteration values if accepted
      f_proposal_theta = f_proposal_theta_new
      f_target_theta = f_target_theta_new

      accepts[t] = 1
    else:
      thetas[t] = thetas[t-1]
    
    # Record iteration time
    timeend = time.time()
    iteration_times[t] = timeend - timestart

  return b_opt, thetas, accepts, iteration_times




'''
###
# Test example
###
n_features = 100
n_samples = 10
sigma2_prior = 1

# Generate data
b_true = 1
theta_true = torch.zeros(n_features).normal_(0, sigma2_prior**(1/2))
X = torch.zeros(n_samples, n_features).uniform_(-1, 1)
Y = torch.zeros(n_samples, dtype=torch.long)
prob = torch.sigmoid(b_true + X @ theta_true)
for i in range(0, Y.size(0)):
  Y[i] = torch.bernoulli(prob[i])


# CMHI Sampler
bias, thetas, accepts = bayesian_logistic_regression(X, Y, sigma2_prior = sigma2_prior, C = torch.eye(n_features),
                                               n_iterations = 10**4, h = .9 * sigma2_prior)
  
print("CMHI Sampler:")
print("n accepts:", int(accepts.sum().item()))

predictions = torch.round(torch.sigmoid(bias + X @ thetas.mean(0))).long()
accuracy = 1/Y.size(0)*torch.sum(predictions == Y).item()
print("accuracy:", accuracy)
'''
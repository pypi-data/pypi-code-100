from setuptools import setup, find_packages

setup(
  name="cmhi", 
  version="0.1",
  author="Austin Brown",
  author_email="brow5079@umn.edu",
  description="'Centered' Metropolis-Hastings Independence algorithm for Bayesian logistic regression",
  url = "https://github.umn.edu/brow5079/Centered-Metropolis-Hastings",
  packages=["cmhi"],
  install_requires=["torch >= 1.9.1"],
  keywords=["Metropolis-Hastings", "MCMC"]
)


import sys
import os
import casadi.casadi as cs
import opengen as og

optimizers_dir = "my_optimizers"
optimizer_name = "rosenbrock"

u = cs.SX.sym("u", 5)  # decision variable (nu = 5)
p = cs.SX.sym("p", 2)  # parameter (np = 2)
phi = og.functions.rosenbrock(u, p)  # cost function

s = og.constraints.Simplex(alpha=1.5)
b = og.constraints.Ball1(center=[1., 0.3], radius=1)
bounds = og.constraints.CartesianProduct([2, 4], [s, b])

problem = og.builder.Problem(u, p, phi) \
    .with_constraints(bounds)
meta = og.config.OptimizerMeta() \
    .with_optimizer_name(optimizer_name)


build_config = og.config.BuildConfiguration() \
    .with_build_directory(optimizers_dir) \
    .with_build_mode(og.config.BuildConfiguration.DEBUG_MODE) \
    .with_build_python_bindings() \
    .with_open_version(local_path="/Users/3054363/Documents/Development/OpEn")

builder = og.builder.OpEnOptimizerBuilder(problem,
                                          meta,
                                          build_config,
                                          og.config.SolverConfiguration())
builder.build()

sys.path.insert(1, os.path.join(optimizers_dir, optimizer_name))
rosenbrock = __import__(optimizer_name)

solver = rosenbrock.solver()
result = solver.run([1., 2.])
x_star = result.solution
print(sum(x_star))

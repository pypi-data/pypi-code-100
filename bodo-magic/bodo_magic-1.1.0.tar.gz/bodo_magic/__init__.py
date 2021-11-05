import ast
import asyncio
import sys
from hashlib import blake2b

from IPython.core.magic import (Magics, magics_class, cell_magic)
from IPython.core.magic_arguments import (
  argument, 
  magic_arguments,
  parse_argstring,
)

from .utils import decorator_gen, arg_gen, split_top, BodoVisitor, eprint, get_args


@magics_class
class BodoMagic(Magics):
  @cell_magic
  @magic_arguments()
  @argument(
    "-v",
    "--verbose",
    dest="verbose",
    action="store_true",
    help="Print Verbose and Debugging Info",
  )
  @argument(
    "-c",
    "--cache",
    dest="cache",
    action="store_true",
    help="Enable Caching on the Wrapped Function",
  )
  @argument(
    "-d",
    "--dry-run",
    dest="dry",
    action="store_true",
    help="Do Not Execute Any Code or Wrapper Function",
  )
  @argument(
    "-o",
    "--outputs",
    dest="outputs",
    action="store",
    nargs="*",
    help="Variables to Output from the Wrapped Function (default: Returns All Defined Variables)"
  )
  def bodo(self, line: str, cell: str):
    # Argument Parsing
    args = parse_argstring(self.bodo, line)
    if args.verbose:
      print("Magic Args:", args, "\n")

    # Generate Decorator for Functions
    decorator = decorator_gen(args.cache)

    # Generate Hash From Cell Input
    hashed = blake2b(cell.encode('utf-8'), digest_size=4).hexdigest()
    func_name = f'_func_{hashed}'


    # Parse Input to AST and Split Top Level Stuff
    cell_ast = ast.parse(cell)
    top_split, cell_ast = split_top(cell_ast, decorator)

    # Traverse AST for Warnings and Getting Assignments
    visitor = BodoVisitor()
    visitor.visit(cell_ast)

    # Print Import and Function Warnings
    if visitor.has_function:
      eprint("Warning: The %%bodo magic does not officially support functions in cells.")

    if visitor.has_import:
      eprint("Warning: The %%bodo magic only supports top-level 'import' statements at the beginning of the cell.")


    # Determine Inputs to Wrapper Function
    wrapped_ast = ast.Module(type_ignores=[], body=[ast.FunctionDef(
      name=func_name,
      args=arg_gen([]),
      body=cell_ast.body,
      returns=None,
      decorator_list=[],
      type_comment=None,
    )])

    wrapped_ast = ast.fix_missing_locations(wrapped_ast)
    wrapped_code = compile(wrapped_ast, "", "exec")
    exec(wrapped_code, globals())
    inputs = get_args(globals()[func_name], self.shell.user_ns)

    # Set Outputs / Return Value for Wrapper Function
    outputs = list(visitor.outputs) if args.outputs is None else args.outputs


    # Handle Returning Expression
    has_output = False
    if isinstance(cell_ast.body[-1], ast.Expr):
      has_output = True
      output_name = f'_ret_{hashed}'
      outputs.append(output_name)

      expr = cell_ast.body[-1].value
      cell_ast.body[-1] = ast.Assign(value=expr, targets=[
        ast.Name(id=output_name, ctx=ast.Store())
      ])


    if args.verbose:
      print("args:   ", ', '.join(inputs))
      print("returns:", ', '.join(outputs))
      print("retexpr:", has_output)
      print()


    # Crafting the New AST
    func_args = arg_gen(inputs)

    new_ast_body = top_split
    new_ast_body.insert(0, ast.Import(names=[ast.alias(name='bodo')]))
    new_ast_body.append(ast.FunctionDef(
      name=func_name,
      args=func_args,
      body=cell_ast.body + [
        ast.Return(ast.Tuple(ctx=ast.Load(), elts=[
          ast.Name(ctx=ast.Load(), id=output) for output in outputs
        ]))
      ],
      returns=None,
      decorator_list=[decorator],
      type_comment=None,
    ))
    
    new_ast_body.append(ast.Assign(
      targets=[ast.Tuple(ctx=ast.Store(), elts=[
        ast.Name(ctx=ast.Store(), id=output) for output in outputs
      ])],
      value=ast.Call(
        func=ast.Name(func_name, ctx=ast.Load()),
        args=[ast.Name(id=arg, ctx=ast.Load()) for arg in inputs],
        keywords=[]
      )
    ))

    if has_output:
      new_ast_body.append(
        ast.Expr(value=ast.Name(id=output_name, ctx=ast.Load()))
      )

    new_ast = ast.Module(
      body=new_ast_body,
      type_ignores=cell_ast.type_ignores,
    )

    new_ast = ast.fix_missing_locations(new_ast)


    # Final Steps
    if args.verbose:
      if sys.version_info >= (3, 9):
        new_str = ast.unparse(new_ast)
        for idx, line in enumerate(new_str.split('\n'), start=1):
          print(f'{idx:2}:  {line}')
      else:
        print(ast.dump(new_ast))

    if args.dry:
      return

    exec_code = compile(new_ast, f"ipython_{hashed}.py", "exec")
    asyncio.run(self.shell.run_code(exec_code), debug=args.verbose)


def load_ipython_extension(ipython):
    "Register the bodo magic with IPython"
    ipython.register_magics(BodoMagic)


from importlib.metadata import version, PackageNotFoundError

try:
  __version__ = version("bodo-magic")
except PackageNotFoundError:
  pass

del version, PackageNotFoundError

import ast
import sys
from types import ModuleType
from typing import List, Callable, Tuple, Union

from numba.core import ir_utils, ir


def eprint(*args, **kwargs):
  print(*args, file=sys.stderr, **kwargs)


def arg_gen(args):
  return ast.arguments(
    args=[ast.arg(arg) for arg in args],
    posonlyargs=[],
    vararg=None,
    kwonlyargs=[],
    kw_defaults=[],
    kwarg=None,
    defaults=[],
  )


def decorator_gen(enable_cache):
  "Generate Bodo Decorators for Functions in the Cell"
  keywords = [ast.keyword(
    arg='returns_maybe_distributed',
    value=ast.Constant(value=True, kind=None),
  )]

  if enable_cache:
    keywords.append(ast.keyword(
      arg="cache",
      value=ast.Constant(value=True, kind=None),
    ))

  return ast.Call(
    func=ast.Attribute(
      value=ast.Name(id='bodo', ctx=ast.Load()),
      attr='jit',
      ctx=ast.Load(),
    ),
    keywords=keywords,
    args=[],
  )


def split_top(cell_ast: ast.Module, decorator) -> Tuple[
  List[Union[ast.Import, ast.ImportFrom, ast.FunctionDef]], 
  ast.Module,
]:
  "Split Top-Level Module Imports and Function Definitions from Cell String"
  split = False
  imports_defs = []
  rest = []

  for elem in cell_ast.body:
    if split:
      rest.append(elem)

    else:  
      if isinstance(elem, ast.Import) or isinstance(elem, ast.ImportFrom):
        imports_defs.append(elem)

      elif isinstance(elem, ast.FunctionDef):
        imports_defs.append(ast.FunctionDef(
          name=elem.name,
          args=elem.args,
          body=elem.body,
          returns=elem.returns,
          decorator_list=[decorator],
          type_comment=elem.type_comment,
        ))

      else:
        rest.append(elem)
        split = True

  rest_ast = ast.Module(body=rest, type_ignores=cell_ast.type_ignores)
  return (imports_defs, rest_ast)


def get_args(cell_func: Callable[[], None], global_vars):
  ans = []
  cell_ir = ir_utils.compile_to_numba_ir(cell_func, global_vars)

  for block in cell_ir.blocks.values():
    for line in block.body:
        if isinstance(line, ir.Assign) \
            and isinstance(line.value, ir.Global) \
            and not isinstance(line.value.value, (ir.UndefinedType, ModuleType, type)):
          ans.append(line.value.name)

  return ans


class BodoVisitor(ast.NodeVisitor):
  def visit_Module(self, node):
    self.outputs = set()
    self.has_import = False
    self.has_function = False
    self.generic_visit(node)

  def visit_Assign(self, node):
    for elem in node.targets:
      self.outputs.add(elem.id)
    self.generic_visit(node.value)

  def visit_Import(self, _):
    self.has_import = True

  def visit_ImportFrom(self, _):
    self.has_import = True

  def visit_FunctionDef(self, _):
    self.has_function = True

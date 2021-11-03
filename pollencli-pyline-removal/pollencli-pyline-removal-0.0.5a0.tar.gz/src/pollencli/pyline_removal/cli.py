import ast
from logging import getLogger
from pathlib import Path
from typing import Union

logger = getLogger(__name__)


class RemoveExprHavingSpecificNameChild(ast.NodeTransformer):
    def __init__(self, target_name_id: str):
        self.target_name_id: str = target_name_id

    def visit_Expr(self, node: ast.Expr):
        for child_node in ast.walk(node):
            logger.debug(f"{type(child_node)=}")
            if isinstance(child_node, ast.Name) and child_node.id == self.target_name_id:
                return None
        return node


def remove_pyline(source_filepath: Union[str, Path], target_name_id: str, verbose: bool = False):
    with open(source_filepath, "rt") as f:
        source_code = f.read()
    tree = ast.parse(source_code)
    if verbose:
        msg: str = f"input_ast: {ast.dump(tree)}"
        logger.debug(msg)
        print(msg)
    tree = RemoveExprHavingSpecificNameChild(target_name_id=target_name_id).visit(tree)
    print(ast.unparse(tree))


def main():
    import argparse

    parser = argparse.ArgumentParser(description="Remove logger from code")
    parser.add_argument("name_id", type=str, help="Removing Name Node ID")
    parser.add_argument("source_filepath", type=lambda x: Path(x), help="Input file path")
    parser.add_argument("--verbose", action="store_true", help="debug mode")
    args = parser.parse_args()

    remove_pyline(source_filepath=args.source_filepath, target_name_id=args.name_id, verbose=args.verbose)


if __name__ == "__main__":
    main()

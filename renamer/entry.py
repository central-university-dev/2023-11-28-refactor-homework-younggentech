import datetime
import os
from _ast import ClassDef, Import, Name, Attribute

import libcst as cst
import libcst.matchers as m


class BasicUpdater:
    """Encapsulate params to be changed."""
    def __init__(self, old_name, target_name):
        self._old_name = old_name
        self._target_name = target_name


class RenameClass(BasicUpdater, cst.CSTTransformer):
    """Rename Classes and definitions of inherrited classes."""
    def leave_ClassDef(self, original_node: "ClassDef", updated_node: "ClassDef"):
        if original_node.name.value == self._old_name:
            new_node = updated_node.name.with_changes(value=self._target_name)
            return updated_node.with_changes(name=new_node)
        return updated_node

    def leave_Name(self, original_node: "Name", updated_node: "Name"):
        if original_node.value == self._old_name:
            return updated_node.with_changes(value=self._target_name)
        return updated_node


class UpdateClassImports(BasicUpdater, cst.CSTTransformer):
    """Rename imports of a specific class."""
    def leave_ImportAlias(self, original_node: "Import", updated_node: "Import"):
        if original_node.name.value == self._old_name:
            updated_node = original_node.name.with_changes(value=self._target_name)
            return original_node.with_changes(name=updated_node)
        return original_node


def rename(source_code: str, transformer: BasicUpdater) -> str:
    """Apply transformer to modify the source code."""
    original_tree = cst.parse_module(source_code)
    renamed_tree = original_tree.visit(transformer)
    return renamed_tree.code


def update_classname(fpath: str, old_name: str, target_name: str,
                     local_update_imports: str | None = None) -> str:
    """Update Classes in the specified file and their imports within a directory if required."""
    with open(fpath) as file:
        source_code = file.read()
    rename_transformer = RenameClass(old_name, target_name)
    updated_code = rename(source_code, rename_transformer)
    new_fname = fpath.replace(".py", "") + "_refactorred_.py"
    with open(new_fname, "w") as out_file:
        out_file.write(updated_code)

    if local_update_imports is None:
        return updated_code
    import_transformer = UpdateClassImports(old_name, target_name)
    for path in os.listdir(local_update_imports):
        path = local_update_imports + path
        with open(path) as imp_update_file:
            imp_source_code = imp_update_file.read()
            updated_imp = rename(imp_source_code, import_transformer)
        if updated_imp != imp_source_code:
            new_fname = path.replace(".py", "") + "_refactorred_.py"
            with open(new_fname, 'w') as out_f_imp:
                out_f_imp.write(updated_imp)
    return updated_code

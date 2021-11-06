import os
import sys
from subprocess import Popen, PIPE

here = os.path.abspath(os.path.dirname(__file__))


def system_cmd(command, wait=True, dir_=here):
    command = command if isinstance(command, str) else " ".join(command)
    sep = " && " if sys.platform == "win32" else " ; "
    env = r" %ENV%" if sys.platform == "win32" else "$ENV"
    executable = None if sys.platform == "win32" else '/bin/bash'
    commands = (env, "cd %s" % (dir_,), command)
    process = Popen(sep.join(commands), shell=True, stdout=PIPE, executable=executable)
    if wait:
        process.wait()
    return process


def local_name(filename):
    return os.path.split(filename)[-1]


def unversioned_name(filename):
    return local_name(filename).split(".")[0]
    # return ".".join((filename_parts[0], filename_parts[-1]))


def dependencies(libname):
    if sys.platform == "win32":
        return list()
    elif sys.platform == "darwin":
        command = ['/usr/bin/otool', '-L', libname]
    elif sys.platform == "linux" or sys.platform == "linux2":
        command = ['/usr/bin/ldd', libname]
        return []
    else:
        raise (OSError, "Unsupported Platform")

    dependency_list = []
    o = system_cmd(command)
    for l in o.stdout:
        line = l.decode("utf-8")
        if line[0] == '\t':
            dependency_list.append(line.split(' ', 1)[0][1:])
    return dependency_list


def replace_runtime_path(libname, sublibname):
    if sys.platform == "win32":
        return
    elif sys.platform == "darwin":
        system_cmd(['install_name_tool', '-change', sublibname, os.sep.join(('@rpath', local_name(sublibname))), libname])
    elif sys.platform == "linux" or sys.platform == "linux2":
        return
        # system_cmd(['patchelf', '--replace-needed', sublibname, os.sep.join(('@rpath', local_name(sublibname))), libname])
    else:
        raise (OSError, "Unsupported Platform")
    print("Replaced Runtime Path: %s -> %s with %s" %(libname, sublibname, os.sep.join(('@rpath', local_name(sublibname)))))


def replace_all_runtime_paths(libname, destination, local_libnames, unversioned_names):
    for sublibname in dependencies(libname):
        if unversioned_name(libname) != unversioned_name(sublibname) and unversioned_name(sublibname) in unversioned_names:
            replace_runtime_path(libname, sublibname)
            sublibname = local_libnames[unversioned_names.index(unversioned_name(sublibname))]
            sublibname = os.sep.join((destination, sublibname))
            replace_all_runtime_paths(sublibname, destination, local_libnames, unversioned_names)


def replace_linker_path(libname, destination):
    if sys.platform == "win32":
        return
    elif sys.platform == "darwin":
        system_cmd(['install_name_tool', '-id', os.sep.join(('@rpath', local_name(libname))), libname])
    elif sys.platform == "linux" or sys.platform == "linux2":
        return
    else:
        raise (OSError, "Unsupported Platform")
    print("Replaced Linker Path: " + libname)


def create_shared_object(libname, destination):
    local_libname = local_name(libname)
    if sys.platform == "win32":
        local_soname = local_libname.replace("py.dll", ".pyd")
        system_cmd(['copy', os.sep.join((destination, local_libname)), os.sep.join((destination, local_soname))])
        system_cmd(['del', " /f", os.sep.join((destination, local_libname))])
    elif sys.platform == "darwin":
        local_soname = local_libname[3::].replace("py.dylib", ".so")
        system_cmd(['rm', "-rf", os.sep.join((destination, local_soname))])
        system_cmd(['ln', os.sep.join((destination, local_libname)), os.sep.join((destination, local_soname))])
    elif sys.platform == "linux" or sys.platform == "linux2":
        local_soname = local_libname[3::].replace("py.so", ".so")
        system_cmd(['rm', "-rf", os.sep.join((destination, local_soname))])
        system_cmd(['ln', os.sep.join((destination, local_libname)), os.sep.join((destination, local_soname))])
        return
    else:
        raise (OSError, "Unsupported Platform")
    print("Created Shared Object: " + local_soname)


# def distribute_core_libs(libname, destination):
#     if sys.platform == "win32":
#         for libname in libnames:
#             system_cmd(['copy', libname, destination])
#     elif sys.platform == "darwin":
#         for libname in libnames:
#             system_cmd(['cp', libname, destination])
#     elif sys.platform == "linux" or sys.platform == "linux2":
#         for libname in libnames:
#             system_cmd(['cp', libname, destination])
#     else:
#         raise (OSError, "Unsupported Platform")


def distribute_library(libname, destination):
    if sys.platform == "win32":
        suffix = ["dll"]
    elif sys.platform == "darwin":
        suffix = ["dylib", "framework"]
    elif sys.platform == "linux" or sys.platform == "linux2":
        suffix = ["so"]
    else:
        raise (OSError, "Unsupported Platform")
    libname = ".".join((libname, suffix[0]))
    local_libnames, unversioned_libnames = [], []
    for filename in os.listdir(destination):
        local_libname = local_name(filename)
        fileparts = local_libname.split(".")
        if len(fileparts) == 2 and fileparts[-1] in suffix:
            local_libnames.append(local_libname)
            unversioned_libnames.append(unversioned_name(local_libname))
    replace_all_runtime_paths(libname, destination, local_libnames, unversioned_libnames)
    replace_linker_path(libname, destination)


def distribute_plugin(libname, destination):
    if sys.platform == "win32":
        suffix = ["dll"]
    elif sys.platform == "darwin":
        suffix = ["dylib", "framework"]
    elif sys.platform == "linux" or sys.platform == "linux2":
        suffix = ["so"]
    else:
        raise (OSError, "Unsupported Platform")
    libname = ".".join((libname, suffix[0]))
    if sys.platform == "win32":
        system_cmd(['move', libname, destination])
    elif sys.platform == "darwin":
        system_cmd(['mv', libname, destination])
    elif sys.platform == "linux" or sys.platform == "linux2":
        system_cmd(['mv', libname, destination])
    else:
        raise (OSError, "Unsupported Platform")
    print("Moved Plugin %s -> %s" % (libname, destination))


def distribute_shiboken(libname, destination):
    if sys.platform == "win32":
        suffix = ["dll"]
    elif sys.platform == "darwin":
        suffix = ["dylib", "framework"]
    elif sys.platform == "linux" or sys.platform == "linux2":
        suffix = ["so"]
    else:
        raise (OSError, "Unsupported Platform")
    libname = ".".join((libname, suffix[0]))
    local_libnames, unversioned_libnames = [], []
    for filename in os.listdir(destination):
        local_libname = local_name(filename)
        fileparts = local_libname.split(".")
        if len(fileparts) == 2 and fileparts[-1] in suffix:
            local_libnames.append(local_libname)
            unversioned_libnames.append(unversioned_name(local_libname))
    replace_all_runtime_paths(libname, destination, local_libnames, unversioned_libnames)
    replace_linker_path(libname, destination)
    create_shared_object(libname, destination)


if __name__ == "__main__":
    if sys.argv[1] == "lib":
        distribute_library(sys.argv[2], sys.argv[3])
    if sys.argv[1] == "plugin":
        distribute_plugin(sys.argv[2], sys.argv[3])
    if sys.argv[1] == "shiboken":
        distribute_shiboken(sys.argv[2], sys.argv[3])






from . import paths
import os
import subprocess


def get_current_home_dir():
    return os.path.expanduser('~')


def execute_capture(command):
    os_exec = os.popen(command)
    Read = os_exec.read()
    os_exec.detach()
    return Read



def command(args: list, quite=False, read=False):
    if quite:
        sub = subprocess.Popen(args, stdout=subprocess.DEVNULL, stderr=subprocess.STDOUT)

    elif read:
        sub = subprocess.Popen(args, stdout=subprocess.PIPE, stdin=subprocess.PIPE,
                               stderr=subprocess.STDOUT)

        response = sub.communicate()[0].decode('utf8')
        sub.wait()
        sub.poll()
        returnCode = int(sub.returncode)

        return response, returnCode, sub
    else:
        sub = subprocess.Popen(args)

    sub.wait()
    sub.kill()
    sub.terminate()


def remove(file):
    command(args=['rm', '-rf', file])


def get_ip():
    ip = command(['ipconfig', 'getifaddr', 'en0'], read=True)
    return ip[0].removesuffix('\n')


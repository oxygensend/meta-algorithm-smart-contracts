import re
import subprocess

from config import data_dir


def smartcheck_analyst(file_path):
    cmd = 'smartcheck -p ' + file_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')

    if out != '':
        matches = re.findall(r'content: .*?\n(.*(?:\n.*)*)', out)
        out = matches[0]
        save_output('smartcheck_output.txt', out)

    if err != '':
        save_output('smartcheck_error.txt', err)

    return out, err


def save_output(file_path, output):
    with open(data_dir(file_path), 'w') as f:
        f.write(output)

import re
import subprocess
import logging

from config import data_dir

INVALID_VERSION_PATTERN = r'pragma directive defines a prior version to (0\.\d+(?:\.\d+)?)'


def securify_analyst(file_path):
    cmd = 'securify ' + file_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    out = out.decode('utf-8')
    err = err.decode('utf-8')

    if out != '':
        if re.search(INVALID_VERSION_PATTERN, out):
            logging.error('Securify excluded due to invalid version message: {}', err)
            return '', ''

        out = (out.replace('[0m', '')
               .replace('[0;31m', '')
               .replace('\x1b', ''))
        save_output('securify_output.txt', out)
    if err != '':
        save_output('securify_error.txt', err)

    return out, err


def save_output(file_path, output):
    with open(data_dir(file_path), 'w') as f:
        f.write(output)

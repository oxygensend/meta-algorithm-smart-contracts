import subprocess


def smartcheck_analyst(file_path):
    cmd = 'smartcheck -p ' + file_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    if out != b'':
        save_output('data/smartcheck_output.txt', out)

    if err != b'':
        save_output('data/smartcheck_error.txt', err)

    return out, err


def save_output(file_path, output):
    with open(file_path, 'wb') as f:
        f.write(output)

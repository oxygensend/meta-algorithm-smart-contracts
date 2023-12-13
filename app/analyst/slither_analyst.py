import subprocess


def slither_analyst(file_path):
    cmd = 'slither ' + file_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()

    save_output('data/slither_output.txt', err)

    return out, err


def save_output(file_path, output):
    with open(file_path, 'wb') as f:
        f.write(output)
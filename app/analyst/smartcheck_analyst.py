import subprocess


def smartcheck_analisists(file_path):
    cmd = 'smartcheck -p ' + file_path
    p = subprocess.Popen(cmd, shell=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
    out, err = p.communicate()
    print(out)
    return out, err

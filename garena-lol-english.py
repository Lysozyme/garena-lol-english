import psutil
import time
import sys

LOL_PROCESS_NAME = 'RiotClientServices.exe'
LOCALE_ARG_PREFIX = '--locale='
LOCALE_ARG_EN = LOCALE_ARG_PREFIX + 'en_US'


def find_process_by_name(process_name):
    for p in psutil.process_iter():
        try:
            if p.name() == process_name:
                return p
        except psutil.AccessDenied:
            pass
    return None


def is_english_lol(process):
    return LOCALE_ARG_EN in process.cmdline()


def kill_process_tree(process):
    for child in process.children(recursive=True):
        child.kill()
    process.kill()


def run_english_lol(old_cmdline):
    new_cmdline = old_cmdline
    for i, arg in enumerate(new_cmdline):
        if arg.startswith(LOCALE_ARG_PREFIX):
            new_cmdline[i] = LOCALE_ARG_EN
    psutil.Popen(new_cmdline)


def main():
    print('MAKE SURE TO RUN AS ADMIN!')
    lol_process = None
    while True:
        print('Looking for LoL')
        lol_process = find_process_by_name(LOL_PROCESS_NAME)
        if lol_process is not None:
            break
        else:
            time.sleep(1)
    if is_english_lol(lol_process):
        print('Found English LoL, will not do anything')
        sys.exit()
    else:
        print('Found non-English LoL')
    lol_cmdline = lol_process.cmdline()
    print('Killing non-English LoL')
    kill_process_tree(lol_process)
    print('Launching English LoL')
    run_english_lol(lol_cmdline)


if __name__ == '__main__':
    main()

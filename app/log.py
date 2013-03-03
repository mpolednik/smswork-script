from config.files import files

NOTICE='[??]'
FAIL='[!!]'
OK='[OK]'

def write(state, file, message):
    print ' '.join((state, files[file], message))

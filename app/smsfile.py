import re

def parseline(line):
    line = re.findall('([A-Z]*)="([^"]*)', line.replace('""', '{QUOTE}'))
    return dict(line)

def add(phone, text, id):
    text = text.replace('"', '""')
    return 'STATE="NEW" PHONE="%s" TEXT="%s" ID="%s"\n' % (phone, text, id)

from time import sleep

from app import smsfile
from app import log

from config.files import files

import app.db as db

from app.sentsms import SentSMS
from app.receivedsms import ReceivedSMS

# SENDING PROCESS
states = ('DONE', 'ERROR')

def handle_sent():
    session = db.Session()
    lines = []

    # Process current entries in file
    try:
        with open(files['outfile'], 'r') as f:
            log.write(log.NOTICE, 'outfile', 'Opening file')

            for line in f:
                parse = smsfile.parseline(line)

                # Handle message based on status
                if 'STATE' in parse and parse['STATE'] in states:

                    if parse['STATE'] == 'DONE':
                        try:
                            SentSMS.update_state(parse['ID'], 2)

                            log.write(log.NOTICE, 'outfile', 'Updating and ' \
                                      'removing message (id: %s; status: 2)' % 
                                      parse['ID'])
                        except:
                            lines.append(line)

                            log.write(log.NOTICE, 'outfile', 'Failed to ' \
                                      'update status and remove message ' \
                                      '(id: %s; status: 2)' % parse['ID'])

                    if parse['STATE'] == 'ERROR':
                        try:
                            SentSMS.update_state(parse['ID'], 3)

                            log.write(log.NOTICE, 'outfile', 'Updating ' \
                                      'status and removing message (id: %s; ' \
                                      'status: 3)'  % parse['ID'])
                        except:
                            lines.append(line)

                            log.write(log.NOTICE, 'outfile', 'Failed to ' \
                                      'update status and remove message ' \
                                      '(id: %s; status: 3)' % parse['ID'])

                else:
                    # State unexistant or unknown - simply write the line back
                    lines.append(line)
    except Exception as e:
        log.write(log.FAIL, 'outfile', 'Could not process file: %s' % (e))
    else:
        # Append new entries
        try:
            usms = SentSMS.get_unprocessed()

            log.write(log.NOTICE, 'outfile', 'Fetched %d messages' % 
                      len(usms))
        except:
            log.write(log.FAIL, 'outfile', 'Could not fetch unprocessed ' \
                      'messages from database')
        else:
            for sms in usms:
                sms.state = 1
                lines.append(smsfile.add(sms.phone, sms.text, sms.id))

                log.write(log.NOTICE, 'outfile', 'Adding message (phone: ' \
                          '%s; text: %s; id: %s)' % 
                          (sms.phone, sms.text, sms.id))
        try:
            with open(files['outfile'], 'w') as f:
                f.write(''.join(lines))

            log.write(log.NOTICE, 'outfile', 'Writing %d messages back to ' \
                      'file' % (len(lines)))

            session.commit()

            log.write(log.NOTICE, 'outfile', 'Comitting database changes')
        except:
            session.rollback()

            log.write(log.FAIL, 'outfile', 'Could not commit changes to ' \
                      'database')
        else:
            log.write(log.OK, 'outfile', 'Processed file')

def handle_recv():
    session = db.Session()
    lines = []

    try:
        with open(files['infile'], 'r') as f:
            log.write(log.NOTICE, 'infile', 'Opening file')
            for line in f:
                data = smsfile.parseline(line)
                try:
                    sms = ReceivedSMS(data['PHONE'],
                                      data['TEXT'], data['TIME'])
                    session.add(sms)

                    log.write(log.NOTICE, 'infile', 'Adding message by %s ' \
                              'with text %s (timestamp: %s)' %
                              (data['PHONE'], data['TEXT'], data['TIME']))
                except:
                    lines.append(line)

                    log.write(log.FAIL, 'infile', 'Could not add ' \
                              'message(%s, %s, %s) to database' %
                              (data['PHONE'], data['TEXT'], data['TIME']))
    except Exception as e:
        log.write(log.FAIL, 'infile', 'Could not process file: %s' % (e))
    else:
        try:
            with open(files['infile'], 'w') as f:
                f.write(''.join(lines))

            log.write(log.NOTICE, 'infile', 'Writing %s messages back to ' \
                      'file' % (len(lines)))
            
            session.commit()

            log.write(log.NOTICE, 'infile', 'Comitting database changes')
        except:
            session.rollback()

            log.write(log.FAIL, 'infile', 'Could not commit changes to ' \
                      'database')
        else:
            log.write(log.OK, 'infile', 'Processed file')

while True:
    handle_sent()
    handle_recv()
    sleep(10)

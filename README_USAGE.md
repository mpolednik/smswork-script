Maturita SMS server
===================
Connect to remote database

* Server: localhost
* Username: your_username
* Password: your_password
* Port: 3306

To send new message...

Insert new row into table **sms_send**

Required values

    phone - Integer
    text - Char(160)

    Send message to 600600600 containing text 'Hello World!' from user root
    INSERT INTO sms_send(phone, text, owner) VALUES('600600600', 'Hello World!', root);

To fetch information about the sent message

Select requested information from the table **sms_send**

Table structure

    id - Char(200)
    phone - Char(200)
    text - Char(200)
    ts - Char(200)
    owner - Char(200)
    state - Char(200)
        0 - unprocessed
        1 - processed
        2 - sent
        3 - error

    Send message to 600600600 containing text 'Hello World!' from user root
    INSERT INTO sms_send(phone, text, owner) VALUES('600600600', 'Hello World!', root);

To fetch received messages...

Select requested information from the table **sms_recv**

Table structure

    id - Integer: identifier, not relevant
    phone - Integer: Sender's phone phone 
    text - Char(160): Text body
    ts - Timestamp: Unix timestamp of received message

    Select all messages received in last 2 days
    SELECT phone, text, ts FROM sms_recv [WHERE ts > TIMEDIFF(NOW(), SUBTIME(NOW(), '2 0:0.0');
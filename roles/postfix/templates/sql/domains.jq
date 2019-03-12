user = vmail
password = {{ vmail_pass }}
hosts = 127.0.0.1
dbname = vmail
query = SELECT domain FROM domains WHERE domain='%s'
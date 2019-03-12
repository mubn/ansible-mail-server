user = vmail
password = {{ vmail_pass }}
hosts = 127.0.0.1
dbname = vmail
query = select 1 as found from accounts where username = '%u' and domain = '%d' and enabled = true LIMIT 1;

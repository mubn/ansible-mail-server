user = vmail
password = {{ vmail_pass }}
hosts = 127.0.0.1
dbname = vmail
query = SELECT policy, params FROM tlspolicies WHERE domain = '%s'
user = vmail
password = {{ vmail_pass }}
hosts = 127.0.0.1
dbname = vmail
query = select concat(destination_username, '@', destination_domain) as destinations from aliases where source_username = '%u' and source_domain = '%d' and enabled = true;

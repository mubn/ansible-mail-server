user = vmail
password = {{ vmail_pass }}
hosts = 127.0.0.1
dbname = vmail
query = select concat(username, '@', domain) as 'owns' from accounts where username = '%u' AND domain = '%d' and enabled = true union select concat(destination_username, '@', destination_domain) AS 'owns' from aliases where source_username = '%u' and source_domain = '%d' and enabled = true;

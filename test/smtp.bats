#!/usr/bin/env bats

# https://github.com/sstephenson/bats
# Requirements
# - curl

@test "Email send with curl returns no errors" {
  curl -sv --ssl --user $mail_user:$mail_pass \
  smtp://$mail_host --mail-from $mail_user \
  --mail-rcpt $mail_user --upload-file mail.txt
  [[ $? == 0 ]]
}

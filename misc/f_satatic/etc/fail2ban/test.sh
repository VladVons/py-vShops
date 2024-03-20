#fail2ban-regex /home/vladvons/www/vShops/src/vShops.log /etc/fail2ban/filter.d/vShops.conf
fail2ban-client status
fail2ban-client status vShops
fail2ban-client banned
#
fail2ban-client unban --all

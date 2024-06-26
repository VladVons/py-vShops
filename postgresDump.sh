#!/bin/bash
# VladVons@gmail.com
# Created: 2024.06.25

# crontab -e
# 0 23 * * * /home/vladvons/www/vShops/postgresDump.sh


DbBackup()
{
    #echo "hostname:port:database:username:password" > ~/.pgpass

    Host="localhost"
    Port="5433"
    DbName="used"
    User="admin"
    #
    File="$(hostname)_${DbName}.sql.dat"
    Date=$(date "+%y%m%d-%H%M")
    PathDump=${Host}_${Date}_${File}.zst

    echo "dump $PathDump ..."
    Cmd="pg_dump --verbose --host=$Host --port=$Port --username=$User --dbname=$DbName | zstd > $PathDump"
    echo $Cmd
    eval $Cmd
}

ToFtp()
{
    #PathDump="localhost_240625-0827_vmi1108500.contaboserver.net_used.sql.dat.zst"

    PasswFtp="/home/vladvons/.passw_ftp1"
    Host="download.oster.com.ua"
    User="backups"
    RemotePath="/backups"

    echo "To FTP $PathDump ..."
    Passw=$(cat $PasswFtp)
    Cmd="wput $PathDump ftp://$User:$Passw@$Host$RemotePath"
    echo $Cmd
    eval $Cmd
}

DbBackup
ToFtp

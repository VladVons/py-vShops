Host="localhost"
#
#Port="5432"
Port="5433"
#
DbName="crawler2"
#DbName="used"
#DbName="used_davyd"
#
User="admin"
#User="davyd"
#
#File="shop2.sql.dat"
#File="vShopsMeta.sql"
File="$(hostname)_${DbName}.sql.dat"
#
Path=${Host}_${File}
Date=$(date "+%y%m%d-%H%M")


Backup()
{
    echo "dump $Path ..."
    #pg_dump --verbose --host=$Host --port=$Port --username=$User --dbname=$DbName > $Path
    #pg_dump --verbose --host=$Host --port=$Port --username=$User --dbname=$DbName | gzip > $Path.gz
    pg_dump --verbose --host=$Host --port=$Port --username=$User --dbname=$DbName | zstd > $Path.zstd
}

BackupData()
{
    echo "dump $Path ..."
    pg_dump --host=$Host --port=$Port --username=$User --dbname=$DbName --data-only --column-inserts > $Path
}

BackupSchema()
{
    echo "dump $Path ..."
    pg_dump --host=$Host --port=$Port --username=$User --dbname=$DbName --schema-only --schema-only > $Path
}

Restore()
{
    cat $Path | psql --host=$Host --port=$Port --username=$User --dbname=$DbName
    #pg_restore --verbose --clean --no-acl --no-owner --host=$Host --port=5432 --dbname=$DbName --username=$User $File
}

Create()
{
    psql --host=$Host --port=$Port --username=$User -d template1 -c "CREATE DATABASE $DbName;"
}

clear

Backup
#BackupData
#BackupSchema
#Create
#Restore

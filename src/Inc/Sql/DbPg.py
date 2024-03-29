# Created: 2022.02.25
# Author: Vladimir Vons <VladVons@gmail.com>
# License: GNU, see LICENSE for more details
#
# pip3 install aiopg


import asyncio
import aiopg
from psycopg2 import errors
from psycopg2.errorcodes import (
    UNIQUE_VIOLATION,
    NOT_NULL_VIOLATION,
    UNDEFINED_COLUMN,
    FOREIGN_KEY_VIOLATION,
    SYNTAX_ERROR
)
#
from IncP.Log import Log
from Inc.DbList import TDbSql
from .ADb import TADb, TDbExecPool


class TDbPg(TADb):
    async def Connect(self) -> bool:
        await self.Close()
        Log.Print(1, 'i', 'Connect()', [self.Auth.host, self.Auth.port, self.Auth.database, self.Auth.user])

        for x in reversed(range(3)):
            try:
                self.Pool = await aiopg.create_pool(
                    host = self.Auth.host,
                    port = self.Auth.port,
                    dbname = self.Auth.database,
                    user = self.Auth.user,
                    password = self.Auth.password,
                    timeout = 10
                )
                break
            except asyncio.TimeoutError as _E:
                Log.Print(1, 'x', f'TDbPg.Connect() to {self.Auth.host} timeout. Try {x} ...')
            # except Exception as E:
            #     Err = str(E).split('\n', maxsplit = 1)[0]
            #     Log.Print(1, 'x', f'TDbPg.Connect() {Err}', [self.Auth.host, self.Auth.port, self.Auth.database, self.Auth.user])
            await asyncio.sleep(3)
        return bool(self.Pool)

    async def GetTablesColumns(self, aTable: list = None) -> dict:
        if (not aTable):
            Data = await self.GetTables()
            aTable = [x[0] for x in Data[0]]

        Res = {}
        for Table in aTable:
            Dbl = await self.GetTableColumns(Table)
            Res[Table] = Dbl.ExportList('column_name')
        return Res

    async def GetTables(self, aSchema: str = 'public') -> TDbSql:
        Query = f'''
            select
                table_name
            from
                information_schema.tables
            where
                table_schema = '{aSchema}'
            order by
                table_name
            '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetTableColumns(self, aTable: str = '', aSchema: str = 'public') -> TDbSql:
        CondTable = f"and table_name = '{aTable}'" if (aTable) else ''

        Query = f'''
            select
                table_name,
                column_name,
                udt_name as column_type,
                is_nullable as is_null
            from
                information_schema.columns
            where
                table_schema = '{aSchema}'
                {CondTable}
            order by
                table_name,
                column_name
            '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetIndexes(self, aTable: str = '', aSchema: str = 'public') -> TDbSql:
        CondTable = f"and t.relname = '{aTable}'" if (aTable) else ''

        Query = f'''
            select
                t.relname as table_name,
                i.relname,
                idxs.indexdef,
                idx.indisunique,
                t.relkind,
                array_to_string(array(
                    select pg_get_indexdef(idx.indexrelid, k + 1, true)
                    from generate_subscripts(idx.indkey, 1) as k
                    order by k), ',')
            from
                pg_catalog.pg_class as t
            inner join
                pg_catalog.pg_index as idx
                on (t.oid = idx.indrelid)
            inner join
                pg_catalog.pg_class as i
                on (idx.indexrelid = i.oid)
            inner join
                pg_catalog.pg_indexes as idxs
                on (idxs.tablename = t.relname and idxs.indexname = i.relname)
            where
                (idxs.schemaname = '{aSchema}')
                {CondTable}
            order by
                idx.indisunique desc,
                i.relname
        '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetPrimaryKeys(self, aTable: str = '', aSchema: str = 'public', aType: str = '') -> TDbSql:
        CondTable = f"and tc.table_name = '{aTable}'" if (aTable) else ''
        CondType =  f"and tc.constraint_type = '{aType}'" if (aType) else ''

        Query = f'''
            select
                tc.table_name,
                kc.column_name,
                tc.constraint_type
            from
                information_schema.table_constraints as tc
            inner join
                information_schema.key_column_usage as kc
                on (tc.table_name = kc.table_name and
                    tc.table_schema = kc.table_schema and
                    tc.constraint_name = kc.constraint_name)
            where
                tc.table_schema = '{aSchema}'
                {CondTable}
                {CondType}
        '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetForeignKeys(self, aTable: str = '', aSchema: str = 'public') -> TDbSql:
        CondTable = f"and tc.table_name = '{aTable}'" if (aTable) else ''

        Query = f'''
            select distinct
                tc.table_name,
                kcu.column_name,
                ccu.table_name as table_name_f,
                ccu.column_name as column_name_f
            from
                information_schema.table_constraints as tc
            join
                information_schema.key_column_usage as kcu
                on (tc.constraint_name = kcu.constraint_name and
                    tc.constraint_schema = kcu.constraint_schema and
                    tc.table_name = kcu.table_name and
                    tc.table_schema = kcu.table_schema)
            join
                information_schema.constraint_column_usage as ccu
                on (ccu.constraint_name = tc.constraint_name and
                    ccu.constraint_schema = tc.constraint_schema)
            where
                tc.constraint_type = upper('foreign key')
                and tc.table_schema = '{aSchema}'
                {CondTable}
            '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetDbVersion(self, aSchema: str = 'public') -> TDbSql:
        Query = f'''
            select
                current_database() as db_name,
                version() as version,
                date_trunc('second', current_timestamp - pg_postmaster_start_time()) as uptime,
                pg_database_size(current_database()) as size,
                (
                    select
                        count(*) as count
                    from
                        information_schema.tables
                    where
                        (table_catalog = current_database())
                        and (table_schema = '{aSchema}')
                ) as tables
        '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetRoutines(self, aSchema: str = 'public') -> TDbSql:
        Query = f'''
            select
                routine_schema,
                routine_name,
                routine_type,
                data_type,
                is_deterministic
            from
                information_schema.routines
            where
                routine_schema = '{aSchema}'
        '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetTriggers(self) -> TDbSql:
        Query = '''
            select
                event_object_table as table_name,
                trigger_name,
            from
                information_schema.triggers
        '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetStat(self) -> TDbSql:
        Query = '''
            select
                t3.max_conn,
                t1.used as used_conn,
                t2.res_for_super,
                t3.max_conn - t1.used - t2.res_for_super as res_for_normal,
                t4.num_backends
            from
            (
                select count(*) as used
                from pg_stat_activity
            ) t1,
            (
                select setting::int as res_for_super
                from pg_settings
                where name = 'superuser_reserved_connections'
            ) t2,
            (
                select setting::int as max_conn
                from pg_settings
                where name = 'max_connections'
            ) t3,
            (
                select sum(numbackends) as num_backends
                from pg_stat_database
            ) t4
        '''
        return await TDbExecPool(self.Pool).Exec(Query)

    async def GetCount(self) -> TDbSql:
        Query = '''
            select
                relname as table,
                n_live_tup as records
            from
                pg_stat_user_tables
            order by
                n_live_tup desc
        '''
        return await TDbExecPool(self.Pool).Exec(Query)

def DTransaction(aMethod):
    async def Decor(self, aData, *_aArgs):
        async with self.Db.Pool.acquire() as Connect:
            async with Connect.cursor() as Cursor:
                Trans = await Cursor.begin()
                try:
                    Res = await aMethod(self, aData, Cursor)
                except (
                    errors.lookup(UNIQUE_VIOLATION),
                    errors.lookup(NOT_NULL_VIOLATION),
                    errors.lookup(UNDEFINED_COLUMN),
                    errors.lookup(FOREIGN_KEY_VIOLATION),
                    errors.lookup(SYNTAX_ERROR)
                ) as E:
                    Res = {'err': str(E).split('\n', maxsplit = 1)[0]}
                    Log.Print(1, 'x', 'DTransaction()', aE=E, aSkipEcho=['TEchoDb'])

                if (Res) and ('err' in Res):
                    #TransStat = await Connect.get_transaction_status()
                    #Res['trans'] = (TransStat != psycopg2.extensions.TRANSACTION_STATUS_INERROR)
                    await Trans.rollback()
                else:
                    await Trans.commit()
            return Res
    return Decor

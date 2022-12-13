import aiosqlite, asyncio
from Authentication import Auth
from Accounts import Account

class Database:       
    __slots__ = "db_name", "auth", "active_user"
    def __init__(self) -> None:
        self.db_name = "db.sqlite"
        self.auth = Auth()
        self.active_user = None
           
    async def generate_schemas(self):      
        queries = ("CREATE TABLE USER_ACCOUNTS(UUID VARCHAR, EMAIL VARCHAR, PASSWORD VARCHAR, FIRST_NAME VARCHAR, LAST_NAME VARCHAR);",
                "CREATE TABLE SECURITY(QUESTIONS VARCHAR);",
                "CREATE TABLE ACCOUNT_STORAGE(UUID VARCHAR, ACCOUNTS VARCHAR, KEY VARCHAR);")
        
        async with aiosqlite.connect(self.db_name) as db:
            tasks = [db.execute(query) for query in queries]
            await asyncio.gather(*tasks)
            await db.commit()
        del queries
            
    async def check_uuid(self, uuid: str) -> str:
        query = "SELECT UUID FROM USER_ACCOUNTS;"
        async with aiosqlite.connect(self.db_name) as db:
            taken_uuid = list(await db.execute_fetchall(query))
        while uuid in taken_uuid:
            uuid = self.auth.gen_uuid()
        return uuid            
    
    async def create_login_account(self, email: str, password: str, first_name: str, last_name: str):
            uuid = self.auth.gen_uuid()
            uuid = await self.check_uuid(uuid)
            params = (uuid, email, self.auth.hash(password), first_name, last_name)
            del password
            query = "INSERT INTO USER_ACCOUNTS VALUES (?, ?, ?, ?, ?);"
            async with aiosqlite.connect(self.db_name) as db:
                await db.execute(query, params)
                await db.commit()
                
    async def login(self, email: str, password: str) -> bool:
        query = "SELECT EMAIL, PASSWORD, UUID FROM USER_ACCOUNTS;"
        async with aiosqlite.connect(self.db_name) as db:
            accounts = await db.execute_fetchall(query)
        
        for account in accounts:
            if account[0] == email and account[1] == self.auth.hash(password):
                del password, query
                self.active_user = account[2]
                return True
        del password
        return False
    
    async def add_account(self, uname: str, pword: str, desc: str):
        query = "INSERT INTO ACCOUNT_STORAGE VALUES (?, ?, ?);"
        key = self.auth.generate_key()
        pword = self.auth.encrypt_str(pword, key)
        key = self.auth.encrypt_key(key)
        acc = Account(uname, pword, desc, key)
        params = (self.active_user, self.auth.dump(acc), key)
        
        async with aiosqlite.connect(self.db_name) as db:
            await db.execute(query, params)
            await db.commit()
            
    async def get_accounts(self):
        query = "SELECT * FROM ACCOUNT_STORAGE WHERE UUID = ?;"
        params = (self.active_user,)
        async with aiosqlite.connect(self.db_name) as db:
            accounts = await db.execute_fetchall(query, params)
        return [str(account) for account in accounts]
    
    async def main(self):
        #await self.generate_schemas()
        #await self.create_login_account("test@test.com", "test", "Tester", "Testy")
        print(await self.login("test@test.com", "test"))
        await self.add_account("test", "test", "this is a test")
        print(await self.get_accounts())    
    
    
if __name__ == "__main__":
    db = Database()
    asyncio.run(db.main())
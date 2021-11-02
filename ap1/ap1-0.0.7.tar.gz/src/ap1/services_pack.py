import traceback
import asyncio
import os

class Services:
    def __init__(self,app):
        self.app = app

        self.companies = {}
        self.search_locks = {}

    async def __directSearchCompany(self,company_name):
        try:
            params = {"keyword": company_name}
            async with self.app.session.get(self.app.config['search_company_api'],params=params,verify_ssl=False) as resp:
                if resp.status == 200:
                    data = (await resp.json())['data']
                    if not data:
                        not_fined_msg=f"Company was not found: {company_name}"
                        self.app.logger.warning(not_fined_msg)
                        return None

                    fined_msg = f"Company was found: {company_name}"
                    self.app.logger.info(fined_msg)
                    return data[0]

        except Exception as e:
            self.app.logger.warning(e,traceback.format_exc())

    async def searchCompany(self,company_name):
        if 'search_company_api' not in self.app.config:
            raise Exception("Add search_company_api to config file")

        if company_name in self.companies:
            return self.companies[company_name]
        elif company_name in self.search_locks:
            async with self.search_locks[company_name]:
                return self.companies[company_name]

        self.search_locks[company_name] = asyncio.Lock()
        async with self.search_locks[company_name]:
            self.companies[company_name] = await self.__directSearchCompany(company_name)

        del self.search_locks[company_name]
        return self.companies[company_name]

    async def loadFile(self, url:str,file_name:str, folder_dir:str=None) -> bool:
        try:
            if folder_dir is None:
                if 'base_path' not in self.app.config or 'folder' not in self.app.config:
                    raise Exception("Add both base_url and folder  to config file")

                folder_dir = os.path.join(self.app.config['base_path'], self.app.config['folder'])

            if not os.path.exists(folder_dir):
                os.mkdir(folder_dir)

            async with self.app.safe_requests.get(url) as resp:
                with open(file_name, 'wb') as f:
                    f.write(await resp.read())

            return True
        except:

            return False


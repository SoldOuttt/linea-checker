from web3 import Web3
from web3.eth import AsyncEth


class Client:
    def __init__(self):
        pass

    @staticmethod
    async def configure_web3(rpc: str, proxy: str):
        web3 = Web3(
            provider=Web3.AsyncHTTPProvider(
                endpoint_uri=rpc,
                request_kwargs={"proxy": proxy}
            ),
            modules={'eth': (AsyncEth,)},
            middlewares=[]
        )
        return web3

import asyncio
import os
import random
from typing import Tuple, Any
import openpyxl

from web3.contract import Contract

from client import Client

rpc = 'https://1rpc.io/linea'
contract_address = '0xDb75Db974B1F2bD3b5916d503036208064D18295'


async def has_name(contract, address) -> bool:
    result = await contract.functions.redeemed(address).call()
    return result

async def tmp(address) -> tuple[Any, bool]:
    module_dir = os.path.dirname(__file__)
    filename = module_dir + '/proxy.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        lines = file.readlines()

    for i in range(10):
        try:
            random_proxy = random.choice(lines).strip()
            web3 = await Client.configure_web3(rpc, random_proxy)
            break
        except Exception as e:
            if i == 9:
                raise Exception('proxy doesn\'t work')
    abi = [
        {
            "inputs": [
                {
                    "internalType": "address",
                    "name": "_address",
                    "type": "address"
                }
            ],
            "name": "redeemed",
            "outputs": [
                {
                    "internalType": "bool",
                    "name": "",
                    "type": "bool"
                }
            ],
            "stateMutability": "view",
            "type": "function"
        }
    ]
    contract: Contract = web3.eth.contract(abi=abi, address=contract_address)
    res = await has_name(contract, address)
    return address, res
async def main():
    module_dir = os.path.dirname(__file__)
    filename = module_dir + '/public_keys.txt'
    with open(filename, 'r', encoding='utf-8') as file:
        public_keys = file.readlines()
        public_keys = [key.strip() for key in public_keys]

    tasks = [tmp(key) for key in public_keys]
    results = await asyncio.gather(*tasks, return_exceptions=True)
    print(results)
    workbook = openpyxl.Workbook()
    sheet = workbook.active
    sheet["A1"] = "Address"
    sheet["B1"] = "Is named"

    for row_index, person in enumerate(results, start=2):
        sheet.cell(row=row_index, column=1).value = person[0]
        sheet.cell(row=row_index, column=2).value = 'YES' if person[1] else 'NO'
    workbook.save("people.xlsx")

if __name__ == "__main__":
    asyncio.run(main())

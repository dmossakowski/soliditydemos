from solcx import compile_standard, install_solc

import json
import numpy as np
import pandas as pd
from web3 import Web3
from web3.types import SignedTx
from dotenv import load_dotenv
import os

load_dotenv()

with open("./SimpleStorage.sol", "r") as file:
    simple_storage_file = file.read()

install_solc("0.6.0")

compiled_sol = compile_standard(
    {
        "language": "Solidity",
        "sources": {"SimpleStorage.sol": {"content": simple_storage_file}},
        "settings": {
            "outputSelection": {
                "*": {"*": ["abi", "metadata", "evm.bytecode", "evm.sourceMap"]}
            }
        },
    },
    solc_version="0.6.0",
)

aa = np.array([1, 2, 2])


with open("compiled.json", "w") as file:
    json.dump(compiled_sol, file)

bc = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["evm"]["bytecode"][
    "object"
]

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER")))


# chainId = 1337 #ganache
chainId = 4  # infura
myAddress = os.getenv("MY_ADDRESS")

private_key = os.getenv("PRIVATE_KEY")
print(private_key)
SimpleStorage = w3.eth.contract(abi=abi, bytecode=bc)

nonce = w3.eth.getTransactionCount(myAddress)

print(nonce)

transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chainId, "from": myAddress, "nonce": nonce + 1}
)

print(transaction)

signedTx = w3.eth.account.sign_transaction(transaction, private_key)

tx_has = w3.eth.send_raw_transaction(signedTx.rawTransaction)

tx_receipht = w3.eth.wait_for_transaction_receipt(tx_has)

simple_storage = w3.eth.contract(address=tx_receipht.contractAddress, abi=abi)

print(simple_storage.functions.getAmount().call())

# print(simple_storage.functions.store(14).call())

storeTransaction = simple_storage.functions.store(15).buildTransaction(
    {"chainId": chainId, "from": myAddress, "nonce": nonce + 1}
)


signed_store_tx = w3.eth.account.sign_transaction(
    storeTransaction, private_key=private_key
)

print("transaction sent.. waiting for confirmation..")
send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)
tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

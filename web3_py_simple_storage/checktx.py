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


# w3 = Web3(Web3.HTTPProvider("HTTP://127.0.0.1:8545"))

w3 = Web3(
    Web3.HTTPProvider("https://rinkeby.infura.io/v3/3158e535f5e942b6a91ef815f31facc8")
)

# chainId = 1337 #ganache
chainId = 4  # infura
# myAddress = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
myAddress = "0xf4b6066299a7D0Db55976d6EA81b6eD613D72650"  # metamask account1

private_key = os.getenv("PRIVATE_KEY")

SimpleStorage = w3.eth.contract(abi=abi, bytecode=bc)

nonce = w3.eth.getTransactionCount(myAddress)

print("nonce=", nonce)

# gasPrice = w3.eth.gasPrice * 1.40

tx = w3.eth.getTransaction(
    "0x22e20f33ca12028ec99c922e8ddc4b31de07faa84427a71f97ba013eb60520a3"
)

print(tx)

txgasprice = tx["gasPrice"]

print(txgasprice)

gasprice10 = txgasprice * 1.1

print(
    "txgasprice=", txgasprice, " tx gasprice=", txgasprice, " +10 gasprice=", gasprice10
)


transaction = SimpleStorage.constructor().buildTransaction(
    {"chainId": chainId, "from": myAddress, "nonce": nonce, "gasPrice": txgasprice}
)

# print(transaction)

signedTx = w3.eth.account.sign_transaction(transaction, private_key)


tx_has = w3.eth.send_raw_transaction(signedTx.rawTransaction)

tx_receipt = w3.eth.wait_for_transaction_receipt(tx_has)

simple_storage = w3.eth.contract(address=tx_receipt.contractAddress, abi=abi)

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

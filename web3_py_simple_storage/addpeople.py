import dotenv
from solcx import compile_standard, install_solc

import json
import numpy as np
import pandas as pd
from web3 import Web3
from web3.types import SignedTx
from dotenv import load_dotenv
import os

load_dotenv()


compiled_sol = None
with open("compiled.json", "r") as file:
    compiled_sol = json.load(file)

abi = compiled_sol["contracts"]["SimpleStorage.sol"]["SimpleStorage"]["abi"]


w3 = Web3(Web3.HTTPProvider(os.getenv("WEB3_PROVIDER")))

res = w3.isConnected()

print(res)

# chainId = 1337 #ganache
chainId = 4  # infura
# myAddress = "0x90F8bf6A479f320ead074411a4B0e7944Ea8c9C1"
myAddress = os.getenv("MY_ADDRESS")  # metamask account1

private_key = os.getenv("PRIVATE_KEY")


nonce = w3.eth.getTransactionCount(myAddress)

print("nonce=", nonce)

# gasPrice = w3.eth.gasPrice * 1.40
simplestoragecontractid = "0x796d876110bC4D5b12c7162C2F1a8Cb9C6bc4439"


balance = w3.eth.getBalance(myAddress)

print(balance)

nonce = w3.eth.getTransactionCount(myAddress)
print("nonce=", nonce)

simplestoragecontractid = "0x796d876110bC4D5b12c7162C2F1a8Cb9C6bc4439"
simplestorage = w3.eth.contract(address=simplestoragecontractid, abi=abi)

print("calling retrieve3")
response = simplestorage.functions.retrieve3().call()

print(response)

print("calling people 0")
response = simplestorage.functions.people(1).call()

print(response)

print(w3.clientVersion)

# tx_hash = simplestorage.functions.store(20).transact()


# estimate = w3.eth.estimateGas(
#    {"to": simplestoragecontractid, "from": myAddress, "value": 145}
# )
# print("gas estimate = " + estimate)

# web3_filter = w3.eth.filter("pending")

# transaction_hashes = w3.eth.getFilterChanges(web3_filter.filter_id)

# for tx in transaction_hashes:
#    Datatx = w3.eth.getTransaction(tx)
#    print(Datatx)


def find_transaction(id):
    tx = w3.eth.get_transaction(id)

    print(tx)


def increase_gas():

    print(" increasing gas ")

    gasPrice = 1215467640
    gas = 1000000

    storeTransaction = simplestorage.functions.store(16).buildTransaction(
        {
            "chainId": chainId,
            "from": myAddress,
            "nonce": nonce + 1,
            "gas": gas,
            "gasPrice": gasPrice,
        }
    )

    print(storeTransaction)

    signed_store_tx = w3.eth.account.sign_transaction(
        storeTransaction, private_key=private_key
    )

    print("transaction signed.. sending..")

    send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)

    print("transaction sent.. waiting for confirmation..")

    tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

    print("00000000")

    storeTransaction = simplestorage.functions.store(15).buildTransaction(
        {"chainId": chainId, "from": myAddress, "nonce": nonce + 1}
    )

    signed_store_tx = w3.eth.account.sign_transaction(
        storeTransaction, private_key=private_key
    )

    print(signed_store_tx)
    print("transaction sent.. waiting for confirmation..")
    send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)

    print(send_store_tx)

    tx_receipt = w3.eth.wait_for_transaction_receipt(send_store_tx)

    print("------")

    storeTransaction = simplestorage.functions.store(15).buildTransaction(
        {"chainId": chainId, "from": myAddress, "nonce": nonce + 1}
    )

    signed_store_tx = w3.eth.account.sign_transaction(
        storeTransaction, private_key=private_key
    )

    send_store_tx = w3.eth.send_raw_transaction(signed_store_tx.rawTransaction)

    print(storeTransaction)
    print("transaction sent.. waiting for confirmation..")

    tx_receipt = w3.eth.wait_for_transaction_receipt(storeTransaction)


# find_transaction("0x4cce375f57063ff84f129a2f5d0aca2745d01b96e0e8e4f50c2b8bd18b9b4b54")
increase_gas()

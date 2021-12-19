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

myAddress = os.getenv("MY_ADDRESS")

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

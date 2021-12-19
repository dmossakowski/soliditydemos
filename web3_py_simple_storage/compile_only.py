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

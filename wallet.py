# Import dependencies
import subprocess
import json
import os
# Load and set environment variables
from dotenv import load_dotenv
from constants import *
from pprint import pprint
from pathlib import Path
from getpass import getpass

load_dotenv()
mnemonic = os.getenv("mnemonic")
print(mnemonic)
# Import constants.py and necessary functions from bit and web3
from web3 import Web3, middleware, Account
from web3.middleware import geth_poa_middleware


from web3.gas_strategies.time_based import medium_gas_price_strategy
# from eth_account import Account

from bit import wif_to_key
from bit import PrivateKeyTestnet
from bit.network import NetworkAPI

w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:7545"))
w3.middleware_onion.inject(geth_poa_middleware, layer=0)
w3.eth.setGasPriceStrategy(medium_gas_price_strategy)


# Enter private key of the bip39 address
# key = wif_to_key("L5UYexkSVa9vroE2usKfzosuzJQdtqefFDcfdZkapdL1SoUKMYxU")
key = wif_to_key("cVPmfCd3N7N3R4aHpQpdrS1Kd1YjP25YHdc2oG5jRh47Nith2H1p")

print(key.get_balance('btc'))
print(key.get_unspents())
print(key)

# Use the subprocess library to create a shell command that calls the ./derive script from Python. Make sure to properly wait for the process. Windows Users may need to prepend the php command in front of ./derive like so:
# php ./derive --mnemonic --coin --numderive --format=json
#Mnemonic () must be set from an environment variable, or default to a test mnemonic
#Coin ()
#Numderive (--numderive) to set number of child keys generated
#Format (--format=json) to parse the output into a JSON object using json.loads(output)
 
# Create a function called `derive_wallets`
def derive_wallets(Mnemonic, Coin, Numderive):
    command = f'php ./derive -g --mnemonic="{Mnemonic}" --cols=all --coin={Coin} --numderive={Numderive} --format=json'
    p = subprocess.Popen(command, stdout=subprocess.PIPE, shell=True)
    output, err = p.communicate()
    p_status = p.wait()
    return json.loads(output)






# Create a function called `priv_key_to_account` that converts privkey strings to account objects.
def priv_key_to_account(coin, priv_key):

    if coin == ETH:
        return Account.privateKeyToAccount(priv_key)
    elif coin == BTCTEST:
        return PrivateKeyTestnet(priv_key)


# Create a function called `create_tx` that creates an unsigned transaction appropriate metadata.
def create_tx(coin, account, recipient, amount):
    
    if coin == ETH:
        eth_value = w3.toWei(amount, "ether")

        gasEstimate = w3.eth.estimateGas(
            {"from": account, "to": recipient, "amount": value}
        )
        return {
            "from": account.address,
            "to": recipient,
            "value": eth_value,
            "gasPrice": w3.eth.gasPrice,
            "gas": gasEstimate,
            "nonce": w3.eth.getTransactionCount(account.address),
            "chainID": w3.eth.chain_id,
            }
    if coin == BTCTEST:
        return PrivateKeyTestnet.prepare_transaction(account.address, [(recipient, amount, BTC)])

# Create a function called `send_tx` that calls `create_tx`, signs and sends the transaction.
def send_tx(coin, account, recipient, amount):
    # sender_account = priv_key_to_account(coins[0]["privkey"], "BTCTest")
    if coin == ETH:
        tx = create_tx(coin, account.address, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        return w3.eth.sendRawTransaction(signed_tx.rawTransaction)

    if coin == BTCTEST:
        tx = create_tx(coin, account, recipient, amount)
        signed_tx = account.sign_transaction(tx)
        #print(tx)
        #print(signed_tx)
        return NetworkAPI.broadcast_tx_testnet(signed_tx)

   
    

    

# Create a dictionary object called coins to store the output from `derive_wallets`. 

coins = {
    BTC: derive_wallets(mnemonic,BTC,3),
    ETH:derive_wallets(mnemonic,ETH,3),
    BTCTEST: derive_wallets(mnemonic,BTCTEST,3)
}
#print(coins)
pprint(coins)
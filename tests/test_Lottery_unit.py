from brownie import Lottery, accounts, config, network
from web3 import Web3
from scripts.deploy_Lottery import deploy_lottery


def test_get_price_fee():
    

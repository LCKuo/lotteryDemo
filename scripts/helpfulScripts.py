from brownie import network, accounts, config
from web3 import Web3
from brownie import MockV3Aggregator, Contract, VRFCoordinatorMock, LinkToken

DECIMAL = 8
STARTPRICE = 2000

FORKED_LOACL_ENVIROMENT = ["LC"]
LOCAL_BLOCKCHAIN_ENVIROMENT = ["development"]


def getAccount(index=None, id=None):
    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENT
        or network.show_active() in FORKED_LOACL_ENVIROMENT
    ):
        return accounts[0]
    else:
        return config["wallet"]["from_key"]


contract_to_mock = {
    "eth_usd_price_feed": MockV3Aggregator,
    "vrf_coordinator": VRFCoordinatorMock,
    "link_token": LinkToken,
}


def get_contract(contract_name):
    contract_type = contract_to_mock[contract_name]
    if network.show_active() in LOCAL_BLOCKCHAIN_ENVIROMENT:
        if len(contract_type) <= 0:
            deploy_Mock()
        contract = contract_type[-1]
        # MockV3Aggregator[-1]
    else:
        contract_address = config["networks"][network.show_active()][contract_name]
        # for this demo ,it deploy to LC-network
        contract = Contract.from_abi(
            contract_type.name, contract_address, contract_type.abi
        )
    return contract


def deploy_Mock():
    account = getAccount()
    mock_price_feed = MockV3Aggregator.deploy(
        DECIMAL, Web3.toWei(STARTPRICE, "ether"), {"from": account}
    )
    link_token = LinkToken.deploy({"from": account})
    VRFCoordinatorMock.deploy(link_token.address, {"from": account})
    print("Mock deployed!")


def fund_with_link(
    contract_address, account=None, link_token=None, amount=100000000000000000
):
    account = account if account else getAccount()
    link_token = link_token if link_token else get_contract("link_token")
    tx = link_token.transfer(contract_address, amount, {"from": account})
    tx.wait(1)
    print("Contract funded")
    return tx

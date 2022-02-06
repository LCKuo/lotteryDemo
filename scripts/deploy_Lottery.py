from os import access
from brownie import Lottery, network, config
from scripts.helpfulScripts import getAccount, get_contract, fund_with_link
import time


def deploy_lottery():
    account = getAccount()
    """address _priceFeedAddress,
        address _VRFCordinator,
        address _link,
        uint256 _fee,
        bytes32 _keyhash"""
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrf_coordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )


def startLottery():
    account = getAccount()
    lottery = Lottery[-1]
    starting_tx = lottery.startLottery({"from": account})
    starting_tx.wait(1)
    print("Lottery started")


def enter_lottery():
    account = getAccount()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    print(f"Enterance Fee : {value}")
    # 0.02500000
    tx = lottery.ENTER({"from": account, "value": value})
    tx.wait(1)
    print("You have entered lottery")


def end_lottery():
    account = getAccount()
    lottery = Lottery[-1]
    tx = fund_with_link(lottery.address)
    tx.wait(1)
    ending_tx = lottery.endLottery({"from": account})
    ending_tx.wait(1)
    time.sleep(60)
    print(f"{lottery.recentWinner()} is the winner")


def main():
    print(network.show_active())
    deploy_lottery()
    startLottery()
    enter_lottery()
    end_lottery()

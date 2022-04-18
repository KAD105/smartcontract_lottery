from brownie import Lottery, network, config
from scripts.helpful_scripts import get_contract, get_account


def deploy_lottery():
    account = get_account()
    lottery = Lottery.deploy(
        get_contract("eth_usd_price_feed").address,
        get_contract("vrfCoordinator").address,
        get_contract("link_token").address,
        config["networks"][network.show_active()]["fee"],
        config["networks"][network.show_active()]["keyhash"],
        {"from": account},
        publish_source=config["networks"][network.show_active()].get("verify", False),
    )

    print("Deployed lottery!")
    return lottery


def start_lottery():
    account = get_account()
    lottery = Lottery[-1]
    tx1 = lottery.startLottery({"from": account})
    tx1.wait(1)
    print("The start of Lottery!")


def enter_lottery():
    account = get_account()
    lottery = Lottery[-1]
    value = lottery.getEntranceFee() + 100000000
    tx2 = lottery.enter({"from": account, "value": value})
    tx2.wait(1)
    print("Now you have entered the lottery!")


def end_lottery():
    account = get_account()
    lottery = Lottery[-1]
    lottery.endLottery()


def main():
    deploy_lottery()
    start_lottery()
    enter_lottery()
    end_lottery()

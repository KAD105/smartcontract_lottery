from brownie import Lottery, accounts


def deploy_lottory():
    account = accounts[0]
    lottory = Lottery.deploy({"from": account})


def main():
    deploy_lottory()

from pickle import NONE
from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_ENVIRONMETN = ["development", "ganache-local"]
FORKED_LOCAL_ENVIRIONMENT = ["mainnet-fork", "mainnet-fork-dev"]


def get_account(index=None, id=None):

    if index:
        return accounts[index]
    if id:
        return accounts.load(id)
    if (
        network.show_active() in LOCAL_BLOCKCHAIN_ENVIRONMETN
        or network.show_active() in FORKED_LOCAL_ENVIRIONMENT
    ):
        return accounts[0]
    return accounts.add(config["wallets"]["from_key"])

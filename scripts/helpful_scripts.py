from brownie import network, accounts, config

LOCAL_BLOCKCHAIN_ENVIRONMETN = ["development", "ganache-local"]


def get_account():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMETN:
        return accounts[0]
    else:
        return accounts.add(config["wallets"]["from_key"])

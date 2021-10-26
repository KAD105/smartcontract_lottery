from brownie import accounts, Lottery, network, config
from web3 import Web3

#We expect to get 0.012(current 50 / ethereum) eth as our result.
def test_get_entrance_fee():
    account = accounts[0]
    lottery = Lottery.deploy(
        config["networks"] [network.show_active()] ["eth_usd_price_feed"],
        {"from": account},
    )

    # assert lottery.getEnteranceFee() > Web3.toWei(0.011, "ether")
    # assert lottery.getEnteranceFee() < Web3.toWei(0.013, "ether")
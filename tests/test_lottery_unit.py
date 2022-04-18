from brownie import network, exceptions
from scripts.helpful_scripts import (
    LOCAL_BLOCKCHAIN_ENVIRONMETN,
    get_account,
    fund_with_link,
    get_contract,
)
from scripts.deploy_lottery import deploy_lottery
from web3 import Web3
import pytest

# We expect to get 0.025(current 50 / ethereum) eth as our result.
def test_get_entrance_fee():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMETN:
        pytest.skip()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    expected_entrance_fee = Web3.toWei(0.025, "ether")
    assert entrance_fee == expected_entrance_fee


def test_cant_enter_unless_strated():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMETN:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    with pytest.raises(exceptions.VirtualMachineError):
        lottery.enter({"from": account, "value": entrance_fee})


def test_can_start_and_enter_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMETN:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()
    lottery.startLottery()
    entrance_fee = lottery.getEntranceFee()
    lottery.enter({"from": account, "value": entrance_fee})
    assert lottery.players(0) == account


def test_end_lottery():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMETN:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    lottery.startLottery()
    lottery.enter({"from": account, "value": entrance_fee})
    fund_with_link(lottery.address)
    lottery.endLottery({"from": account})
    assert lottery.lottery_state() == 2


def test_can_select_winner_properly():
    if network.show_active() not in LOCAL_BLOCKCHAIN_ENVIRONMETN:
        pytest.skip()
    account = get_account()
    lottery = deploy_lottery()
    entrance_fee = lottery.getEntranceFee()
    lottery.startLottery({"from": account})
    lottery.enter({"from": account, "value": entrance_fee})
    lottery.enter({"from": get_account(index=1), "value": entrance_fee})
    lottery.enter({"from": get_account(index=2), "value": entrance_fee})
    starting_balance_of_lottery = lottery.balance()
    starting_balance_of_account = account.balance()
    fund_with_link(lottery)
    end_lottory_deployed = lottery.endLottery({"from": account})
    request_id = end_lottory_deployed.events["requestedRandomness"]["requestId"]
    our_given_random_Nr = 777
    get_contract("vrfCoordinator").callBackWithRandomness(
        request_id, our_given_random_Nr, lottery.address, {"from": account}
    )
    # 777 % 3 = 0. it means that out of 3 participants our account
    # which is index=0 must be the winner

    assert lottery.recentWinner() == account
    assert lottery.balance() == 0
    assert (
        account.balance() == starting_balance_of_lottery + starting_balance_of_account
    )

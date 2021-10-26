

// SPDX-License-Identifier: MIT

pragma solidity ^0.6.6;

import "@chainlink/contracts/src/v0.6/interfaces/AggregatorV3Interface.sol";
import "@openzeppelin/contracts/access/Ownable.sol";


contract Lottery is Ownable{

   address payable[] public  palyers;
   uint256 public usdEntryFee;
   AggregatorV3Interface internal ethUsdPriceFeed;

   enum LOTTERY_STATE{
       OPEN,
       CLOSE,
       CALCULATING_STATE
   }
   // LOTTERY_STATE is a type. 
   // OPEN, CLOSE, CALCULATING_STATE = 0,1,2

   LOTTERY_STATE public lottery_state;

    constructor(address _priceFeedAddress) public{
        usdEntryFee = 50 * (10**18);
        ethUsdPriceFeed = AggregatorV3Interface(_priceFeedAddress);
        lottery_state = LOTTERY_STATE.CLOSE;
        // We can also set it close like this: lottery_state = 1
       
    }
    function enter() public payable{
        // 50$ minimum
        require(msg.value >= getEnteranceFee(), "Not enough Eth!");
        require(lottery_state == LOTTERY_STATE.OPEN);
        palyers.push(msg.sender);
       
    }
    function getEnteranceFee() public view returns(uint256){
        (, int256 price, , , ) = ethUsdPriceFeed.latestRoundData();
        uint256 adjustedPrice = uint256(price) * 10**10; //18 decimals
        uint256 costToEnter = (usdEntryFee * 10**18) / adjustedPrice;
        return costToEnter;
    }
    function startLottery() public onlyOwner {
        require(lottery_state == LOTTERY_STATE.CLOSE, "Can't start a lottery yet!");
        require(lottery_state == LOTTERY_STATE.OPEN);
    }
    function endLottery() public{}
}


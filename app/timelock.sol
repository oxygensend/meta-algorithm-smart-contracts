pragma solidity 0.5.0;


contract TimeLock {

    mapping(address => uint) public balances;
    mapping(address => uint) public lockTime;

    function deposit() public payable {
        balances[msg.sender] += msg.value;
        lockTime[msg.sender] = now + 1 weeks;
    }

    function increaseLockTime(uint _secondsToIncrease) public {
        lockTime[msg.sender] += _secondsToIncrease;
    }

    function withdraw() public {
        require(balances[msg.sender] > 0);
        require(now > lockTime[msg.sender]);
        balances[msg.sender] = 0;
        msg.sender.transfer(balances[msg.sender]);
    }

    function echidna_test_balance()  public returns (bool){
        return (balances[address(0xcafe)] == 0);
    }

    function echidna_test_lockTime()  public returns (bool){
        return (lockTime[address(0xcafe)] == 0);
    }
}
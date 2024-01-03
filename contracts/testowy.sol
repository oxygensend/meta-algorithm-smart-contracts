// SPDX-License-Identifier: MIT
pragma solidity ^0.8.2;

interface ICaller {
    function thisIsFine() external;
    function reentrancy() external;
    function callUserAddress(address addr) external;
    function callStoredAddress() external;
    function setStoredAddress(address addr) external;
}

contract Caller is ICaller {
    address public immutable FIXED_ADDRESS;
    address public storedAddress;

    uint256 private _stateVar;

    constructor(address addr) public {
        require(addr != address(0), "Caller: address should not be 0");
        FIXED_ADDRESS = addr;
    }

    function thisIsFine() override external {
        FIXED_ADDRESS.call("");
    }

    function reentrancy() override external {
        _stateVar = 0;
        FIXED_ADDRESS.call("");
    }

    function callUserAddress(address addr) override external {
        require(addr != address(0), "Caller: address should not be 0");
        addr.call("");
    }

    function callStoredAddress() override external {
        storedAddress.call("");
    }

    function setStoredAddress(address addr) override external {
        require(addr != address(0), "Caller: address should not be 0");
        storedAddress = addr;
    }
}

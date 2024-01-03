pragma solidity ^0.8.9;

contract Caller {
    address public fixed_address;
    address public stored_address;

    uint256 statevar;

    constructor(address addr) {
        fixed_address = addr;
    }

    function thisisfine() public {
        fixed_address.call("");
    }

    function reentrancy() public {
        if (fixed_address.call("")) {
            statevar = 0;
        }
    }

    function calluseraddress(address addr) public {
        if (addr != address(0)) {
            addr.call("");
        }
    }

    function callstoredaddress() public {
        if (stored_address != address(0)) {
            stored_address.call("");
        }
    }

    function setstoredaddress(address addr) public {
        stored_address = addr;
    }
}
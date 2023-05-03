// get artifact
const PatentManager = artifacts.require("PatentManager");
const web3 = require('web3');

contract("PatentManager", (accounts) => {

    let myContract;

    before(async () => {
        myContract = await PatentManager.deployed();
    });

    // getPatent should return data given given upon addPatent call
    it("should add a new Patent and retrieve the correct owner", async () => {

        const expectedOwner = accounts[0];
        const testHash = '0x7465737400000000000000000000000000000000000000000000000000000000';
        const valueInEth = web3.utils.toWei('0.2', 'ether');

        // add test Patent
        await myContract.addPatent(testHash, expectedOwner, { value: valueInEth });

        // retrieve owner
        const gotOwner = await myContract.getPatent(testHash);

        assert.equal(gotOwner, expectedOwner, 'the retrieved owner should match the one set upon Patent insertion');

    });
});




























//
// get artifact
const PatentManager = artifacts.require("PatentManager");
const truffleAssert = require("truffle-assertions");
const Web3 = require('web3');
const web3 = new Web3();

contract("PatentManager", (accounts) => {

    let myContract; let result; let result1; let testHash; let expectedOwner; let newHash;

    before(async () => {
        myContract = await PatentManager.deployed();
    });

    // getPatent should return the owner set upon newPatent call
    it("should add a new Patent and retrieve the correct owner", async () => {
        expectedOwner = accounts[0];
        testHash = '0x7465737400000000000000000000000000000000000000000000000000000000';
        const valueInEth = Web3.utils.toWei('0.2', 'ether');

        // add test Patent
        result = await myContract.addPatent(testHash, expectedOwner, { value: valueInEth });

        // retrieve owner
        const gotOwner = await myContract.getPatent.call(testHash);

        assert.equal(gotOwner, expectedOwner, 'the retrieved owner should match the one set upon Patent insertion');

    });

    // check event newPatent has been emitted
    it("should correctly emit event after patent upload", () => {
        truffleAssert.eventEmitted(result, "newPatent", (event) => {
            return (event.id.toNumber() === 1 && event.hash === testHash && event.owner === expectedOwner);
        }, 'newPatent event should have been emitted with correct parameters');
    });

    // changePatent should modify the hash associated to the Patent, when retrieving the owner with getPatent it should
    // return the same owner that uploaded the patent (if not changed properly, the new hash will return the empty address)
    it("should correctly modify the hash of the patent", async () => {
        newHash = '0x8465737400000000000000000000000000000000000000000000000000000000';
        const valueInEth = web3.utils.toWei('0.05', 'ether');

        // change hash aassociated to the Patent
        result1 = await myContract.changePatent(newHash, 1, { value: valueInEth });

        // should retrieve the same owner as previously
        const gotOwner = await myContract.getPatent(newHash);

        assert.notEqual(gotOwner, web3.eth.accounts.null, 'the modifyed hash should have been mapped to the previous owner');
    });

    // check event patentChanged has been emitted
    it("should correctly emit event after hash edit", () => {
        truffleAssert.eventEmitted(result1, "patentChanged", (event) => {
            return (event.id.toNumber() === 1 && event.oldHash === testHash && event.newHash === newHash);
        }, 'patentChanged event should have been emitted with correct parameters');
    });



});




























//
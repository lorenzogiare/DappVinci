// get artifact of smartcontract
const PatentManager = artifacts.require("./PatentManager.sol");

// this is to deploy on the blockchain
module.exports = function (deployer) {
    deployer.deploy(PatentManager);
};
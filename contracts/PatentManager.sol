// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

contract PatentManager {
    
    struct Patent {
        uint256 id;     // id of patent        
        bytes32 hash;   // Hash of the data
        address owner;  // Owner's account
    }

    uint256 internal patentCount = 0;

    mapping(uint256 => Patent) private patents;
    mapping(bytes32 => address) private patentOwners;

    // event: new patent added
    event newPatent(uint256 id, bytes32 hash, address owner);

    // event: patent hash changed
    event patentChanged(uint256 id, bytes32 oldHash, bytes32 newHash);

    /** 
     * @dev add new Patent, caller is required to pay 0.2 eth
     * @param _hash hash of the data
     * @param _owner owner of the patent (might be different from the caller)
     */
    function addPatent(bytes32 _hash, address _owner) public payable {

        uint256 costToAdd = 0.2 ether;
        require(
            patentOwners[_hash] == address(0x0),
            "this hash of data has already been injected"
        );
        require(
            msg.value == costToAdd,
            "adding a Patent requires paying 0.2 eth!"
        );

        // increment id
        patentCount++;   
        
        // update patents map
        patents[patentCount] = Patent({
            id: patentCount,
            hash: _hash,
            owner: _owner
        });

        // update owners map
        patentOwners[_hash] = _owner;

        // emit event 
        emit newPatent(patentCount, _hash, _owner);
    }

    /** 
     * @dev check if hash of a patent exists
     * @param _hash hash of the data
     * @return return owner of the patent (if hash exists), null address otherwise (0x0)
     */
    function getPatent(bytes32 _hash) public view returns (address){
        return patentOwners[_hash];
    }

    /** 
     * @dev change hash associated to a patent, only the owner has access
     * @param _newHash hash of the modified data
     * @param _id id of the patent of interest
     */
    function changePatent(bytes32 _newHash, uint256 _id) public payable {

        uint256 costToMod = 0.05 ether;
        require(
            msg.sender == patents[_id].owner,
            "only the owner of the patent can modify the hash"
        );
        require(
            msg.value == costToMod,
            "modifying a Patent requires paying 0.05 eth!"
        );

        bytes32 _oldHash = patents[_id].hash;

        // update owners map
        patentOwners[_oldHash] = address(0x0);  // old hash to owner is cleared
        patentOwners[_newHash] = msg.sender;    // new hash to owner is set

        // update patents map
        patents[_id].hash = _newHash;    

        // emit event
        emit patentChanged(_id, _oldHash, _newHash);       
    }
}
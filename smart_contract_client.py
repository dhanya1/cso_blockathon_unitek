import json
from web3 import Web3, HTTPProvider
from configparser import ConfigParser

config = ConfigParser()
config.read('config.ini')


def smart_contract_client(data=None, action=None, txn_id=None):
    # Config
    contract_address = config['etherum']['contract_address']
    wallet_private_key = config['etherum']['wallet_private_key']
    wallet_address = config['etherum']['wallet_address']
    w3 = Web3(HTTPProvider(config['etherum']['url']))
    contract_address = w3.toChecksumAddress(contract_address)
    w3.eth.DefaultAccount =config['etherum']['account']
    # Contract setup
    with open('abi.json') as f:
        json_abi = json.load(f)
    if action.lower() == 'store':
        contract = w3.eth.contract(address=contract_address,
                                   abi=json_abi["abi"])
        nonce = w3.eth.getTransactionCount(wallet_address)
        txn_dict = {
            'data': data,
            'gas': 2000000,
            'nonce': nonce,
            'chainId': 3,
            'gasPrice': w3.toWei('4', 'gwei')
        }
        signed_txn = w3.eth.account.signTransaction(txn_dict,
                                                    wallet_private_key)
        txn_hash_1 = w3.eth.sendRawTransaction(signed_txn.rawTransaction)
        w3.eth.waitForTransactionReceipt(txn_hash_1)
        txn_hash = w3.eth.getTransactionReceipt(txn_hash_1)
        print(txn_hash)
        return txn_hash['transactionHash'].hex()
    if action.lower() == 'verify':
        result = w3.eth.getTransaction(txn_id)
        if result is None:
           return 0
        string_on_transaction = result['input']
        verification_string = '0x'+ data
        if string_on_transaction == verification_string:
            return 1
        else:
            return 0


if __name__ == "__main__":
    smart_contract_client(data="blahhhjhh", action="store")
    """
    smart_contract_client(
        data="blah", action="verify",
        txn_id="0x9d53b42a7230be1875483eaf1762414bbba3422d49f386459fc531b70992b4cf")
    """

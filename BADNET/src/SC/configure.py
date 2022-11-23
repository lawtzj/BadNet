import sys
import binascii
from ecies.utils import generate_key
from eth_account import Account

from web3 import Web3, HTTPProvider
import contract_abi


contract_address = "0xD6bfD430134759a0deebF58da785c116B524A968"
web3 = Web3(HTTPProvider("https://sepolia.infura.io/v3/67631e6ab6fc44e49915da74fd957740"))
contract_instance = web3.eth.contract(address=contract_address, abi=contract_abi.abi)


def create_account(path):
    secp_k = generate_key()
    wallet_private_key = binascii.hexlify(secp_k.secret).decode('utf-8')
    public_key = secp_k.public_key.format(True)
    wallet_public_key = binascii.hexlify(public_key).decode('utf-8')
    account = Account.from_key(wallet_private_key)
    wallet_addr = account.address

    with open(path, mode='w') as filename:
        filename.write('contract_address = "' + contract_address + '"' + '\n\n')
        filename.write('wallet_addr = "' + wallet_addr + '"' + '\n')
        filename.write('wallet_public_key = "' + wallet_public_key + '"' + '\n')
        filename.write('wallet_private_key = "' + wallet_private_key + '"' + '\n')
    print(wallet_addr)


def relay_get_upload_period():
    return contract_instance.functions.relay_get_upload_period().call()


if __name__ == '__main__':
    path = '/usr/local/BADNET-V3-relay/'
    create_account(path + 'SC/account.py')
    """
    RelayUploadPeriod = relay_get_upload_period()
    with open(path + 'BADNET.relay', mode='a') as filename:
        filename.write('\n' + 'RelayUploadPeriod ' + str(RelayUploadPeriod))
    """

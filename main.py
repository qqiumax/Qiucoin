from hashlib import sha512
from json import dumps
import time
from flask import Flask
import os

class Block(object):
    def __init__(self, index, transactions, timestamp, previous_hash, nonce=0):
        self.index = index
        self.transactions = transactions
        self.timestamp = timestamp

        self.previous_hash = previous_hash
        self.nonce = nonce

    def hash(self):
        block_string = dumps(self.__dict__, sort_keys=True)
        return sha512(block_string.encode()).hexdigest()


class Blockchain():
    def __init__(self):
        self.unconfirmed_transactions = []
        self.chain = []
        self.create_genesis_block()

    def create_genesis_block(self):
        genesis_block = Block(0, [], str(time.time()), "0")
        genesis_block.hash = genesis_block.hash()
        self.chain.append(genesis_block)

    @property
    def last_block(self):
        return self.chain[-1]


    difficulty = 2


def proof_of_work(block):
    block.nonce = 0
    computed_hash = block.hash()
    while not computed_hash.startswith('0' * Blockchain.difficulty):
        block.nonce += 1
        computed_hash = block.hash()
    return computed_hash


def add_block(self, block, proof):
    previous_hash = self.last_block.hash
    if previous_hash != block.previous_hash:
        return False
    if not self.is_valid_proof(block, proof):
        return False
    block.hash = proof
    self.chain.append(block)
    return True


def is_valid_proof(block, block_hash):
    return (block_hash.startswith('0' * Blockchain.difficulty) and
            block_hash == block.hash())


def add_new_transaction(self, transaction):
    self.unconfirmed_transactions.append(transaction)


def mine(self):
    if not self.unconfirmed_transactions:
        return False

    last_block = self.last_block

    new_block = Block(index=last_block.index + 1, transactions=self.unconfirmed_transactions, timestamp=time.time(), previous_hash=last_block.hash)

    proof = self.proof_of_work(new_block)
    self.add_block(new_block, proof)
    self.unconfirmed_transactions = []
    return new_block.index


app = Flask(__name__)

blockchain = Blockchain()


@app.route('/', methods=['GET'])
def get_chain():
    chain_data = []
    for block in blockchain.chain:
        chain_data.append(block.__dict__)



    return dumps({"length": str(len(chain_data)), "chain": chain_data})


app.run(debug=True, port=8000)

yourNgrokServerUrl = "bf31bf366cd6-2620527287896722552.ngrok-free.app"
os.system("ngrok http --domain="+yourNgrokServerUrl+'8000')
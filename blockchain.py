from hashlib import sha512
from json import dumps
import time
from flask import Flask


# This file is able to be put on any server, further broadcasting of functions are in dev.
# This blockchain is now designed to be centralized as the broadcasting and comparing chain functions are still in dev.


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


def proof_of_work(block):
    block.nonce = 0
    computed_hash = block.hash()
    while not computed_hash.startswith('0' * Blockchain.difficulty):
        block.nonce += 1
        computed_hash = block.hash()
    return computed_hash


def is_valid_proof(block, block_hash):
    return (block_hash.startswith('0' * Blockchain.difficulty) and
            block_hash == block.hash())


class Blockchain(object):
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

    def add_block(self, block, proof):
        previous_hash = self.last_block.hash
        if previous_hash != block.previous_hash:
            return False

        if not is_valid_proof(block, proof):
            return False

        block.hash = proof
        self.chain.append(block)
        return True

    def add_new_transaction(self, transaction):
        self.unconfirmed_transactions.append(transaction)

    def send(self, sender, recipient, amount):
        nb = (sender, recipient, amount)
        self.add_new_transaction(nb)

    def mine(self):
        if not self.unconfirmed_transactions:
            return False

        last_block = self.last_block

        new_block = Block(index=last_block.index + 1,
                          transactions=self.unconfirmed_transactions,
                          timestamp=time.time(),
                          previous_hash=last_block.hash)

        proof = proof_of_work(new_block)
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

    f = open('blockchain.data', 'w', encoding='utf-8')
    f.write(dumps({"length": str(len(chain_data)), "chain": chain_data}))
    f.close()

    o = open('blockchain.data', 'r', encoding='utf-8')
    oe = o.read()
    o.close()

    return oe


app.run(debug=False, port=8000)

# You can further put the api on any server you want
# This is much needed as I do not have a server

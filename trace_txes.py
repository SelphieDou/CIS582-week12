from bitcoinrpc.authproxy import AuthServiceProxy, JSONRPCException
import json
from datetime import datetime

rpc_user='quaker_quorum'
rpc_password='franklin_fought_for_continental_cash'
rpc_ip='3.134.159.30'
rpc_port='8332'

rpc_connection = AuthServiceProxy("http://%s:%s@%s:%s"%(rpc_user, rpc_password, rpc_ip, rpc_port))

###################################

class TXO:
    def __init__(self, tx_hash, n, amount, owner, time ):
        self.tx_hash = tx_hash 
        self.n = n
        self.amount = amount
        self.owner = owner
        self.time = time
        self.inputs = []

    def __str__(self, level=0):
        ret = "\t"*level+repr(self.tx_hash)+"\n"
        for tx in self.inputs:
            ret += tx.__str__(level+1)
        return ret

    def to_json(self):
        fields = ['tx_hash','n','amount','owner']
        json_dict = { field: self.__dict__[field] for field in fields }
        json_dict.update( {'time': datetime.timestamp(self.time) } )
        if len(self.inputs) > 0:
            for txo in self.inputs:
                json_dict.update( {'inputs': json.loads(txo.to_json()) } )
        return json.dumps(json_dict, sort_keys=True, indent=4)

    @classmethod
    def from_tx_hash(cls,tx_hash,n=0):
        #YOUR CODE HERE
        #this function takes in a txid of a transaction and return a TXO object of that transaction

        tx = rpc_connection.getrawtransaction(tx_hash,True)
        print(tx)
        for attr in tx['vout']:
            if attr['n'] == 0:   
                tx_hash = tx['hash']
                print(tx_hash)
                n = attr['n']
                print(n)
                address = attr['scriptPubKey']['addresses']
                owner = json.loads(address)
                print(owner['addresses'])
                amount = int(attr['value']) 
                print(amount)
                time = datetime.datetime.fromtimestamp(tx['time'],None) 
                print(tx['time'])
                break
            else:
                print('No such transaction!')
        return TXO['tx_hash', 'n', 'amount', 'owner', 'time']
        

    def get_inputs(self,d):
        #YOUR CODE HERE
        if not self.tx_hash:
            print('Invalid inputs!')
            return 
        if d < 1:
            print('Invalid depth!')
            return

        self.get_leaf_TXOs() #fill the first level of leaves (inputs of the current transaction)
        if d == 1: 
            return self #if depth = 1, done.
        if d > 1:
            if not self.inputs:
                #if depth > 1, recursively call this function for each leaf(inputs) and get its TXO objects
                for obj in self.inputs: 
                    self.get_inputs(obj,d-1)   
            return self

        

    def get_leaf_TXOs(self):
        #this function take an TXO object as input and fill its leaves(inputs) lists with its input TXOs
        if self.tx_hash:
            tx = rpc_connection.getrawtransaction(self.tx_hash,True)
        if tx['vin']:
            for attr in tx['vin']:
                #call classmethod
                #get every TXO object from input ('vin') list
                obj = TXO.from_tx_hash(attr['txid'],0) 
                self.inputs.append(obj)
        return self





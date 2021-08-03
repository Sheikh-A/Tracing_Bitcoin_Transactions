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
        tx = rpc_connection.getrawtransaction(tx_hash,True)
        #use V.out to get tx
        v_out = tx.get("vout")
        #Get the array
        v_out = v_out[n]
        #Wallet Owner
        wallet_owner = v_out.get("scriptPubKey").get("addresses")[0]
        #Total Amount
        total_amount = v_out.get("value") * 100000000
        #date time
        date_time = datetime.fromtimestamp(tx.get("time"))
        #return all
        return TXO(tx_hash, n, total_amount, wallet_owner, date_time)


    def get_inputs(self,d=1):
        tx = rpc_connection.getrawtransaction(self.tx_hash,True)
        #Vin arg
        v_in = tx.get("vin")
        
        if d >= 1:
            #Set equal to 0
            id_var_counter = 0
            #Length of vin
            vin_length = len(v_in)
            #use While loop
            while id_var_counter < vin_length:
                #Get the array value
                d_value = v_in[id_var_counter]
                #get the transactions value
                transaction = TXO.from_tx_hash(d_value.get("txid"), d_value.get("vout"))
                #Get inputs
                transaction.get_inputs(d-1)
                #append inputs
                self.inputs.append(transaction)
                #increment loop counter
                id_var_counter += 1


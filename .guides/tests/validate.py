#!/usr/bin/env python3

import random
import os
import sys
from datetime import datetime
import json

try:
    from trace_txes import TXO
except ImportError:
    print( "Failed to import TXO" )
    raise ImportError("Could not import TXO from homework file 'trace_txes.py'")

def test_TXO(tx,tx_dict,num_tests=0,num_passed=0):
    nt = num_tests
    np = num_passed
    if tx_dict['inputs']:
        for child_dict in tx_dict:
            ran_test = False
            for child_tx in tx.inputs:
                if child_tx.n == child_dict['n']:
                    ran_test = True
                    nnt,nnp = test_TXO(child_tx,child_dict,num_tests,num_passed)
                    num_passed += nnp
                    num_tests += nnt
            if not ran_test: #If no matching input in tx object, then that's equivalent to running a test and failing it
                num_tests += 1
    
    nt += 1
    if not isinstance(tx.time,datetime):
        print( "FAILURE: TXO.time should be a datetime object" )
        print( f"type(TXO.time) = {type(tx.time)}" )
    if tx.amount == tx_dict['amount']:
        print( "SUCCESS: TXO.amount successfully retrieved" )
        np += 1
    else:
        print( "FAILURE: on 'amount' field" )
        print( f"Received {tx.amount}" )
        print( f"Expected {tx_dict['amount']}" )
    if tx.owner == tx_dict['owner']:
        print( "SUCCESS: TXO.owner successfully retrieved" )
        np += 1
    else:
        print( "FAILURE: on 'owner' field" )
        print( f"Received {tx.owner}" )
        print( f"Expected {tx_dict['owner']}" )
    if tx.time == datetime.fromtimestamp(tx_dict['time']):
        print( "SUCCESS: TXO.time successfully retrieved" )
        np += 1
    else:
        print( "FAILURE: on 'time' field" )
        print( f"Received {datetime.timestamp(tx.time)}" )
        print( f"Expected {tx_dict['time']}" )
    return nt,np

def validate():
    num_passed = 0

    try:
        jsonfile = open(os.path.join(sys.path[0], 'tx_data.json'))
        test_txos = json.load(jsonfile)
        jsonfile.close()
    except Exception as e:
        print( e )

    num_tests = 0
    for tx_dict in test_txos:
        try:
            tx = TXO.from_tx_hash(tx_dict['tx_hash'],tx_dict['n'])
        except Exception as e:
            num_tests += 1 #This is like running a test and failing
            print( "FAILURE: from_tx_hash() " )
            continue
        nt, np = test_TXO(tx,tx_dict,num_tests,num_passed)
        num_tests += nt
        num_passed += np

    try:
        tx_get_inputs = TXO.from_tx_hash('1620c59574743195fb5ad0d0bf96ac4e16a78f3912a58d23c6e2aeaf2595bfe7')
        tx_get_inputs.get_inputs(d=3)
        if len(tx_get_inputs.inputs) != 1:
            print("(Ungraded) you did not pass sanity check 1 for get_inputs")
        
        if len(tx_get_inputs.inputs[0].inputs) != 2:
            print("(Ungraded) you did not pass sanity check 2 for get_inputs")
        
        depth_2_inps = tx_get_inputs.inputs[0].inputs
        if len(depth_2_inps[0].inputs) + len(depth_2_inps[1].inputs) != 15:
            print("(Ungraded) you did not pass sanity check 3 for get_inputs")
            
    except Exception as e:
        print('Error occurred when running get_inputs')
        print(e)
        print('Uncomment the line in the validate script to see the full error traceback')
        # raise(e)
        
    print( f"Passed {num_passed}/{3*num_tests}" )
    return int( 100*float(num_passed)/(3*num_tests) )



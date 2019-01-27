# -*- coding: utf-8 -*-
"""
Created on Sat Jan 26 17:10:13 2019

@author: Anoop
"""
from smart_contract_client import smart_contract_client
import hashlib


def hash_doc(filename, action='store', txn_id=None):
    verify = False
    hasher = hashlib.md5()
    with open(filename, 'rb') as afile:
       buf = afile.read()
       hasher.update(buf)
    block1 = hasher.hexdigest()
    if action == 'store':
        txn_id = smart_contract_client(data=block1, action='store')
        return txn_id
    else:
        verify = smart_contract_client(data=block1, action='verify', txn_id=txn_id)
        return verify


if __name__ == '__main__':
    txn_id = hash_doc('static/Census_precent_change.csv', action='store')
    res = hash_doc('static/Census_precent_change.csv', action='verify', txn_id=txn_id)
    print(res)



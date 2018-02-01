# -*- coding: utf-8 -*-

from .context import nempy
import unittest
import json
import os

pvtkey = os.environ.get('pvtkey')
print("###",pvtkey,"###")

class AdvancedTestSuite(unittest.TestCase):
    #######################################################################################

    def test_pvtkey2pubkey(self):
        pubkey = nempy.pvtkey2pubkey("1411c9ff8dda47053133eeed943ea0365e81876b381fb205abc2aa391d6ad499")
        print(pubkey)
        assert pubkey == "f0d94bcdc9aa20f893f22b84896959c4f87947c8d52acee92762afe8363364f3"

    #######################################################################################

    def test_pubkey2addr_mainnet(self):
        pubkey = "f0d94bcdc9aa20f893f22b84896959c4f87947c8d52acee92762afe8363364f3"
        addr = nempy.pubkey2addr(pubkey)
        print(addr)
        assert addr == "NC4WKOGT6V2B6O5LKBMBMBC6UBIARCSX7Q6UKQMT"

    def test_pubkey2addr_testnet(self):
        pubkey = "f0d94bcdc9aa20f893f22b84896959c4f87947c8d52acee92762afe8363364f3"
        addr = nempy.pubkey2addr(pubkey, version="test")
        print(addr)
        assert addr == "TC4WKOGT6V2B6O5LKBMBMBC6UBIARCSX7R4WPJCV"

    def test_pubkey2addr_mijinnet(self):
        pubkey = "f0d94bcdc9aa20f893f22b84896959c4f87947c8d52acee92762afe8363364f3"
        addr = nempy.pubkey2addr(pubkey, version="mijin")
        print(addr)
        assert addr == "MC4WKOGT6V2B6O5LKBMBMBC6UBIARCSX7SAZWCBP"

    #######################################################################################

    def _test_transfer_transaction(self): # OK
        # signer: Your public key
        params = {
            "timeStamp": nempy.getTimeStamp(),
            "amount": int(0.1*1000000),
            "fee": int(0.15*1000000),
            "recipient": "TC4WKOGT6V2B6O5LKBMBMBC6UBIARCSX7R4WPJCV",
            "type": nempy.TransactionType.transfer_transaction,
            "deadline": nempy.getTimeStamp(delta=3600),
            "message":
            {
                "payload": "hello",
                "type": 1
            },
            "version": nempy.Version.test,
            "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
            "mosaics":[
            {
                "mosaicId":{
                    "namespaceId": "nem",
                    "name": "xem"
                },
                "quantity": 100000
            }
            ]
        }

        data = nempy.createTransaction(params)
        signed_data = nempy.signTransaction(data, pvtkey)
        r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
        print(r.json())

    def _test_importance_transfer_transaction(self): # OK
        # signer: Your public key
        # remoteAccount: Public key bytes of remote account
        # remoteAccount: Public key bytes of your account
        params =  {
            "timeStamp": nempy.getTimeStamp(),
            "fee": 150000,
            "mode": nempy.Mode.activate,
            "remoteAccount": "321e4febc03f39ae3e0216ab6b9970ffd0817f38e9edc08e4baa7c62aab7b7dd",
            "type": nempy.TransactionType.importance_transfer_transaction,
            "deadline": nempy.getTimeStamp(delta=3600),
            "version": nempy.Version.test,
            "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357"
        }
        data = nempy.createTransaction(params)
        signed_data = nempy.signTransaction(data, pvtkey)
        r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
        print(r.json())

    def _test_multisig_aggregate_modification_transfer_transaction(self): # OK
        params = {
            "timeStamp": nempy.getTimeStamp(),
            "fee": 500000,
            "type": nempy.TransactionType.multisig_aggregate_modification_transfer_transaction,
            "deadline": nempy.getTimeStamp(delta=3600),
            "version": nempy.Version.test,
            "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
            "modifications": [
                {
                    "modificationType": nempy.Mode.add_cosignatory,
                    "cosignatoryAccount": "213150649f51d6e9113316cbec5bf752ef7968c1e823a28f19821e91daf848be"
                },
                {
                    "modificationType": nempy.Mode.add_cosignatory,
                    "cosignatoryAccount": "213150649f51d6e9113316cbec5bf752ef7968c1e823a28f19821e91daf848be"
                }
            ],
            "minCosignatories" : {
                "relativeChange" : 2
            }
        }
        data = nempy.createTransaction(params)
        signed_data = nempy.signTransaction(data, pvtkey)
        r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
        print(r.json())

    def _test_multisig_signature_transaction(self): # OK
        # otherAccount: Address of multisig account
        params = {
            "timeStamp": nempy.getTimeStamp(),
            "fee": 150000,
            "type": nempy.TransactionType.multisig_signature_transaction,
            "deadline": nempy.getTimeStamp(delta=3600),
            "version": nempy.Version.test,
            "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
            "otherHash": {
                "data": "dac3435b36b65825375366c848a1fdd2b26cb55011db32526eaa266ee32f6419"
            },
            "otherAccount": "TC4WKOGT6V2B6O5LKBMBMBC6UBIARCSX7R4WPJCV" 
        }
        data = nempy.createTransaction(params)
        signed_data = nempy.signTransaction(data, pvtkey)
        r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
        print(r.json())

    def test_multisig_transaction(self): # OK
        # This function wraps a transfer, an importance transfer or an aggregate modification transaction.
        params = {
            "timeStamp": nempy.getTimeStamp(),
            "fee": int(0.15*1000000),
            "type": nempy.TransactionType.multisig_transaction,
            "deadline": nempy.getTimeStamp(delta=3600),
            "version": nempy.Version.test,
            "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
            "inner":{
                "timeStamp": nempy.getTimeStamp(),
                "amount": int(0.1*1000000),
                "fee": int(0.15*1000000),
                "recipient": "TC4WKOGT6V2B6O5LKBMBMBC6UBIARCSX7R4WPJCV",
                "type": nempy.TransactionType.transfer_transaction,
                "deadline": nempy.getTimeStamp(delta=3600),
                "message":
                {
                    "payload": "hello",
                    "type": 1
                },
                "version": nempy.Version.test,
                "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
                "mosaics":[
                {
                    "mosaicId":{
                        "namespaceId": "nem",
                        "name": "xem"
                    },
                    "quantity": 100000
                }
                ]
            }
        }
        data = nempy.createTransaction(params)
        signed_data = nempy.signTransaction(data, pvtkey)
        r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
        print(r.json())

    def _test_provision_namespace_transaction(self): # OK
        params = {
            "timeStamp": nempy.getTimeStamp(),
            "fee": 150000,
            "type": nempy.TransactionType.provision_namespace_transaction,
            "deadline": nempy.getTimeStamp(delta=3600),
            "version": nempy.Version.test,
            "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
            "newPart": "hello",
            "parent": "mochizuki" # or False if root provisioning
        }
        data = nempy.createTransaction(params)
        signed_data = nempy.signTransaction(data, pvtkey)
        r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
        print(r.json())

    def _test_mosaic_definition_creation_transaction(self): # OK
        params = {
            "timeStamp": nempy.getTimeStamp(),
            "fee": 150000,
            "type": nempy.TransactionType.mosaic_definition_creation_transaction,
            "deadline": nempy.getTimeStamp(delta=3600),
            "version": nempy.Version.test,
            "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
            "mosaicDefinition": {
                "creator": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
                "description": "this is test mosaic",
                "id": {
                    "namespaceId": "mochizuki.hello",
                    "name": "mochitoken2"
                },
                "properties": [{
                        "name": "divisibility",
                        "value": "3"
                    },{
                        "name": "initialSupply",
                        "value": "1000"
                    },{
                        "name": "supplyMutable",
                        "value": "false"
                    },{
                        "name": "transferable",
                        "value": "true"
                    }
                ],
                "levy": {
                    "type": 1,
                    "recipient": "TD3RXTHBLK6J3UD2BH2PXSOFLPWZOTR34WCG4HXH",
                    "mosaicId": {
                        "namespaceId": "nem",
                        "name": "xem"
                    },
                    "fee": 10
                }
            }
        }
        data = nempy.createTransaction(params)
        signed_data = nempy.signTransaction(data, pvtkey)
        r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
        print(r.json())

    def _test_mosaic_supply_change_transaction(self):
        params = {
            "timeStamp": nempy.getTimeStamp(),
            "fee": 150000,
            "type": nempy.TransactionType.mosaic_supply_change_transaction,
            "deadline": nempy.getTimeStamp(delta=3600),
            "version": nempy.Version.test,
            "signer": "0c38cc1d69eb8f673a8803cf976f12e3639f868b0cfe75d1477cbf59643b6357",
            "supplyType": nempy.SupplyType.decrease,
            "delta": 323,
            "mosaicId": {
                "namespaceId": "mochizuki.hello",
                "name": "mochitoken"
            }
        }
        data = nempy.createTransaction(params)
        signed_data = nempy.signTransaction(data, pvtkey)
        r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
        print(r.json())

if __name__ == '__main__':
    unittest.main()

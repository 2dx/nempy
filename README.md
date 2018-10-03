NEM SDK for Python3
========================

トランザクション生成用のJSONをcreateTransaction関数に渡すとバイト文字列が返ってきます。それをsignTransaction関数で処理すると署名データが得られます。ここまでをオフラインで実行できます。最後にオンライン環境でannounceTransaction関数でアナウンスすればトランザクションがブロックチェーンに記録されます。モザイク作成時のlevyとメッセージの暗号化は未実装です。  

テスト用としてのみ使用してください。このコードによって損害が生じても責任は負いかねます。  
Please use only for testing. I am not responsible for any trouble that may occur.

#### 実行例(トランスファートランザクション)

* インポート --- import

```
import nempy
```

* トランザクション作成 --- create transaction  

```
params = {
	"transaction":
	{
	    "timeStamp": nempy.getTimeStamp(),
	    "amount": int(0.3*1000000),
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
	    "signer": "f0d94bcdc9aa20f893f22b84896959c4f87947c8d52acee92762afe8363364f3",
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
```

* 署名 --- sign transaction 

```
signed_data = nempy.signTransaction(data, pvtkey="1411c9ff8dda47053133eeed943ea0365e81876b381fb205abc2aa391d6ad499")
``` 

* アナウンス --- announce signed transaction

```
r = nempy.announceTransaction(signed_data, nis="http://23.228.67.85:7890")
``` 
* 結果の確認 --- check result  

```
print(r.json())
```

```
{
	"innerTransactionHash": {},
	"code": 1,
	"type": 1,
	"message": "SUCCESS",
	"transactionHash": {
		"data": "84792a6e23a8a4d1b889b5c60fcf248c91519da2e54aba6ab3d4af1096ce700a"
	}
}
```

#### その他のトランザクションを生成するために、createTransaction関数に渡すJSON構造の例

* Importance transfer transaction

```
# signer: Your public key
# remoteAccount: Public key bytes of remote account
# signer: Public key bytes of your account
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
```


* Multisig aggregate modification transfer transaction

```
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
```

* Multisig signature transaction

```
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
```

* Multisig transaction

```
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
```

* Provision namespace transaction

```
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
```

* Mosaic definition creation transaction

```
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
            "name": "mochitoken"
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
```

* Mosaic supply change transaction

```
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
```

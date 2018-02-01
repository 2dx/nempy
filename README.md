NEM SDK for Python3
========================

現在のところ、マルチシグトランザクション以外を実装済みです。使い方はそのうちREADMEにまとめるつもりですが、今のところはtest/test.pyを見て下さい。トランザクション生成用のJSONをcreateTransaction関数に渡すとバイト文字列が返ってきます。それをsignTransaction関数で処理すると署名データが得られます。ここまでをオフラインで実行できます。最後にオンライン環境でannounceTransaction関数でアナウンスすればトランザクションがブロックチェーンに記録されます。  

テスト用としてのみ使用してください。このコードによって損害が生じても責任は負いかねます。  
Please use only for testing. I am not responsible for any trouble that may occur.

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
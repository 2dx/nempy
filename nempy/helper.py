class Version():
	main = 0x68000001
	test = 0x98000001
	mijin = 0x60000001

class TransactionType():
	transfer_transaction = 0x0101
	importance_transfer_transaction = 0x0801
	multisig_aggregate_modification_transfer_transaction = 0x1001
	multisig_signature_transaction = 0x1002
	multisig_transaction = 0x1004
	provision_namespace_transaction = 0x2001
	mosaic_definition_creation_transaction = 0x4001
	mosaic_supply_change_transaction = 0x4002

class Mode():
	activate = 0x01
	deactivate = 0x02
	add_cosignatory = 0x01
	delete_cosignatory = 0x02

class RentalFee():
	root = 100*1000000
	sub = 10*1000000

class CreationFee:
	mosaic = 10*1000000

class SupplyType:
	increase = 0x01
	decrease = 0x02

def CreationFeeSink(versionHex):
	if versionHex[-2:] == "68":
		# main
		return "NBMOSAICOD4F54EE5CDMR23CCBGOAM2XSIUX6TRS"
	elif versionHex[-2:] == "98":
		# test
		return "TBMOSAICOD4F54EE5CDMR23CCBGOAM2XSJBR5OLC"
	else:
		raise

def RentalFeeSink(versionHex):
	if versionHex[-2:] == "68":
		# main
		return "NAMESPACEWH4MKFMBCVFERDPOOP4FK7MTBXDPZZA"
	elif versionHex[-2:] == "98":
		# test
		return "TAMESPACEWH4MKFMBCVFERDPOOP4FK7MTDJEYP35"
	else:
		raise
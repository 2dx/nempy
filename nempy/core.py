# -*- coding: utf-8 -*-
import base64
import hashlib
import sys
import binascii
import ed25519
sys.path.insert(0, 'python-sha3')
from python_sha3 import *
from .helper import *
from config import config
import datetime
import struct
import binascii
import requests
import json
import time

def getTimeStamp(delta=0):
	return int(time.time()) - 1427587585 + delta

def post(nis,url,data):
	headers = {'Content-type': 'application/json'}
	return requests.post(nis+url, data=json.dumps(data), headers=headers, timeout=10)

def int2hex(i: int):
	return binascii.hexlify(struct.pack('<I', i)).decode('utf-8')

def long2hex(i: int):
	return binascii.hexlify(struct.pack('<q', i)).decode('utf-8')

def string2hex(string: str):
	return binascii.hexlify(string.encode('utf-8')).decode('utf-8')

def pvtkey2pubkey(pvtkey :str):
    binpvtkey = binascii.unhexlify(pvtkey)[::-1]
    binpubkey = ed25519.publickey_hash_unsafe(binpvtkey , sha3_512)
    return binascii.hexlify(binpubkey).decode('utf-8')

def pubkey2addr(pubkey :str, version="main"):
	pubkey = binascii.unhexlify(pubkey)
	s = sha3_256()
	s.update(pubkey)
	sha3_pubkey = s.digest()
	h = hashlib.new('ripemd160')
	h.update(sha3_pubkey)
	ripe = h.digest()
	if version == 'main':
		versionHex = "68" + ripe.hex()
	elif version == 'test':
		versionHex = "98" + ripe.hex()
	elif version == 'mijin':
		versionHex = "60" + ripe.hex()
	versionHex = binascii.unhexlify(versionHex)
	s2 = sha3_256()
	s2.update(versionHex)
	checksum = s2.digest()[0:4]
	address = base64.b32encode(versionHex + checksum)
	return address.decode('utf-8')

def announceTransaction(data, nis):
	return post(nis, '/transaction/announce', data)

def signTransaction(hexString, pvtkey):
	binpvtkey = binascii.unhexlify(pvtkey)[::-1]
	binpubkey = binascii.unhexlify(pvtkey2pubkey(pvtkey))
	signature = ed25519.signature_hash_unsafe(binascii.unhexlify(hexString), binpvtkey, binpubkey, sha3_512)
	signed_data = {"data": hexString, "signature": signature.hex()}
	return signed_data

# https://nemproject.github.io
def createTransaction(t):
	feeHex = long2hex(t["fee"])
	timestampHex = int2hex(t["timeStamp"])
	deadlineHex = int2hex(t["deadline"])
	transactionTypeHex = int2hex(t["type"])
	version = t["version"] + (t["type"]==TransactionType.transfer_transaction or t["type"]==TransactionType.multisig_aggregate_modification_transfer_transaction)
	versionHex = int2hex(version)
	pubkeyLengthHex = int2hex(len(t["signer"])//2)
	hexString = transactionTypeHex + versionHex + timestampHex + pubkeyLengthHex + t["signer"] + feeHex + deadlineHex
	if t["type"] == TransactionType.transfer_transaction:
		hexString += createTransferPart(t["recipient"], t["amount"], t["message"], t["mosaics"])
	elif t["type"] == TransactionType.importance_transfer_transaction:
		hexString += createImportanceTransferPart(t["mode"],t["remoteAccount"])
	elif t["type"] == TransactionType.multisig_aggregate_modification_transfer_transaction:
		hexString += createMultisigAggregateModificationTransferPart(t["modifications"], t["minCosignatories"])
	elif t["type"] == TransactionType.multisig_signature_transaction:
		hexString += createMultisigSignaturePart(t["otherHash"], t["otherAccount"])
	elif t["type"] == TransactionType.multisig_transaction:
		hexString += createMultisigPart(t["inner"])
	elif t["type"] == TransactionType.provision_namespace_transaction:
		hexString += createProvisionNamespaceTransactionPart(RentalFeeSink(versionHex), t["newPart"], t["parent"])
	elif t["type"] == TransactionType.mosaic_definition_creation_transaction:
		hexString += createMosaicDefinitionCreationTransactionPart(CreationFeeSink(versionHex), t["mosaicDefinition"])
	elif t["type"] == TransactionType.mosaic_supply_change_transaction:
		hexString += createMosaicSupplyChangeTransactionPart(t["supplyType"], t["delta"], t["mosaicId"])
	else:
		raise
	return hexString


def createTransferPart(recipientAddressString, amount, message, mosaics):
	recipientAddressHex = string2hex(recipientAddressString)
	recipientAddressLengthHex = int2hex(len(recipientAddressHex)//2)
	amountHex = long2hex(amount)
	messageTypeHex = int2hex(message["type"])
	payloadHex = string2hex(message["payload"])
	hexString = recipientAddressLengthHex + recipientAddressHex + amountHex
	if len(payloadHex) > 0:
		# TODO ENCRYPTION
		payloadLengthHex = int2hex(len(payloadHex)//2)
		messageFieldLengthHex = int2hex(len(messageTypeHex + payloadLengthHex + payloadHex)//2)
		hexString += messageFieldLengthHex + messageTypeHex + payloadLengthHex + payloadHex
	else:
		messageFieldLengthHex = int2hex(0)
		hexString += messageFieldLengthHex
	mosaicsNumberHex = int2hex(len(mosaics))
	hexString += mosaicsNumberHex
	for mosaic in mosaics:
		quantityHex = long2hex(mosaic["quantity"])
		namespaceIdStringHex = string2hex(mosaic["mosaicId"]["namespaceId"])
		mosaicNameStringHex = string2hex(mosaic["mosaicId"]["name"])
		namespaceIdStringLength = len(namespaceIdStringHex)//2
		mosaicNameStringLength = len(mosaicNameStringHex)//2
		namespaceIdStringLengthHex = int2hex(namespaceIdStringLength)
		mosaicNameStringLengthHex = int2hex(mosaicNameStringLength)
		mosaicIdStructureLength = 4+namespaceIdStringLength+4+mosaicNameStringLength
		mosaicIdStructureLengthHex = int2hex(mosaicIdStructureLength)
		mosaicStructureLengthHex = int2hex(4+mosaicIdStructureLength+8)
		mosaicHex = mosaicStructureLengthHex + mosaicIdStructureLengthHex
		mosaicHex += namespaceIdStringLengthHex + namespaceIdStringHex
		mosaicHex += mosaicNameStringLengthHex + mosaicNameStringHex
		mosaicHex += quantityHex
		hexString += mosaicHex
	return hexString

def createImportanceTransferPart(mode, remoteAccount):
	hexString = int2hex(mode) + int2hex(0x20)
	hexString += remoteAccount
	return hexString

def createMultisigAggregateModificationTransferPart(modifications, minCosignatories):
	hexString = int2hex(len(modifications))
	for m in modifications:
		hexString += int2hex(0x28) + int2hex(m["modificationType"]) + int2hex(0x20) + m["cosignatoryAccount"]
	hexString += int2hex(0x04) + int2hex(minCosignatories["relativeChange"])
	return hexString

def createMultisigSignaturePart(otherHash, otherAccount):
	hexString = int2hex(0x24) + int2hex(0x20) + otherHash["data"] + int2hex(0x28) + string2hex(otherAccount)
	return hexString

def createProvisionNamespaceTransactionPart(rentalFeeSink, newPart, parent):
	if parent:
		rentalFee = RentalFee.sub
	else:
		rentalFee = RentalFee.root
	hexString = int2hex(0x28) + string2hex(rentalFeeSink) + long2hex(rentalFee)
	newPartString = string2hex(newPart)
	hexString += int2hex(len(newPartString)//2) + newPartString
	if parent:
		parentString = string2hex(parent)
		hexString += int2hex(len(parentString)//2) + parentString
	else:
		hexString += int2hex(0xffffffff)
	return hexString

def createMosaicDefinitionCreationTransactionPart(creationFeeSink, mosaicDefinition):
	if len(mosaicDefinition["creator"]) != 64:
		raise
	hexString = int2hex(0x20) + mosaicDefinition["creator"]
	# start mosaicDefinition
	namespaceIdStringHex = string2hex(mosaicDefinition["id"]["namespaceId"])
	mosaicNameStringHex = string2hex(mosaicDefinition["id"]["name"])
	mosaicIdStructureHex = int2hex(len(namespaceIdStringHex)//2) + namespaceIdStringHex + int2hex(len(mosaicNameStringHex)//2) + mosaicNameStringHex
	hexString += int2hex(len(mosaicIdStructureHex)//2) + mosaicIdStructureHex

	descriptionStringHex = string2hex(mosaicDefinition["description"])
	hexString += int2hex(len(descriptionStringHex)//2) + descriptionStringHex

	hexString += int2hex(len(mosaicDefinition["properties"]))
	for prop in mosaicDefinition["properties"]:
		propNameHex = string2hex(prop["name"])
		propValueHex = string2hex(prop["value"])
		propStructureHex = int2hex(len(propNameHex)//2) + propNameHex + int2hex(len(propValueHex)//2) + propValueHex
		hexString += int2hex(len(propStructureHex)//2) + propStructureHex

	if "levy" in mosaicDefinition:
		hexString += int2hex(0) # TODO LEVY
	else:
		hexString += int2hex(0)
	# end mosaicDefinition
	hexString = int2hex(len(hexString)//2) + hexString
	
	hexString += int2hex(0x28) + string2hex(creationFeeSink)
	hexString += long2hex(CreationFee.mosaic)
	print(hexString)
	return hexString

def createMosaicSupplyChangeTransactionPart(supplyType, delta, mosaicId):
	namespaceIdStringHex = string2hex(mosaicId["namespaceId"])
	mosaicNameStringHex = string2hex(mosaicId["name"])
	mosaicIdStructureHex = int2hex(len(namespaceIdStringHex)//2) + namespaceIdStringHex + int2hex(len(mosaicNameStringHex)//2) + mosaicNameStringHex
	hexString = int2hex(len(mosaicIdStructureHex)//2) + mosaicIdStructureHex

	hexString += int2hex(supplyType)
	hexString += long2hex(delta)

	return hexString

def createMultisigPart(inner):
	innerHex = createTransaction(inner)
	return int2hex(len(innerHex)//2) + innerHex


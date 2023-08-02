import logging

logging.basicConfig(
	filename="koto.log",
	filemode="w",
	encoding="utf-8",
	format="%(asctime)s %(module)s %(levelname)s %(message)s",
	level=logging.DEBUG,
)

from pysui import SuiConfig, SyncClient, handle_result
from pysui.sui.sui_txn.sync_transaction import SuiTransaction
from pysui.sui.sui_types.collections import SuiArray
from pysui.sui.sui_types.address import SuiAddress
from pysui.sui.sui_types.scalars import ObjectID, SuiU64
from pysui.sui.sui_types.bcs import OptionalU64
cfg = SuiConfig.user_config(
	rpc_url="http://localhost:9000",
	prv_keys=["AIk9y2ecOdbQvQC/GLqdZ6SyEVD4TWLYZ3NO73p7ERBR"],
)

client = SyncClient(cfg)

txer = SuiTransaction(client)
package = "0xbc2738ba27f9076c8280749b1e0c6b1cbc5819b1d8bc471224979ce4c7e874af::koto"

def create_bal(recipient: str, kotocap: str):
	tx = SuiTransaction(client)
	args = SuiArray([ObjectID(kotocap), SuiAddress(recipient)])
	tx.move_call(target=package+"::create", arguments=args)
	return tx.execute()

def mint_to_bal(bal: str, kotocap: str, value: int):
	tx = SuiTransaction(client)
	args = SuiArray([ObjectID(kotocap),ObjectID(bal),SuiU64(value)])
	tx.move_call(target=package+"::mint", arguments=args)
	return tx.execute()

def burn_from_bal(bal:str, kotocap: str, value: int):
	tx = SuiTransaction(client)
	args = SuiArray([ObjectID(kotocap),ObjectID(bal),SuiU64(value)])
	tx.move_call(target=package+"::burn", arguments=args)
	return tx.execute()

result = handle_result(burn_from_bal("0x3baf2c6617e56a9c98f5d45eb7d79bdcd24a606148e324b5c2416a43cc8beaf8","0xfe835dad4314610da52ac49be820c54d2781e124b43799e1ccfc7b9a1d65032f",1000))
print(result.effects.status.status)

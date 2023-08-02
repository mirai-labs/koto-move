import logging
import os
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
	prv_keys=[os.environ["KEY"]],
)

client = SyncClient(cfg)

txer = SuiTransaction(client)
package = os.environ["PACKAGE"] + "::koto"

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

def banned_list(registry: str):
	return client.get_object(ObjectID(registry))

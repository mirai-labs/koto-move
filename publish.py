import json
import os
import subprocess
from time import sleep

NETWORK = os.environ["NETWORK"]


def transfer_object(
    object_id: str,
    to: str,
):
    cmd = f"sui client transfer --to {to} --object-id {object_id} --gas-budget 1000000000 --json"  # fmt: skip
    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()
    print(json.dumps(json.loads(output.decode("utf-8")), indent=4))
    return


def deploy():
    cmd = "sui client publish --gas-budget 500000000 --json"

    if NETWORK == "testnet":
        cmd = f"{cmd} --skip-dependency-verification"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

    print(json.dumps(json.loads(output.decode("utf-8")), indent=4))

    result = json.loads(output.decode("utf-8"))

    object_changes = result["objectChanges"]

    config = {}

    for change in object_changes:
        if change["type"] == "published":
            config["KotoPackageId"] = change["packageId"]
        elif change["type"] == "created":
            if "CoinMetadata" in change["objectType"]:
                config["KotoCoinMetadata"] = change["objectId"]
            elif "TreasuryCap" in change["objectType"]:
                config["KotoTreasuryCap"] = change["objectId"]
            elif "UpgradeCap" in change["objectType"]:
                config["KotoUpgradeCap"] = change["objectId"]

    print(json.dumps(config, indent=4))

    with open(f"./koto-{NETWORK}.json", "w+") as f:
        json.dump(config, f, indent=4)

    sleep(3)

    print("Transferring UpgradeCap to 0x0000000000000000000000000000000000000000000000000000000000000000")  # fmt: skip
    transfer_object(config["KotoUpgradeCap"], "0x0000000000000000000000000000000000000000000000000000000000000000")  # fmt: skip


deploy()

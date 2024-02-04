import json
import subprocess


def deploy():
    cmd = "sui client publish --gas-budget 500000000 --skip-dependency-verification --with-unpublished-dependencies --json"

    process = subprocess.Popen(cmd, stdout=subprocess.PIPE, shell=True)
    output, error = process.communicate()

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

    with open("./koto.json", "w+") as f:
        json.dump(config, f, indent=4)


deploy()

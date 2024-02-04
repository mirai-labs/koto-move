import json

with open("./koto.json", "r") as f:
    objects = json.load(f)

cmd = f"sui client call --package {objects['KotoPackageId']} --module koto --function mint --args {objects['KotoTreasuryCap']}, 0x64, 0x43888ff633a296d4d87026ee10a4d9f3ca649ea3403190a45ddd9712948d73cb --gas-budget 5000000000"
print(cmd)

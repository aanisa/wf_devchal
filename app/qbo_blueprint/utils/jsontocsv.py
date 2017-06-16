#!/usr/bin/env python

import json
import sys
import csv

# throw away script to create a CSV of accounts from the json of a query of accounts

input = sys.stdin.read()

writer = csv.writer(sys.stdout)

for account in json.loads(input)["QueryResponse"]["Account"]:
    writer.writerow([
        account.get("FullyQualifiedName", ""),
        account.get("Classification", ""),
        account.get("AccountType", ""),
        account.get("AccountSubType", ""),
        account.get("Description", "")
    ])

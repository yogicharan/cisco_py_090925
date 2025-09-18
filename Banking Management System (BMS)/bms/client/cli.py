import requests
import argparse
import sys

API = "http://localhost:5000/api"


def create(args):
    payload = {"name": args.name, "number": args.number, "balance": args.balance}
    r = requests.post(f"{API}/accounts", json=payload)
    r.raise_for_status()
    print(r.json())


def list_accounts(_args):
    r = requests.get(f"{API}/accounts")
    r.raise_for_status()
    for a in r.json():
        print(a)


def get(args):
    r = requests.get(f"{API}/accounts/{args.id}")
    r.raise_for_status()
    print(r.json())


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest="cmd")
    p = sub.add_parser("create")
    p.add_argument("--name", required=True)
    p.add_argument("--number", required=True)
    p.add_argument("--balance", type=float, default=0.0)
    p = sub.add_parser("list")
    p = sub.add_parser("get")
    p.add_argument("--id", type=int, required=True)
    args = parser.parse_args()
    if args.cmd == "create":
        create(args)
    elif args.cmd == "list":
        list_accounts(args)
    elif args.cmd == "get":
        get(args)
    else:
        parser.print_help()
        sys.exit(1)


if __name__ == "__main__":
    main()

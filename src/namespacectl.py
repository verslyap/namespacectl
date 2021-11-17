import argparse
import dbus

def parse():
    parser = argparse.ArgumentParser("NSWorker",description="Worker process for namespaced")
    subparsers = parser.add_subparsers(dest="action")

    create = subparsers.add_parser("add")
    create.add_argument("name")
    create.add_argument("type",choices=["cgroup","pid","ipc","uts","net","mount","user","time"])

    remove = subparsers.add_parser("remove")
    remove.add_argument("name")

    reload = subparsers.add_parser("reload")

    dump = subparsers.add_parser("dump")

    return parser.parse_args()

def main():
    o = parse()
    bus = dbus.SystemBus()
    namespaced = bus.get_object("org.apv.namespaced", "/org/apv/namespaced/namespaces")
    match o.action:
        case "add":
            result = namespaced.add(o.name,o.type)
        case "remove":
            result = namespaced.remove(o.name)
        case "reload":
            namespaced.reload()
        case "dump":
            print(namespaced.dump())

if __name__ == "__main__":
    main()

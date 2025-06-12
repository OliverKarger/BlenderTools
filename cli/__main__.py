from . import parser

def main():
    args = parser.parse()

    if hasattr(args, "handler") and callable(args.handler):
        args.handler(args)
    else:
        print("[ERROR] No handler defined for this command.")

if __name__ == "__main__":
    main()

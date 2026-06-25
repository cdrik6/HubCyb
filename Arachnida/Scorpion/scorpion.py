import sys


def main():
    try:
        params = parse_argv(sys.argv, USAGE, PATH)
    except KeyboardInterrupt:
        print("\nScorpion interrupted by user.")


if __name__ == "__main__":
    main()

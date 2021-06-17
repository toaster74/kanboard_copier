"""Console script for kanboard_copier."""

import fire

def help():
    print("kanboard_copier")
    print("=" * len("kanboard_copier"))
    print("Copy of Kanboard project to another Kanboard project")

def main():
    fire.Fire({
        "help": help
    })


if __name__ == "__main__":
    main() # pragma: no cover

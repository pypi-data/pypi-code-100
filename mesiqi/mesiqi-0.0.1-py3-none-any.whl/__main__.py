if __name__ == "__main__":  # pragma: no cover
    import sys

    from mesiqi.framework.cli import main

    if sys.argv[0].endswith("__main__.py"):
        sys.argv[0] = "python -m mesiqi"
    main()

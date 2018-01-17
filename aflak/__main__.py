"""
Entrypoint module, in case you use `python -m aflak`.
"""
import sys

from aflak.aflak import main


if __name__ == "__main__":
    sys.exit(main())

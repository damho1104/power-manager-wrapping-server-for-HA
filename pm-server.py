#!/usr/bin/env python3
# -*- coding: utf-8 -*-
import sys
import lib
from lib.util import log


def main():
    lib.run()
    return True


if __name__ == '__main__':
    if not main():
        sys.exit(1)
    sys.exit(0)

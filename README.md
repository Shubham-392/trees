# trees

Python implementations of tree data structures used in databases and storage systems.

## Implemented

- **B-Tree** — `btree.py`
- **B+Tree** — `bplus.py`

## Planned

- R-Tree
- Geo-spatial trees

## Setup

Requires Python (version pinned in `.python-version`) and [uv](https://github.com/astral-sh/uv).

    git clone https://github.com/Shubham-392/trees.git
    cd trees
    uv sync

## Run Tests

    uv run python btest.py     # B-Tree
    uv run python bptest.py    # B+Tree

## Structure

    trees/
    ├── btree.py     # B-Tree
    ├── bplus.py     # B+Tree
    ├── btest.py     # B-Tree tests
    └── bptest.py    # B+Tree tests

## License

MIT
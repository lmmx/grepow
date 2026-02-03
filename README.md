# grepow

[![PyPI version](https://img.shields.io/pypi/v/grepow.svg)](https://pypi.org/project/grepow/)
[![Python versions](https://img.shields.io/pypi/pyversions/grepow.svg)](https://pypi.org/project/grepow/)
[![License](https://img.shields.io/pypi/l/grepow.svg)](https://github.com/lmmx/grepow/blob/master/LICENSE)
[![pre-commit.ci status](https://results.pre-commit.ci/badge/github/lmmx/grepow/master.svg)](https://results.pre-commit.ci/latest/github/lmmx/grepow/master)

CLI for sparse checkouts of results from [grep.app](https://grep.app) repo search.

## Installation

```sh
uv pip install grepow
````

## Requirements

- Python 3.10+
- Git (with sparse-checkout support)

## Features

- **Smart sparse checkouts**: Clone only the files matching your search hits, not entire repos
- **grep.app integration**: Uses the grep.app API to fetch search results
- **Grouped by repo**: Aggregates hits per repository and applies sparse-checkout filters
- **Optional full clone**: Fall back to full repository cloning when needed

## Usage

```sh
# Search and sparse checkout matching files
grepow "your search query" repo_dirs
# Full clone instead of sparse checkout
grepow "your search query" repo_dirs --full
```

### How it works

1.  Queries the grep.app API with your search term
2.  Groups matching files by repository
3.  Clones each repository with `git sparse-checkout`
4.  Applies filter cones for just the matched file paths

## Contributing

Contributions are welcome! Please:

1.  Open an issue to discuss bugs or feature requests
2.  Fork the repo and submit a PR for changes
3.  Install dev dependencies with `uv sync` and run `pre-commit install`

## License

MIT License - see [LICENSE](LICENSE) for details.

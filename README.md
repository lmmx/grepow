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

## Glossary

- **grep.app**: A search engine that indexes GitHub's popular projects (typically those with at
  least a handful of stars) with an API. Try it out at [grep.app](https://grep.app/) for a sense of what it gives you.
- **Sparse checkout**: When git clones only the files matching a 'filter'. We use this to isolate just the search hits from the repos in the results list.
- **Grouped hits**: Rather than somehow having individual search results (files) in separate repo copies, we aggregate multiple hits per repo into a single 'filter set'

## Usage

To search and sparse checkout matching files:

```sh
grepow "your search query" repo_dirs
```

The results will be saved to `repo_dirs` (created if it doesn't exist), cloned into subdirs.

Alternatively, for full repos, pass the `--full` flag.

## Contributing

Contributions are welcome! Please:

1.  Open an issue to discuss bugs or feature requests
2.  Fork the repo and submit a PR for changes
3.  Install dev dependencies with `uv sync` and run `pre-commit install`

## License

MIT License - see [LICENSE](LICENSE) for details.

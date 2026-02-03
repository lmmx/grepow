# grepow

A local CLI for [grep.app](http://grep.app) which `git sparse-checkout`s each repo
with a filter cone over just the hits (or optional full cloning).

grep.app has an API, we use that to pull the hits, group by repo, clone those and then
add filters to the sparse checkout for the file set per repo.

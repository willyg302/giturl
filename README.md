# giturl

A tool for parsing all sorts of Git URLs

## Usage

You can safely do `from giturl import *`. This imports the class `GitURL`.

The usage of giturl is best illustrated through an example:

```python
g = GitURL('gh:willyg302/giturl')

print g.host      # prints "github.com"
print g.owner     # prints "willyg302"
print g.repo      # prints "giturl"

g.to_ssh()        # returns 'git@github.com:willyg302/giturl.git'
g.to_https()      # returns 'https://github.com/willyg302/giturl.git'
g.to_git()        # returns 'git://github.com/willyg302/giturl.git'
g.to_http()       # returns None
g.to('ssh')       # same as g.to_ssh()

g.is_a('github')  # returns True
g.valid           # returns True
```

### Short URLs

giturl is capable of parsing short versions of common Git URLs:

- **GitHub**: `gh:owner/repo`
- **Bitbucket**: `bb:owner/repo`

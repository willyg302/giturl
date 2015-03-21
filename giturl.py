'''
giturl: A tool for parsing all sorts of Git URLs
Repo: https://github.com/willyg302/giturl
'''
import re
import sys


__version__ = '0.2.1'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['GitURL']


PY2 = sys.version_info[0] == 2

def iteritems(d):
	return d.iteritems() if PY2 else d.items()


URL_DICT = {
	'github': {
		'matches': [
			'git://github.com/(?P<owner>.+)/(?P<repo>[^\.]+?)(?:$|\.git)',
			'https://github.com/(?P<owner>.+)/(?P<repo>[^\.]+?)(?:$|\.git)',
			'git@github.com:(?P<owner>.+)/(?P<repo>[^\.]+?)(?:$|\.git)',
			'gh:(?P<owner>.+)/(?P<repo>.+)'
		],
		'host': 'github.com',
		'formatters': {
			'git': 'git://{host}/{owner}/{repo}.git',
			'https': 'https://{host}/{owner}/{repo}',
			'ssh': 'git@{host}:{owner}/{repo}.git'
		}
	},
	'bitbucket': {
		'matches': [
			'https://(?P<owner>.+)@bitbucket.org/(?P=owner)/(?P<repo>[^\.]+?)(?:$|\.git)',
			'git@bitbucket.org:(?P<owner>.+)/(?P<repo>[^\.]+?)(?:$|\.git)',
			'bb:(?P<owner>.+)/(?P<repo>.+)'
		],
		'host': 'bitbucket.org',
		'formatters': {
			'https': 'https://{owner}@{host}/{owner}/{repo}',
			'ssh': 'git@{host}:{owner}/{repo}.git'
		}
	},
	'assembla': {
		'matches': [
			'git://git.assembla.com/(?P<repo>[^\.]+?)(?:$|\.git)',
			'git@git.assembla.com:(?P<repo>[^\.]+?)(?:$|\.git)',
			'as:(?P<repo>.+)'
		],
		'host': 'git.assembla.com',
		'formatters': {
			'git': 'git://{host}/{repo}.git',
			'ssh': 'git@{host}:{repo}.git'
		}
	},
	'gist': {
		'matches': [
			'https://gist.github.com/(?P<owner>.+)/(?P<repo>[^\.]+)(?:$)',
			'gist:(?P<owner>.+)/(?P<repo>.+)'
		],
		'host': 'gist.github.com',
		'formatters': {
			'https': 'https://{host}/{owner}/{repo}'
		}
	}
}

def matches(s, regexes):
	for r in regexes:
		match = re.compile(r).match(s)
		if match:
			return match.groupdict()


class GitURL(object):

	def __init__(self, url):
		for type, d in iteritems(URL_DICT):
			match = matches(url, d['matches'])
			if match:
				self._valid = True
				self._type = type
				self._host = d['host']
				self._owner = match.get('owner')
				self._repo = match.get('repo')
				break;
		else:
			self._valid = False

	@property
	def host(self):
		return getattr(self, '_host', None)

	@property
	def owner(self):
		return getattr(self, '_owner', None)

	@property
	def repo(self):
		return getattr(self, '_repo', None)

	@property
	def valid(self):
		return self._valid

	def is_a(self, type):
		return getattr(self, '_type', None) == type

	def to(self, protocol):
		if not self.valid:
			raise ValueError('Unable to format invalid URL to {}'.format(protocol))
		formatters = URL_DICT[self._type]['formatters']
		if protocol in formatters:
			return formatters[protocol].format(**{
				'host': self._host,
				'owner': self._owner,
				'repo': self._repo
			})

	def to_git(self):
		return self.to('git')

	def to_http(self):
		return self.to('http')

	def to_https(self):
		return self.to('https')

	def to_ssh(self):
		return self.to('ssh')

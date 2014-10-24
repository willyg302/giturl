'''
giturl: A tool for parsing all sorts of Git URLs
Repo: https://github.com/willyg302/giturl
'''
import re


__version__ = '0.1.0'
VERSION = tuple(map(int, __version__.split('.')))

__all__ = ['GitURL']


URL_DICT = {
	'github': {
		'matches': [
			'git://github.com/(?P<owner>.+)/(?P<repo>.+)\.git',
			'https://github.com/(?P<owner>.+)/(?P<repo>.+)\.git',
			'git@github.com:(?P<owner>.+)/(?P<repo>.+)\.git',
			'gh:(?P<owner>.+)/(?P<repo>.+)'
		],
		'host': 'github.com',
		'formatters': {
			'git': 'git://{host}/{owner}/{repo}.git',
			'https': 'https://{host}/{owner}/{repo}.git',
			'ssh': 'git@{host}:{owner}/{repo}.git'
		}
	},
	'bitbucket': {
		'matches': [
			'https://(?P<owner>.+)@bitbucket.org/(?P=owner)/(?P<repo>.+)\.git',
			'git@bitbucket.org:(?P<owner>.+)/(?P<repo>.+)\.git',
			'bb:(?P<owner>.+)/(?P<repo>.+)'
		],
		'host': 'bitbucket.org',
		'formatters': {
			'https': 'https://{owner}@{host}/{owner}/{repo}.git',
			'ssh': 'git@{host}:{owner}/{repo}.git'
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
		for type, d in URL_DICT.iteritems():
			match = matches(url, d['matches'])
			if match:
				self._valid = True
				self._type = type
				self._host = d['host']
				self._owner = match['owner']
				self._repo = match['repo']
				break;
		else:
			self._valid = False

	@property
	def host(self):
		return self._host

	@property
	def owner(self):
		return self._owner

	@property
	def repo(self):
		return self._repo

	@property
	def valid(self):
		return self._valid

	def is_a(self, type):
		return self._type == type

	def to(self, protocol):
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

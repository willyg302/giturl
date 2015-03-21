import unittest

from giturl import *


VALID_URLS = [
	{
		'urls': [
			'git://github.com/owner/repo.git',
			'https://github.com/owner/repo.git',
			'git@github.com:owner/repo.git',
			'git://github.com/owner/repo',
			'https://github.com/owner/repo',
			'git@github.com:owner/repo',
			'gh:owner/repo'
		],
		'host': 'github.com',
		'type': 'github',
		'owner': 'owner',
		'rewrites': [
			('ssh', 'git@github.com:owner/repo.git'),
			('https', 'https://github.com/owner/repo'),
			('git', 'git://github.com/owner/repo.git'),
			('http', None)
		]
	},
	{
		'urls': [
			'https://owner@bitbucket.org/owner/repo.git',
			'git@bitbucket.org:owner/repo.git',
			'https://owner@bitbucket.org/owner/repo',
			'git@bitbucket.org:owner/repo',
			'bb:owner/repo'
		],
		'host': 'bitbucket.org',
		'type': 'bitbucket',
		'owner': 'owner',
		'rewrites': [
			('ssh', 'git@bitbucket.org:owner/repo.git'),
			('https', 'https://owner@bitbucket.org/owner/repo'),
			('git', None),
			('http', None)
		]
	},
	{
		'urls': [
			'git://git.assembla.com/repo.git',
			'git@git.assembla.com:repo.git',
			'git://git.assembla.com/repo',
			'git@git.assembla.com:repo',
			'as:repo'
		],
		'host': 'git.assembla.com',
		'type': 'assembla',
		'owner': None,
		'rewrites': [
			('ssh', 'git@git.assembla.com:repo.git'),
			('https', None),
			('git', 'git://git.assembla.com/repo.git'),
			('http', None)
		]
	},
	{
		'urls': [
			'https://gist.github.com/owner/repo',
			'gist:owner/repo'
		],
		'host': 'gist.github.com',
		'type': 'gist',
		'owner': 'owner',
		'rewrites': [
			('ssh', None),
			('https', 'https://gist.github.com/owner/repo'),
			('git', None),
			('http', None)
		]
	}
]

INVALID_URLS = [
	'git@github.com:owner',
	'get@github.com:owner/repo.git',
	'git@github.com:owner/repo.get',
	'https://owner@bitbucket.org/notowner/repo.git',
	'git://bitbucket.org/owner.repo.git',
	'git@assembla.com:repo.git',
	'https://git.assembla.com/repo.git',
	'https://gist.github.com/owner/repo.git'
]


class TestParse(unittest.TestCase):

	def test_valid_urls(self):
		for e in VALID_URLS:
			for url in e['urls']:
				g = GitURL(url)
				self.assertTrue(g.valid)
				self.assertEqual(g.host, e['host'])
				self.assertEqual(g.owner, e['owner'])
				self.assertEqual(g.repo, 'repo')
				self.assertTrue(g.is_a(e['type']))

	def test_invalid_urls(self):
		for url in INVALID_URLS:
			g = GitURL(url)
			self.failIf(g.valid)
			for e in [g.host, g.owner, g.repo]:
				self.assertIsNone(e)
			with self.assertRaises(ValueError):
				g.to_git()


class TestRewrite(unittest.TestCase):

	def test_rewrite_urls(self):
		for e in VALID_URLS:
			for url in e['urls']:
				g = GitURL(url)
				for protocol, expected in e['rewrites']:
					self.assertEqual(g.to(protocol), expected)


if __name__ == '__main__':
	unittest.main()

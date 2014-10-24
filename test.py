import unittest

from giturl import *


VALID_URLS = [
	{
		'url': 'gh:owner/repo',
		'host': 'github.com',
		'type': 'github',
		'rewrites': [
			('ssh', 'git@github.com:owner/repo.git'),
			('https', 'https://github.com/owner/repo.git'),
			('git', 'git://github.com/owner/repo.git'),
			('http', None)
		]
	},
	{
		'url': 'https://owner@bitbucket.org/owner/repo.git',
		'host': 'bitbucket.org',
		'type': 'bitbucket',
		'rewrites': [
			('ssh', 'git@bitbucket.org:owner/repo.git'),
			('https', 'https://owner@bitbucket.org/owner/repo.git'),
			('git', None),
			('http', None)
		]
	}
]

INVALID_URLS = [
	'git@github.com:owner',
	'get@github.com:owner/repo.git',
	'https://owner@bitbucket.org/notowner/repo.git'
]


class TestParse(unittest.TestCase):

	def test_valid_urls(self):
		for e in VALID_URLS:
			g = GitURL(e['url'])
			self.assertTrue(g.valid)
			self.assertEqual(g.host, e['host'])
			self.assertEqual(g.owner, 'owner')
			self.assertEqual(g.repo, 'repo')
			self.assertTrue(g.is_a(e['type']))

	def test_invalid_urls(self):
		for url in INVALID_URLS:
			g = GitURL(url)
			self.failIf(g.valid)


class TestRewrite(unittest.TestCase):

	def test_rewrite_urls(self):
		for e in VALID_URLS:
			g = GitURL(e['url'])
			for protocol, expected in e['rewrites']:
				self.assertEqual(g.to(protocol), expected)


if __name__ == '__main__':
	unittest.main()

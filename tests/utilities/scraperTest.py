import unittest

from spirecomm.spire.character import PlayerClass

from utilities.scraping import Scraper

class TestScraper(unittest.TestCase):
	def test_creates_folders_on_start(self):
		scraper = Scraper(PlayerClass.DEFECT)

if __name__ == '__main__':
	unittest.main()
'''
Created on 2015/10/28

@author: michael
'''
import unittest
from newsdog import NewsDog

import os
# Run tests within the NewsDog directory
os.chdir('../')

class TestSuite(unittest.TestCase):

    def setUp(self):
        self.newsdog_object = NewsDog()

    def testNoEntries(self):
        self.newsdog_object.add_geohit('New Zealand')
        self.assertIn(['New Zealand', 1], self.newsdog_object.geohits)
        
    def testExistingEntryIncrement(self):
        self.newsdog_object.add_geohit('Japan') # Add once
        self.newsdog_object.add_geohit('Japan') # This should increment 1->2
        self.assertIn(['Japan', 2], self.newsdog_object.geohits)
        
    def testFindCountry(self):
        self.newsdog_object.geo_sources('Caymanians are everywhere.')
        self.assertIn(['Cayman Islands', 1], self.newsdog_object.geohits)

    def testMultipleCountries(self):
        self.newsdog_object.geo_sources('The Englishman said hi to the Frenchwoman.')
        self.assertIn(['England', 1], self.newsdog_object.geohits)
        self.assertIn(['France', 1], self.newsdog_object.geohits)
        
    def tearDown(self):
        unittest.TestCase.tearDown(self)

if __name__ == "__main__":
    #import sys;sys.argv = ['', 'Test.testName']
    unittest.main()
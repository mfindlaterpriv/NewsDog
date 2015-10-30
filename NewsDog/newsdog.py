#-*- coding: utf-8 -*-
'''
Created on 2015/10/26 by Michael Findlater
NewsDog
'''
import praw
import codecs
import string
from ftfy import fix_text
from newspaper import Article

from redditor import Redditor

# TODO:    
#    Migrate reddit functionality to Redditor class.
#    Add additional functionality.
#    Clean up code.

# Configuration
SUBREDDIT = 'worldnews'
GEOSOURCE_COUNTRY = 'geodata/GEODATASOURCE-COUNTRY.TXT'
DEMS = 'geodata/demonyms.txt'
        
class NewsDog():
    geohits = [] # (country, count)
    def __init__(self):
        pass
            
    def get_news(self, limit=5, source='reddit'):
        '''Gets news from source (default is reddit)'''
        if source is 'reddit':
            reddit = Redditor()
            for link in reddit.analyze_day(limit):
                self.get_article(link)
        else:
            print('No source selected!')

    def add_geohit(self, place):
        # If exists, increment
        results = [n for n in self.geohits if n[0] == place]
        if results:
            self.geohits[self.geohits.index(results[0])][1] += 1
        # If not, create
        else:
            self.geohits.append([place, 1])
            
    def geo_sources(self, text):
        '''Processes input text to remove punctuation, then searches the text for
        references to countries. This data is then sent to self.add_geohit().'''
        # Remove punctuation
        remove_punct_map = dict.fromkeys(map(ord, string.punctuation))
        text = text.replace('\n', ' ').translate(remove_punct_map)
        
        country_data = []
        country_file = codecs.open(GEOSOURCE_COUNTRY, 'r', encoding='utf-8')
        
        # TODO: move this to __init__.
        # Read country data file into memory
        for line in country_file.read().split('\n'):
            line_split = line.split('\t')
            if len(line_split)-1 == 3 and 'COUNTRY_NAME' not in line:
                country_data.append( (line_split[0], 
                                      line_split[1], 
                                      line_split[2], 
                                      line_split[3].strip('\r')) )
        country_file.close()
        
        
        text_split = text.split(' ')
        found_match = False
        # Search each word to find any references to countries
        for word in text_split:
            for row in country_data:
                # Match: if the country name itself is in the word
                if row[3] in word:
                    self.check_country(word)
                    found_match = True
                # Match: if the country name is written verbatim
                elif (text_split.index(word)+1 <= len(text_split)-1 and 
                      word+' '+text_split[text_split.index(word)+1] == row[3]):
                    self.check_country(word+' '+text_split[text_split.index(word)+1])
                    found_match = True
                    
            # If we still haven't found something, check for a demonym
            # Checking this is handled by self.check_country()
            if not found_match:
                self.check_country(word)
    
    def get_article(self, url):
        '''Retrieves the text of a news article, given its URL'''
        article = Article(url)
        article.download()
        article.parse()
        self.geo_sources(fix_text(article.text))
    
    def geo_csv(self):
        '''Prints data from self.geohits in CSV format'''
        for item in self.geohits:
            print(item[0]+', '+str(item[1]))
            
    def check_country(self, name):
        '''Checks to see whether 'name' matches a demonym of any countries.
        If it does, the country is passed to self.add_geohit()''' 
        name = name.lower()
        c_defs = codecs.open(DEMS, 'r', encoding='utf-8')
        for line in c_defs.read().split('\n'):
            # Separate elements
            for element in line.split(','):
                if name == element.lower():
                    # Add a match, and exit while loop
                    self.add_geohit(line.split(',')[0])
        c_defs.close()

def main():
    nd = NewsDog()
    nd.get_news(limit=10)
    nd.geo_csv()

if __name__ == '__main__': main()
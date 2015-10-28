'''
Created on 2015/10/28

Handles NewsDog's connections and searches to reddit, using praw

@author: michaelfindlater
'''
import praw

# Configuration
SUBREDDIT = 'worldnews'
        
class Redditor():
    def __init__(self):
        '''Establishes a connection to Reddit'''
        self.reddit = praw.Reddit(user_agent='NewsDog')
            
    def analyze_day(self, limit=5):
        submissions = self.reddit.get_subreddit(SUBREDDIT).get_top_from_day(limit=limit)
        for post in submissions:
            print(post)
            print(post.url)
            # Ignore links to reddit itself (against r/worldnews rules anyway)
            if 'www.reddit.com' not in post.url:
                self.get_article(post.url)

def main():
    nd = NewsDog()
    nd.analyze_day(limit=100)
    nd.geo_csv()

if __name__ == '__main__': main()
import argparse
import pandas as pd
import warnings as w
from config import dict_options, cookies
from utils import  get_logger
from facebook_scraper import get_posts, get_posts_by_search
logger = get_logger('facebook_post')
w.filterwarnings('ignore')
def scrape_posts(query_list, pages, cookies_file, options, type_scraper='account'):
    post_list = []
    for query in query_list:
        if type_scraper == 'account':
            for post in get_posts(account = query, pages = pages, cookies = cookies_file, options = options):
                post['text'] = post['text'].split('\n',1)[0]
                logger.info(f"{post['time']} | {post['text']}")
        if type_scraper == 'hashtag':
            for post in get_posts(hashtag = query, pages = pages, cookies = cookies_file, options = options):
                post['text'] = post['text'].split('\n',1)[0]
                logger.info(f"{post['time']} | {post['text']}")
        if type_scraper == 'word':
            for post in get_posts(word = query, pages = pages, cookies = cookies_file, options = options):
                post['text'] = post['text'].split('\n',1)[0]
                logger.info(f"{post['time']} | {post['text']}")
        post_list.append(post)
    df_posts = pd.DataFrame(post_list)
    return df_posts

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--query', '-q',
                        dest = 'query',
                        help = 'indicar los query de cuenta a extraer')
    args = parser.parse_args()
    query_list = args.query.strip().split()
    logger.info(query_list)
    posts = scrape_posts(query_list, cookies_file = cookies, 
                        pages = 3, options = dict_options)
    posts.to_pickle('../results/posts.pkl')















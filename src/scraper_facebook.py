import argparse
import time
import pandas as pd
import warnings as w
from config import dict_options, cookies, PAGES
from utils import  get_logger
from facebook_scraper import get_posts, get_posts_by_search

logger = get_logger('facebook_post')
w.filterwarnings('ignore')

def scrape_posts(query_list, pages, cookies_file, options, method):
    post_list = []
    for query in query_list:
        if method == 'account':
            for post in get_posts(account = query, pages = pages, cookies = cookies_file, options = options):
                post['text'] = post['text'].split('\n',1)[0]
                logger.info(f"{post['time']} | {post['text']}")
                post_list.append(post)

        if method == 'hashtag':
            for post in get_posts(hashtag = query, pages = pages, cookies = cookies_file, options = options):
                post['text'] = post['text'].split('\n',1)[0]
                logger.info(f"{post['time']} | {post['text']}")
                post_list.append(post)

        if method == 'word':
            for post in get_posts(word = query, pages = pages, cookies = cookies_file, options = options):
                post['text'] = post['text'].split('\n',1)[0]
                logger.info(f"{post['time']} | {post['text']}")
                post_list.append(post)

    df_posts = pd.DataFrame(post_list)
    return df_posts

def main():
    query_list = args.query.strip().split()
    logger.info(query_list)

    start_time  = time.time()
    posts = scrape_posts(query_list, cookies_file = cookies, 
                        pages = PAGES, options = dict_options, method = args.method)
    end_time = time.time()
    logger.info(f'segundos transcurridos : {end_time - start_time}')
    posts.to_pickle('../results/posts.pkl')


if __name__=='__main__':
    parser = argparse.ArgumentParser()

    parser.add_argument('--query', '-q',
                        dest = 'query',
                        help = 'indicar los query de cuenta a extraer')
    parser.add_argument('--method', '-m',
                        dest='method', 
                        help='indicar el tipo de metodo para extraer los post',
                        choices=['account', 'hashtag', 'word'],
                        default='account')

    args = parser.parse_args()
    main()
    

















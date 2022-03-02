import argparse
import pandas as pd
import numpy as np
from utils import get_logger
logger = get_logger('preprocessing')


class GetComment:
    def __init__(self, comments_full, root_id):
        self.data = []
        self.root_id = root_id
        self._get_fields(comments_full, root_id)
    def _get_fields(self, comments_full, parent_id):
        for dict_comment in comments_full:
            dict_comment['root_id'] = self.root_id
            dict_comment['parent_id'] = parent_id
            self.data.append(dict_comment)
            if dict_comment.get('replies'):
                replies = dict_comment['replies']
                if replies:
                    self._get_fields(replies, parent_id = dict_comment['comment_id'])


def main():
    df = pd.read_pickle(args.data)
    keep_columns = ['post_id', 'post_text', 'time', 'image', 'likes', 'comments', 'shares','post_url',
                    'user_id', 'username', 'user_url', 'comments_full','reactions', 'reaction_count']
    df = df[keep_columns].copy()

    list_dict_public = []
    list_dict_comments_full = []
    for index, row in df.iterrows():
        dict_public = {}
        for column in df.columns:
            if 'reactions' == column and row['reactions']:
                for i in row[column]:
                    column_reactions = f'reactions_{i}'
                    dict_public[column_reactions] = row[column][i]
                continue
            if 'comments_full' == column and row['comments_full']:
                get_comment = GetComment(row['comments_full'], root_id = row['post_id'])
                list_dict_comments_full.extend(get_comment.data)
                continue
            if row[column]:
                dict_public[column] = row[column]
        list_dict_public.append(dict_public)
    df_post = pd.DataFrame(list_dict_public).replace({np.nan:None})
    df_comment = pd.DataFrame(list_dict_comments_full)
    df_comment.drop(['comment_reactors', 'replies'], axis=1, inplace=True)
    logger.info('\n{}'.format(df_post))
    logger.info('\n{}'.format(df_comment))

if __name__=='__main__':
    parser = argparse.ArgumentParser()
    parser.add_argument('--data','-d',
                        dest ='data',
                        help = 'indicar la data a procesar',
                        )
    args = parser.parse_args()
    main()




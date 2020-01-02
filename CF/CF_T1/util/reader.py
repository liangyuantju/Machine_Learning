#-*-coding:utf8-*-
"""
author:liangyuan
date:20191018
"""
import os
import sys
import csv

def get_user_click(rating_file, rating_limit):
    """
    get user click list
    Args:
        rating_file: input file
        rating_limit: if rating great than rating_limit, user like this item
    Return:
        dict, key:userid, value:[itemid1, itemid2]
    """
    if not os.path.exists(rating_file):
        print("rating file not exists")
        return {},{}
    user_click = {}
    user_click_time = {}
    num = 0
    with open(rating_file, "r", encoding="utf-8") as fp:
        read = csv.reader(fp)
        for line in read:
            if num == 0:
                num += 1
                continue
            if len(line) < 4:
                continue
            [userid, itemid, rating, timestamp] = line
            if userid + "_" + itemid not in user_click_time:
                user_click_time[userid + "_" + itemid] = int(timestamp)
            if float(rating) < rating_limit:
                continue
            if userid not in user_click:
                user_click[userid] = []
            user_click[userid].append(itemid)
    return user_click, user_click_time

def get_item_info(item_file):
    """
    get item info[title, genres]
    Args:
        item_file:input iteminfo file
    Return:
        a dict, key itemid, value:[title, genres]
    """
    if not os.path.exists(item_file):
        return {}
    
    item_info = {}
    num = 0
    with open(item_file, "r", encoding="utf-8") as fp:
        read = csv.reader(fp)
        for line in read:
            if num == 0:
                num += 1
                continue
            if len(line) < 3:
                continue
            [movieId, title, genres] = line
            if movieId not in item_info:
                item_info[movieId] = [title, genres]
    return item_info

if __name__ == "__main__":
    # user_click = get_user_click("C:/Users/Lenovo/Desktop/CF/CF_T1/data/ratings.txt")
    os.chdir(sys.path[0])
    # user_click = get_user_click("../data/ratings.csv", 3.0)
    # print("user's len = %d" % (len(user_click)))
    # print(user_click["1"])

    movies_info = get_item_info("../data/movies.csv")
    print("movies_info rows = %d" % len(movies_info))
    print('movies_info[141]:', movies_info["141"])

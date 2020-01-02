#-*-coding:utf8-*-
"""
user cf main algo
author liangyuan
date 20191126
"""
from __future__ import division
import sys
import os
import math
import operator
os.chdir(sys.path[0])
sys.path.append("../")
from util import reader as reader

def transfer_user_click(user_click):
    """
    transfer user_click to item_click_by_user
    Args:
      user_click:dict key user value value [itemid1, itemid2, ...]
    Return:
      item_click_by_user:dict key itemid value [userid1, userid2, userid3, ...]
    """
    item_click_by_user = {}
    for [userid, itemlist] in user_click.items():
        for itemid in itemlist:
            item_click_by_user.setdefault(itemid, [])
            item_click_by_user[itemid].append(userid)
    return item_click_by_user

def base_contribute_score():
    """
    usercf base contribute sim score
    """
    return 1

def update_contribution_score(item_user_click_cnt):
    """
    reduce contribution for activity item
    Args:
      item_user_click_cnt:int how many user has clicked this item
    Return:
      sim score contribution
    """ 
    return 1/math.log10(1+item_user_click_cnt)

def update_contribution_score_v2(click_time_one, click_time_two):
    """
    Args:
      different user action time to the same item:click_time_one、click_time_two 
    Return:
      sim score contribution
    """
    delta_time = abs(click_time_one - click_time_two)
    total_sec  = 24*60*60
    delta_time = delta_time/total_sec
    return 1/(1 + delta_time)

def cal_user_sim(item_click_by_user, user_click_time):
    """
    Args:
      item_click_by_user:dict key:itemid value:[userid1, userid2, userid3, ...]
      user_click_time:
    Return:
      user_sim dict, key:userid_i value:dict, value_key:userid_j value_value:simscore
    """
    co_appear = {}
    user_click_cnt = {}  # Record how many items the user clicks on
    for [itemid, userlist] in item_click_by_user.items():
        for index_i in range(len(userlist)):
            user_i = userlist[index_i]
            user_click_cnt.setdefault(user_i, 0)
            user_click_cnt[user_i] += 1
            if user_i + '_' + itemid not in user_click_time:
                click_time_one = 0
            else:
                click_time_one = user_click_time[user_i + '_' + itemid]
            for index_j in range(index_i+1, len(userlist)):
                user_j = userlist[index_j]
                if user_j + '_' + itemid not in user_click_time:
                    click_time_two = 0
                else:
                    click_time_two = user_click_time[user_j + "_" + itemid]
                co_appear.setdefault(user_i, {})
                co_appear[user_i].setdefault(user_j, 0)
                # co_appear[user_i][user_j] += base_contribute_score()
                # co_appear[user_i][user_j] += update_contribution_score(len(userlist))
                co_appear[user_i][user_j] += update_contribution_score_v2(click_time_one, click_time_two)

                co_appear.setdefault(user_j, {})
                co_appear[user_j].setdefault(user_i, 0)
                # co_appear[user_j][user_i] += base_contribute_score()
                # co_appear[user_j][user_i] += update_contribution_score(len(userlist))
                co_appear[user_j][user_i] += update_contribution_score_v2(click_time_one, click_time_two)
    
    user_sim_info = {}
    user_sim_info_sorted = {}
    for [user_i, relate_users] in co_appear.items():
        user_sim_info.setdefault(user_i, {})
        for [user_j, cotime] in relate_users.items():
            user_sim_info[user_i].setdefault(user_j, 0)
            user_sim_info[user_i][user_j] = cotime/math.sqrt(user_click_cnt[user_i] * user_click_cnt[user_j])
    for user in user_sim_info:
        user_sim_info_sorted[user] = sorted(user_sim_info[user].items(), key=operator.itemgetter(1), reverse=True)
    
    return user_sim_info_sorted 

def cal_recom_result(user_click, user_sim):
    """
    Args:
      user_click:dict, key:userid value:[itemid1, itemid2]
      user_sim::dict, key:userid_i value:[(userid_j, simscore1), (userid_k, simscore2)]
    Return:
      dict, key:userid value dict, value_key:itemid, value_value:simscore
    """
    recom_result = {}
    topk_user = 3
    item_num = 5
    for [user, itemlist] in user_click.items():
        tmp_dict = {}
        for itemid in itemlist:
            tmp_dict.setdefault(itemid, 1)
        recom_result.setdefault(user, {})
        for zuhe in user_sim[user][:topk_user]:
            userid_j, simscore = zuhe
            if userid_j not in user_click:
                continue
            for itemid_j in user_click[userid_j][:item_num]:
                if itemid_j in tmp_dict: # filter item that clicked by user
                    continue
                recom_result[user].setdefault(itemid_j, simscore)
    
    return recom_result

def debug_user_sim(user_sim):
    """
    print user sim result
    Args:
      user_sim:dict key userid_i value[(userid1, score1), (userid2, socre2),...]
    """
    topk = 5
    fix_user = "1"
    if fix_user not in user_sim:
        print("invalid user")
        return
    for zuhe in user_sim[fix_user][:topk]:
        userid, score = zuhe
        print("userid : %s\tsim_user : %s\t%s" % (fix_user, userid, score))

def debug_recom_result(item_info, recom_result):
    """
    print recom result for user
    Args:
      item_info   : dict key:itemid value:[title, genres]
      recom_result: dict key:userid value:dict value_key:itemid value_value:recom_score
    """
    fix_user = "1"
    if fix_user not in recom_result:
        print("invalid user for recoming result")
        return
    for itemid in recom_result[fix_user]:
        if itemid not in item_info:
            continue
        recom_score = recom_result[fix_user][itemid]
        print("recom_result:"+".".join(item_info[itemid])+"\t"+str(recom_score))


def main_flow():
    """
    user cf main flow
    """
    user_click, user_click_time = reader.get_user_click("../data/ratings.csv", 1)
    item_info = reader.get_item_info("../data/movies.csv")
    item_click_by_user = transfer_user_click(user_click)
    user_sim = cal_user_sim(item_click_by_user, user_click_time)
    debug_user_sim(user_sim)
    recom_result = cal_recom_result(user_click, user_sim)
    # print(recom_result["1"])
    debug_recom_result(item_info, recom_result)

if __name__ == "__main__":
    main_flow()


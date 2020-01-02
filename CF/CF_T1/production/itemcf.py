#-*-coding:utf8-*-
"""
item cf main Algo 
author:liangyuan 
date:20191122
"""

from __future__ import division
import sys
import os
import math
import operator
os.chdir(sys.path[0])
sys.path.append("../")
from util import reader as reader

def base_contribute_score():
   """
   item cf base sim contribution score by user
   """
   return 1

def update_one_contribute_score(user_total_click_num):
   """
   item cf update sim contribution by user 
   """
   return 1/math.log10(1 + user_total_click_num)

def update_two_contribute_score(click_time_one, click_time_two):
   """
   item cf update two sim contribution by user
   """
   delta_time = abs(click_time_one - click_time_two)
   total_sec = 24*60*60 # 将秒转化为天，对数值进行规约
   delta_time = delta_time/total_sec
   return 1/(1 + delta_time)


def cal_item_sim(user_click, user_click_time):
   """
   Args:
     user_click:dict, key:userid, value[itemid1, itemid2,..]
   Return:
     dict, key:itemid_i, value dict, value_key:itemid_j, value_value:simscore
   """
   co_appear = {}
   item_user_click_time = {}  #用来记录itemid被多少user点击过
   for user, itemlist in user_click.items():
      for index_i in range(0, len(itemlist)):
         itemid_i = itemlist[index_i]
         item_user_click_time.setdefault(itemid_i, 0)
         item_user_click_time[itemid_i] += 1
         for index_j in range(index_i+1, len(itemlist)):
            itemid_j = itemlist[index_j]
            if user + "_" + itemid_i not in user_click_time:
               click_time_one = 0
            else:
               click_time_one = user_click_time[user + "_" + itemid_i]
            if user + "_" + itemid_j not in user_click_time:
               click_time_two = 0
            else:
               click_time_two = user_click_time[user + "_" + itemid_j]
            co_appear.setdefault(itemid_i, {})
            co_appear[itemid_i].setdefault(itemid_j, 0)
            # co_appear[itemid_i][itemid_j] += base_contribute_score()
            # co_appear[itemid_i][itemid_j] += update_one_contribute_score(len(itemlist))
            co_appear[itemid_i][itemid_j] += update_two_contribute_score(click_time_one, click_time_two)

            co_appear.setdefault(itemid_j, {})
            co_appear[itemid_j].setdefault(itemid_i, 0)
            # co_appear[itemid_j][itemid_i] += base_contribute_score()
            # co_appear[itemid_j][itemid_i] += update_one_contribute_score(len(itemlist))
            co_appear[itemid_j][itemid_i] += update_two_contribute_score(click_time_one, click_time_two)
   item_sim_score = {}
   item_sim_score_sorted = {}
   for itemid_i, relate_item in co_appear.items():
      for itemid_j, co_time in relate_item.items():
         sim_score = co_time/math.sqrt(item_user_click_time[itemid_i]*item_user_click_time[itemid_j])
         item_sim_score.setdefault(itemid_i, {})
         item_sim_score[itemid_i].setdefault(itemid_j, 0)
         item_sim_score[itemid_i][itemid_j] = sim_score
   for itemid in item_sim_score:
      item_sim_score_sorted[itemid] = sorted(item_sim_score[itemid].items(), key=operator.itemgetter(1), reverse=True) #使用排序，字典形式将变成元组组成的列表
      
   return item_sim_score_sorted

def cal_recom_result(sim_info, user_click):
   """
   recom by itemcf
   Args:
     sim_info: item sim dict
     user_click: user click dict
   Return:
     dict, key userid, value dict, value_key itemid, value_value: recom_score
   """
   recent_click_num = 3 
   topk = 5
   recom_info = {}
   for user in user_click:
      click_list = user_click[user]
      recom_info.setdefault(user, {})
      for itemid in click_list[:recent_click_num]:
         if itemid not in sim_info:
            continue
         for itemsimzuhe in sim_info[itemid][:topk]:
            itemsimid = itemsimzuhe[0]
            itemsimscore = itemsimzuhe[1]
            recom_info[user][itemsimid] = itemsimscore
   return recom_info

def debug_itemsim(item_info, sim_info):
   """
   show itemsim info
   Args:
     item_info:dict key itemid value:[title. genres]
     sim_info:dict key itemid, value list [(itemid1, simscore1), (itemid2, simscore2)] 
   """
   fixed_itemid = "1"
   if fixed_itemid not in item_info:
      print("invalid_itemid")
      return
   [title_fix, genres_fix] = item_info[fixed_itemid]
   for zuhe in sim_info[fixed_itemid][:5]:
      itemid_sim = zuhe[0]
      simscore = zuhe[1]
      if itemid_sim not in item_info:
         continue
      [title, genres] = item_info[itemid_sim]
      print("%s\t%s\tsim:%s\t%s\t%s" % (title_fix, genres_fix, title, genres, str(simscore)))

def debug_recomresult(recom_result, item_info): 
   """
   debug recom result
   Args:
     recom_result: dict key userid value dict, value_key itemid value_value recom_score 
     item_info: dict key itemid value:[title, genre]
   """
   user_id = "1"
   if user_id not in recom_result:
      print("invalid result")
      return 
   for zuhe in sorted(recom_result[user_id].items(), key=operator.itemgetter(1), reverse=True):
      itemid, score = zuhe
      if itemid not in item_info:
         continue
      print(",".join(item_info[itemid]) + "\t" + str(score))

def main_flow():
   """
   main flow of itemcf
   """ 
   user_click, user_click_time = reader.get_user_click("../data/ratings.csv", 1)
   item_info = reader.get_item_info("../data/movies.csv")
   sim_info = cal_item_sim(user_click, user_click_time)
   debug_itemsim(item_info, sim_info)
   # recom_result = cal_recom_result(sim_info, user_click)
   # print(recom_result["1"])
   # debug_recomresult(recom_result, item_info)

if __name__ == "__main__":
   main_flow()
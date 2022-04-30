#! /usr/bin/env python
# coding=utf-8

import csv
import sys
import redis
import json
import requests
import os
import time
import math
import MySQLdb
import zipfile
import urllib.parse
import etcd3


data, path = etcd3.client(host='127.0.0.1', port=2379).get("/service/game_server/5/1")
http_addr = json.loads(data.decode())["http_api_addr"]


def print_etecd_key():
    print(path.key.decode())


r = redis.StrictRedis(host='127.0.0.1', port=6379, db=9)
# # r.zadd("wulala:practice_job_rank:0:1:16",=1234)
# # r.zadd("wulala:practice_job_rank:0:1:16", 'm1', 22)
# # {\"ActionItemId\":62388,\"Head\":63524,\"HeadSculpture\":35,\"ChatBubble\":63517,\"Pid\":24577,\"RoleId\":20,\"PrepRoleId\":20,\"Nick\":\"sczc\",\"Level\":50,\"FightNum\":9019,\"Points\":3301}
# pid = 8193
# for i in range(1, 1050000):
#     pid += 8193
#     role = 18
#     n = 262144 + i
#     key = '{\"Pid\":' + str(pid) + ',\"RoleId\":' + str(role) + ',\"PrepRoleId\":' + str(role) + ',\"Nick\":\"ci110\",\"Level\":81,\"FightNum\":839251,\"Points\":' + str(1 + i) + '}'
#     key = str(pid)
#     r.zadd('wulala:practice_job_rank:0:1:18:1', {
#         key: n
#     })

# r.zrevrange('wulala:practice_job_rank:0:1:18:1', 0, -1)

# with open(str(sys.argv[1]),'r') as f:
#     reader = csv.reader(f)
#     print(type(reader))
#
#     for row in reader:
#         print len(row)
#         print row[0],row[1]



def insertTeamDatas():
    tmpDadta = []
    # filedir = "/Users/smakry/Downloads/1.6版本大佬玩家"
    filedir = "/Users/smakry/Downloads/2022-02-21T03_01_45.206Z_player_data"

    list = os.listdir(filedir)
    for i in range(0, len(list)):
        path = os.path.join(filedir, list[i])
        with open(path,'r') as f:
            reader = f.readlines()

            print(type(reader),type(json.dumps(reader)))
            tmpDadta.append("".join(reader)) # list转str

    data = {
        "datas": tmpDadta,
    }

    # url = "{}/1.0/copy/insert_datas".format("http://10.30.40.66:56443")
    url = "{}/1.0/copy/insert_datas".format(http_addr)
    response = requests.post(url=url,json=data)
    if response.status_code != 200:
        print("erro!!!!",response)

# insertTeamDatas()

# for i in range(1,10):
#     insertTeamDatas()



def insertEliteRankData():
    r = redis.StrictRedis(host='172.16.22.64', port=19004, db=0)
    for i in range(1, 94):
        n = 8192
        n = n + i
        role = 18
        key = '{\"Pid\":'+ str(n) +',\"RoleId\":23,\"PrepRoleId\":23,\"Nick\":\"robot14\",\"Level\":80,\"Time\":1602412723,\"MissionId\":7}'
        r.zadd('wulala:elite_global:190',{
            key : 32757325644
            })

# insertEliteRankData()

def sql_connect():
    # 打开数据库连接
    db = MySQLdb.connect("localhost", "root", "aaa", "team_place4", charset='utf8' )
    # 使用cursor()方法获取操作游标
    cursor = db.cursor()
    # 使用execute方法执行SQL语句
    cursor.execute("SELECT * FROM global_mission_team_player WHERE pid = nick order by id;")
    # # 使用 fetchone() 方法获取一条数据
    # data = cursor.fetchone()
    # print "Database version : %s " % data

    # 关闭数据库连接
    db.close()
    return cursor

def postGetData():
    data = {
        "RechargeTime": 1600401719,
        "ProductId": "wula6",
    }
    url = "{}/1.0/order/get_first_recharge_start_time".format("http://10.30.40.197:65351")

    data = {"key":"value"}
    res = requests.post(url=url,json=data)
    print(res.text)

# postGetData()


# def releasePet():
#     mail_param = {
#         "player_pet_ids": [40951837],
#         "is_adjective": True,
#         "player_id":3989533,
#     }
#     url = 'http://dev02.wll:43049/1.0/pet/release_pet?{}'.format(json.dumps(mail_param))
#     response = requests.get(url, timeout=10)
#     if response.status_code != 200 {
#         print("erro!!!!")
#     }

# releasePet()

def testRedisMemory():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=3)
    for i in range(11, 3000000):
        r.set("wulala:elite2:{}".format(i),"12345678911")
        # r.hset("wulala:elite2:",i,"12345678911")
# testRedisMemory()


def postServerMail():
    gifts = [
       {
        "ItemId": 53137, # 高级淬炼券
        "Number": 5,
        },
        {
        "ItemId": 63502, # 随机16级宝石
        "Number": 1,
        },
        {
        "ItemId": 63316, # 远古英雄之魂
        "Number": 5,
        },
        {
        "ItemId": 63224, # 赛季通行证积分
        "Number": 200,
        },
    ]

    mail_param = {
        "MessageId": 18,
        "EffectTime": 1598341000, #2020-08-25 15:36:40
        "PlayerExpireTime": 1754150400, #2025-08-03 00:00:00
        "MultiLang": [],
        "Gifts":gifts,
        "GmSendId":6,
        "FilterPlayerIds":[49153],
    }
    mail_param["MultiLang"].append({
                "language": 6,
                "title": "",
                "content": "这是王者之战测试",
            })
    url = "{}/1.0/player/server_send_mail".format("http://172.16.22.67:25414")

    res = requests.post(url=url,json=mail_param)
    print(res.text)
# postServerMail()

def optMailFilter():
    filterPids = [24577]
    data = {
        "FilterPlayerIdsStr": filterPids,
        "GmSendId": 2,
        "OptType":0,
    }
    url = '{}/1.0/player/opt_mail_filter_pids?{}'.format("http://172.16.22.111:35854",json.dumps(data))
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!")


# optMailFilter()


	# var req struct {
	# 	Content         string         `json:"Content"`
	# 	ServerId        uint8          `json:"ServerId"`
	# 	AllServer       int8           `json:"AllServer"`
	# 	PlayerIds       []int64        `json:"PlayerIds"`
	# 	Type            int8           `json:"Type"`
	# 	Items           string         `json:"Items"`
	# 	EffectTime      int64          `json:"EffectTime"`
	# 	ExpireTime      int64          `json:"ExpireTime"`
	# 	MultiLang       []multiLangReq `json:"MultiLang"`
	# 	GmSendId        int64          `json:"GmSendId"`
	# 	FilterPlayerIds []int64        `json:"FilterPlayerIds"`
	# }
# item/change

def optMailFilter2():
    filterPids = [24577]

    gifts = [
        {
            "ItemId": 4766, # 珍珠
            "Number": 456,
        },
    ]

    mail_param = {
        "MessageId": 18,
        "EffectTime": 1598341000, #2020-08-25 15:36:40
        "PlayerExpireTime": 1754150400, #2025-08-03 00:00:00
        "MultiLang": [],
        # "FilterPlayerIds": filterPids,
        "GmSendId": 14,
        "Gifts":gifts,
        "Pid": 32769,
    }

    for langId in range(1,14):
        mail_param["MultiLang"].append({
            "language": langId,
            "title": "",
            "content": "这是测试屏蔽玩家邮件2222222222",
        })

    httpAddr = [
        "http://10.30.40.66:50419",
        # "http://172.16.22.111:43627",
        # "http://172.16.22.111:34774",
        # "http://172.16.22.111:46065",
        # "http://172.16.22.111:44248",
    ]

    for addr in httpAddr:
        url = '{}/1.0/player/server_send_mail?{}'.format(addr,json.dumps(mail_param))
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("erro!!!!")

# optMailFilter2()

# Table  string      `json:"table"`   // 需要更改的表名称
# OpType string      `json:"op_type"` // 操作类型 update delete insert
# IDList []ModifyIds `json:"ids"`     // 表主键 Id/Pid
# Data   string      `json:"data"`    // 表数据的 JSON 序列化需填充全部数据

# def modifyMemory():
#     modify_info = []
#     modify_info.append({
#         "op_type": "delete",
#         "data": "",
#         "table": "player_mail",
#         "ids":[{"id": 350930178,},], # id 或者 pid 必须存在库里面
#     })
#     data = json.dumps({
#             "data": json.dumps(modify_info)
#         })
#     url = "{}/1.0/memory/modify?{}".format("http://wll-cn-prod-game004:42851", data)
#     response = requests.get(url, timeout=10)
#     if response.status_code != 200:
#         print("erro!!!!",response)

# modifyMemory()
def modifyMemory():
    modify_info = []
    modify_info.append({
        "op_type": "delete",
        "data": "",
        "table": "player_mail",
        "ids":[{"id": 81921,"pid":24577},], # id 或者 pid 必须存在库里面
    })
    data = json.dumps({
            "data": json.dumps(modify_info)
        })
    url = "{}/1.0/memory/modify?{}".format("http://10.30.40.66:61101", data)
    response = requests.get(url, timeout=10)
    print(url)
    if response.status_code != 200:
        print("erro!!!!",response)

# modifyMemory()



def roguelikeEnd():
    filterPids = [16385]
    data = {
        "PlayerIds": filterPids,
    }
    url = '{}/1.0/roguelike/end_with_receive_award?{}'.format("http://10.30.40.197:50827",json.dumps(data))
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# roguelikeEnd()

def roguelikeSetId():
    data = {
        "roguelike_id": 0,
    }
    url = '{}/1.0/roguelike/set_roguelike_id?{}'.format("http://10.30.40.197:50827",json.dumps(data))
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# roguelikeSetId()


# canawardPids = {}
# def getData(file):
#     with open(file,'r') as f:
#         reader = csv.reader(f)
#         for row in reader:
#             pid = row[0]
#             if pid.isdigit():
#                 pid = int(pid)
#                 if pid not in canawardPids:
#                     canawardPids[pid] = pid

# canfile = "/Users/smakry/test/tribe_cn/部落战助威_珍珠.csv"
# getData(canfile)


# with open("部落战助威_珍珠.txt", 'a+') as f:
#     for pid in canawardPids:
#         f.write('%s \n' % (pid))




def compress_attaches(files, out_name):
    f = zipfile.ZipFile(out_name, 'w', zipfile.ZIP_DEFLATED)
    for file in files:
        f.write(file)
    f.close()

def copyTeamDatas():
    tmpDadta = [147457,155649,163841,172033,180225,188417,196609,204801,212993,221185,229377,237569,245761,253953,262145,270337]
    files = []
    for pid in tmpDadta:
        data = {
            "pid": pid,
        }

        url = "{}/1.0/copy/copy_data?{}".format("http://10.30.40.97:59792" ,json.dumps(data))
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("erro!!!!:", response)
        else:
            with open("{}.txt".format(pid), "a+") as f:
                f.write(response.json()['data'] + "\n")
                files.append("{}.txt".format(pid))

    if len(files) > 0:
        compress_attaches(files, "copy_data_{}.zip".format(time.time()))

    for pid in tmpDadta:
        os.remove("{}.txt".format(pid))

# copyTeamDatas()

def mothcarTest():
    data = {
        "ProductId": "wula_pet_mcard",
        "Account": 1,
        "PlayerId": 8193,

    }
    url = '{}/1.0/order/recharge?{}'.format("http://10.30.40.197:59294",json.dumps(data))
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# mothcarTest()


def insertSeasonRankData():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=4)
    for i in range(1, 5):
        n = 8192+20000
        n = n + i
        role = 18
        key = '{\"Pid\":'+ str(n) +',\"RoleId\":23,\"PrepRoleId\":23,\"Nick\":\"robot14\",\"Level\":80,\"Time\":1602412723,\"MissionId\":7}'
        r.zadd('wulala:elite_global:195',{
            key : 32757325644
            })

# insertSeasonRankData()


def modifyMemory2():
    modify_info = []
    modify_info.append({
        "op_type": "update",
        "data": json.dumps({"pid":1040385,"total":100,"num":89,"value":3}),
        "table": "player_hero_talent_state",
        "ids":[{"pid": 1040385},], # id 或者 pid 必须存在库里面
    })
    data = json.dumps({
            "data": json.dumps(modify_info)
        })

    url = "{}/1.0/memory/modify?{}".format("http://172.16.22.24:36395", data)
    response = requests.get(url, timeout=10)
    print(url)
    print(response)
    if response.status_code != 200:
        print("erro!!!!",response)

# modifyMemory2()

def team_leave():
    data = {
        "pid": 229380,
    }
    url = '{}/1.0/team/team_leave_http?{}'.format("http://10.30.40.197:64709",json.dumps(data))
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
# team_leave()

def get_rank_chan_length():
    url = '{}/1.0/season/get_season_rank_chan_length'.format("http://10.30.40.197:64338")
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())
# get_rank_chan_length()

def test_do_mission_battle_result():
    cursors = sql_connect()
    team_id_now = 0
    team_data = []
    pids = []
    finished_target_pids = []
    mission_id = 799

    index = 0
    for row in cursors:
        if int(row[1]) < 162996228:
            continue

        data = {
            "mission_id": mission_id,
            "sponsor_pid": 0,
        }
        if int(row[1]) != team_id_now:
            data["team_id"] = team_id_now
            data["pids"] = pids
            data["finished_target_pids"] = finished_target_pids
            if team_id_now <= 0:
                team_id_now = int(row[1])
                continue
            team_id_now = int(row[1])

            team_data.append(data)

            index += 1
            if index > 500:
                index = 0
                url = '{}/1.0/season/test_do_mission_battle_result?{}'.format("http://10.30.40.197:64425",json.dumps({"team_data": team_data}))
                print(url)
                response = requests.get(url, timeout=10)
                if response.status_code != 200:
                    print("erro!!!!",response)
                get_rank_chan_length()
                time.sleep(5)
                team_data = []

            pids = []
            finished_target_pids = []

        pids.append(row[2])
        if row[11] > 100:
            finished_target_pids.append(row[2])

# test_do_mission_battle_result()


def get_day_rank_award():
    url = '{}/1.0/season/send_season_day_five_award_by_snap'.format("http://10.30.40.197:58825")
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# get_day_rank_award()

def optPraciceRank():
    data = {
        "practice_type":1,
    }
    url = '{}/1.0/practice/push_practice_rank_to_redis?{}'.format("http://10.30.40.66:59054",json.dumps(data))
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!")

# optPraciceRank()



def optMailFilter3():
    gifts = [
        {
            "ItemId": 4766, # 珍珠
            "Number": 456,
        },
    ]

    mail_param = {
        "MessageId": 141,
        "EffectTime": 1598341000, #2020-08-25 15:36:40
        "PlayerExpireTime": 1754150400, #2025-08-03 00:00:00
        # "MultiLang": [],
        # "FilterPlayerIds": filterPids,
        # "GmSendId": 14,
        # "Gifts":gifts,
    }

    # for langId in range(1,14):
        # mail_param["MultiLang"].append({
        #     "language": langId,
        #     "title": "",
        #     "content": "这是测试屏蔽玩家邮件2222222222",
        # })

    httpAddr = [
        "http://10.30.40.66:59294"
    ]

    for addr in httpAddr:
        url = '{}/1.0/player/server_send_mail?{}'.format("http://10.30.40.66:59294",json.dumps(mail_param))
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("erro!!!!")

# optMailFilter3()


def quitMonopoly():
    data = {
        "pid": 65537,
        "mode": 1,
    }
    url = '{}/1.0/monopoly/quit_monopoly_game?{}'.format("http://10.30.40.66:50868",json.dumps(data))
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# quitMonopoly()

def clearMonopoly():
    data = {
    }
    url = '{}/1.0/monopoly/fix_monopoly_team_delete?{}'.format("http://10.30.40.66:59025",json.dumps(data))
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)


def afterMonopoly():
    data = {
        "monopoly_id": 1,
        "place_count_time": 1628438399,
    }
    url = '{}/1.0/monopoly/after_monopoly_award_send?{}'.format("http://wll-cn-prod-game047:39019",json.dumps(data))
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# afterMonopoly()

# clearMonopoly()

	# var req struct {
	# 	Content         string         `json:"Content"`
	# 	ServerId        uint8          `json:"ServerId"`
	# 	AllServer       int8           `json:"AllServer"`
	# 	PlayerIds       []int64        `json:"PlayerIds"`
	# 	Type            int8           `json:"Type"`
	# 	Items           string         `json:"Items"`
	# 	EffectTime      int64          `json:"EffectTime"`
	# 	ExpireTime      int64          `json:"ExpireTime"`
	# 	MultiLang       []multiLangReq `json:"MultiLang"`
	# 	GmSendId        int64          `json:"GmSendId"`
	# 	FilterPlayerIds []int64        `json:"FilterPlayerIds"`
	# }

def sendServerMailT():
    gifts = [
        {
            "id": 4766, # 珍珠
            "num": 456,
        },
        {
            "id": 53113, # 月卡
            "num": 1,
        },
    ]

    mail_param = {
        "EffectTime": 1598341000, #2020-08-25 15:36:40
        "ExpireTime": 1754150400, #2025-08-03 00:00:00
        "MultiLang": [],
        # "FilterPlayerIds": filterPids,
        # "GmSendId": 14,
        "ServerId": 1,
        "Items":json.dumps(gifts),
        "AllServer": 1,
        "Content": "这是测试福利邮件",
    }

    for langId in range(5,7):
        mail_param["MultiLang"].append({
            "language": langId,
            "title": "",
            "content": "这是测试屏蔽玩家邮件2222222222",
        })

    httpAddr = [
        "http://10.30.40.66:53411"
    ]

    for addr in httpAddr:
        url = '{}/1.0/item/change?{}'.format(addr, json.dumps(mail_param))
        print(url)
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("erro!!!!:",response.status_code)

# sendServerMailT()



def modifyServerMailMemory():
    modify_info = []
    modify_info.append({
        "op_type": "update",
        "data": "",
        "table": "global_mission_team_player",
        "ids":[{"id": 24577}], # id 或者 pid 必须存在库里面
    })
    data = json.dumps({
            "data": json.dumps(modify_info)
        })
    # url = "{}/1.0/memory/modify?{}".format("http://10.30.40.66:61101", data)

    url = "{}/1.0/memory/modify?{}".format("http://172.16.22.64:38605", data)
    print(url)
    response = requests.get(url, timeout=10)
    print(url)
    if response.status_code != 200:
        print("erro!!!!",response)

# modifyServerMailMemory()


def fix_hero_zone():
    # 45542 42579 43277 38870 42273
    url = '{}/1.0/hero_zone/fix_hero_zone_max_mission'.format("http://172.16.22.64:40907")
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# fix_hero_zone()


def fix_budo_will_award():
    award = [
        {"Id": 1, "WarZoneId": 1, "Round": 32, "AwardBoxId": 647},
        {"Id": 2, "WarZoneId": 1, "Round": 16, "AwardBoxId": 648},
        {"Id": 3, "WarZoneId": 1, "Round": 8, "AwardBoxId": 649},
        {"Id": 4, "WarZoneId": 1, "Round": 4, "AwardBoxId": 650},
        {"Id": 5, "WarZoneId": 1, "Round": 2, "AwardBoxId": 651},
        {"Id": 6, "WarZoneId": 1, "Round": 1, "AwardBoxId": 652},
        {"Id": 7, "WarZoneId": 0, "Round": 32, "AwardBoxId": 641},
        {"Id": 8, "WarZoneId": 0, "Round": 16, "AwardBoxId": 642},
        {"Id": 9, "WarZoneId": 0, "Round": 8, "AwardBoxId": 643},
        {"Id": 10, "WarZoneId": 0, "Round": 4, "AwardBoxId": 644},
        {"Id": 11, "WarZoneId": 0, "Round": 2, "AwardBoxId": 645},
        {"Id": 12, "WarZoneId": 0, "Round": 1, "AwardBoxId": 646},
        ]
    data = {
        "budo_round_award": award,
    }

    https = {
        "http://172.16.22.64:36504",
        # "http://172.16.22.64:39905",
        # "http://172.16.22.64:38804",
        # "http://172.16.22.64:41208",
        # "http://172.16.22.64:38206",
        # "http://10.30.40.66:60996",
    }
    for http in https:
        url = '{}/1.0/budo_will/fix_award_old_box?{}'.format(http,json.dumps(data))
        print(http)
        response = requests.get(url, timeout=10)
        if response.status_code != 200:
            print("erro!!!!",response)

# fix_budo_will_award()

def create_token():
    data = {
        "now": 1628227941,
        "valid": 36000,
        "name": "linxiaodong",
    }

    url = '{}/1.0/copy/gen_copy_authority_token?{}'.format("http://10.30.40.66:51298",json.dumps(data))
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# create_token()


def set_token_key():
    r = redis.StrictRedis(host='127.0.0.1', port=6379, db=9)
    data = {
        "now": 1628227941,
        "valid": 36000,
        "name": "linxiaodong",
        "token": "jJo0lVxzjhpJUT7l5tuDkl9ZBQrZtl22aERX-VYSYQk=",
    }
    r.setnx('wulala:copy_authority_token:{}'.format(data["token"]), json.dumps(data))

# set_token_key()


def test_token_key():
    data = {
        "access_token": {
            "now": 1628227941,
            "valid": 36000,
            "name": "linxiaodong",
            "token": "jJo0lVxzjhpJUT7l5tuDkl9ZBQrZtl22aERX-VYSYQk=",
        },
    }

    url = "{}/1.0/copy/insert_datas".format("http://10.30.40.66:51996")
    response = requests.post(url=url,json=data)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# test_token_key()



def test_fix_foredawn():
    url = '{}/1.0/foredawn_battle/clear_player_config'.format("http://10.30.40.66:61456")
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# test_fix_foredawn()

# print(json.dumps({"now": "✪圣域✪"}))


def fix_budo_will_award():
    data = {
        "stage": 3,
    }

    https = {
        "http://172.16.22.67:41211",
        "http://172.16.22.67:42436",
        "http://172.16.22.67:43980",
        "http://172.16.22.67:42536",
        "http://172.16.22.67:44799",
    }
    for http in https:
        url = '{}/1.0/hero_zone/set_hero_zone_stage?{}'.format(http, json.dumps(data))
        print(url)
        # response = requests.get(url, timeout=10)
        # if response.status_code != 200:
        #     print("erro!!!!",response)



def insertRoguelikeRankData():
    r = redis.StrictRedis(host='172.16.22.113', port=15424, db=0)
    for i in range(1, 94):
        n = 8192
        n = n + i
        role = 18
        key = '{\"Pid\":'+ str(n) +',\"RoleId\":73,\"PrepRoleId\":73,\"Nick\":\"8193\",\"Level\":251,\"RelevelTimes\":1,\"Time\":1637491706,\"MaxFloorId\":105,\"ActionItemId\":63873,\"Head\":64288,\"HeadSculpture\":63945,\"ChatBubble\":63944,\"Title\":64349}'
        r.zadd('wulala:roguelike_global:12:542',{
            key : 453629041669
            })

# insertRoguelikeRankData()


def testFUnc():
    data = {"num": 5200, "num2": 1500, "list": [1819977, 15025481, 7726409, 10560841, 2147657, 214345, 6694217, 1762633, 4269385, 599369, 4343113, 8496457, 2155849, 13780298, 2819402, 877898, 1164618, 2057546, 1369418, 5637450, 4146506, 2696522, 1156426, 13796682, 6538570, 11461963, 6653259, 1090891, 2925899, 1819979, 10691915, 5743947, 4187467, 9528651, 6784331, 468299, 3376459, 13657419, 1992011, 664912, 18834768, 132432, 1279312, 2393424, 16016720, 18507090, 992594, 509266, 648530, 6743378, 2762066, 14820690, 787794, 107858, 3310930, 20391250, 124244, 7873876, 10560852, 10528084, 15238484, 8045908, 7251284, 2155860, 17007956, 12043605, 13632853, 329045, 3065173, 5924182, 1869142, 6407510, 8316246, 16827734, 9299286, 34136, 3753304, 3269976, 3294552, 3081560, 6579545, 4875609, 14165337, 10528089, 2082140, 2000220, 10716508, 5023070, 3343710, 1516894, 11404638, 4646239, 12027232, 124258, 5875042, 3908962, 2319715, 42339, 8004963, 7824739, 1328484, 9626980, 869732, 2065764, 14337380, 2753899, 9405803, 4400491, 11511147, 11003243, 11167085, 10454382, 476526, 11650414, 3827055, 525679, 3302767, 2106735, 7791983, 8947055, 11175279, 13501807, 9667953, 12125553, 13665649, 14443889, 427378, 3212658, 2852211, 13657459, 501107, 5973363, 5154163, 13952371, 5203315, 4728179, 214389, 11732341, 8717685, 1729909, 542069, 10724725, 14189943, 869751, 746871, 845175, 8119671, 4261240, 9225592, 16483704, 7775608, 10855800, 2794872, 1828216, 13206904, 17900920, 3335544, 83321, 370041, 17933689, 468345, 8750457, 8398201, 7931257, 3843449, 10700153, 796025, 9643387, 1172859, 6915451, 10216827, 4105595, 10683771, 10765691, 9889147, 11625852, 11830652, 13362556, 5727612, 8701308, 7234940, 2303356, 11445628, 4662653, 13116797, 746877, 1410429, 2311551, 12141951, 2647423, 5563775, 2139519, 8381823, 4138367, 1566081, 157058, 320898, 4253058, 13370754, 8119682, 10356098, 14427522, 1156482, 13067650, 3990914, 3450242, 12805506, 6325634, 8316291, 8193411, 12912003, 10528131, 3212675, 15476099, 12027267, 10585475, 16663939, 10896771, 2958723, 1934725, 1058181, 12387717, 345477, 320901, 16246149, 2606469, 7062917, 12436869, 132485, 2942341, 16860549, 8480133, 5989766, 66950, 14689670, 15164806, 13903238, 5670278, 3179910, 7914886, 7751046, 11961734, 12699014, 9684358, 4818311, 3646855, 15730055, 198023, 13788551, 15320455, 8430983, 12969351, 4662663, 12420487, 3810695, 9430407, 8816007, 2246023, 6088071, 4195721, 9454985, 12756361, 12682633, 8398217, 5531017, 16352649, 14247305, 9414025, 4171145, 12821897, 697737, 755081, 17311115, 3990923, 75147, 15680907, 12281227, 13010315, 4351371, 21349771, 18007435, 22332811, 23094667, 19514763, 23143819, 13002123, 19080587, 5440907, 5973387, 6915468, 222604, 5481868, 8578444, 11281804, 17687948, 8938892, 3204492, 7693708, 17704332, 19096972, 17556876, 4933004, 9790860, 7406988, 20882828, 17966476, 2336140, 15230348, 5449101, 25240973, 27207053, 689549, 28878221, 4924813, 19334541, 4801933, 542094, 5334414, 279950, 10667406, 206222, 5449102, 11625870, 3368334, 9160078, 8119695, 1181071, 6464911, 6579599, 3630479, 13854095, 8488335, 6514063, 11855248, 10167696, 10208656, 10175888, 8955280, 13256080, 8439184, 26001, 116113, 14960017, 148881, 402833, 2286993, 4400529, 3401105, 10233233, 10773905, 13968785, 2958737, 10839441, 8848786, 6104466, 17851794, 8717714, 17876370, 11838866, 1000850, 17597842, 9962898, 14673298, 1361298, 10651026, 15951250, 13739411, 13321619, 5473683, 16655763, 5563795, 574867, 9667987, 10495379, 14370195, 1672595, 1549715, 4253075, 10478995, 14796179, 13821331, 10266003, 1115539, 13624723, 8119699, 15959446, 7079318, 435606, 11625878, 13272470, 5866902, 9643414, 15918486, 12125590, 5268886, 18122135, 11953559, 11650455, 15279511, 5244311, 1598871, 15443351, 7595415, 5399960, 4588952, 5989784, 13763992, 9749912, 11339160, 320920, 7349656, 5866904, 10143128, 1099160, 3253656, 542104, 10495384, 10618264, 1213848, 2074009, 8447385, 5023129, 1123737, 5694873, 4769177, 3859865, 2557337, 3720601, 7718297, 3057049, 11126169, 148890, 7570842, 722330, 26010, 9553306, 6931866, 1435034, 9209242, 6563226, 10274202, 12993946, 2811290, 6112666, 13387162, 10896794, 3007898, 6129050, 861594, 13452698, 3204506, 11724186, 12420506, 12928412, 6669724, 5678492, 13231516, 3892636, 7628188, 12461468, 12871068, 8570268, 607644, 7636380, 15156636, 15164828, 7284124, 10134940, 6776220, 3368348, 6374812, 9667996, 10036636, 2434460, 9913758, 11019678, 10978718, 10986910, 10995102, 2287006, 5891486, 7521695, 4310431, 722335, 5055903, 4449695, 8095135, 6440351, 2385311, 4965791, 7546271, 7087526, 7071142, 7153062, 1254822, 533926, 746918, 640422, 2114982, 1050022, 1041830, 5801382, 460198, 2860454, 198054, 3696038, 4384166, 3466662, 3171750, 6186407, 5776807, 968103, 1926567, 591271, 2287015, 533927, 3941799, 5449127, 263591, 5727655, 2139559, 6907303, 4851111, 402856, 6882728, 6825384, 542120, 6858152, 6833576, 189864, 6374824, 4564392, 5424552, 6366632, 4531624, 6383016, 6325672, 6186408, 1779112, 1754536, 1795496, 1762728, 8734120, 8725928, 6776232, 2033064, 2057640, 1410472, 4998569, 116137, 132521, 3286441, 3343785, 3311017, 3753385, 984489, 1303977, 1369513, 1320361, 5342635, 107947, 1238443, 271787, 7071147, 820651, 5916075, 5932459, 3384747, 6612395, 5285291, 181675, 3712427, 3777963, 3966379, 3851691, 2753963, 599469, 1762733, 517549, 4924845, 7275949, 34221, 7325101, 7873965, 206253, 5227949, 3622317, 566701, 4654509, 1164717, 2033069, 5997997, 1148333, 2327981, 4965805, 1721774, 2573742, 2753966, 1549742, 1074606, 1525166, 6210990, 4908462, 6497710, 3548590, 12576056, 7243064, 730425, 648505, 12477753, 615737, 435513, 15525177, 14959929, 19514686, 20923712, 11969856, 165185, 14255425, 7701825, 5129537, 8594753, 7677249, 7652673, 959810, 2835780, 10315084, 11650380, 16991564, 8455500, 8201549, 12920141, 5260621, 1549645, 853345, 812396, 894340, 4326794, 370069, 533917, 1959325, 1098888, 844936, 263304, 4211848, 631944, 2196616, 13878408, 353417, 312460, 1311884, 1213580, 3400845, 1705102, 1705103, 4015247, 418959, 1434767, 8602763, 17794197, 6349977, 4424857, 14107801, 2794651, 10708123, 13272221, 16729256, 17327274, 11740333, 3810478, 99502, 320688, 2475190, 2581686, 14050486, 20849850, 91324, 18351292, 7955646, 345278, 1066174, 38388930, 39060674, 12379330, 12420290, 12371138, 37807298, 1017028, 3753158, 12862662, 500936, 54658248, 17610, 53798090, 22979788, 58172626, 51315922, 50193618, 46900434, 12993748, 361684, 37930196, 30565590, 12813528, 24503514, 1762524, 53200092, 255196, 206044, 287964, 1500382, 2491616, 10110176, 12829920, 41821410, 10347748, 31712486, 28050664, 36971752, 14779624, 2000106, 1639660, 247020, 8758512, 558322, 18171122, 25842, 17650, 9127156, 13722868, 14165236, 18015476, 3089654, 9464, 13903096, 19719418, 10552570, 8176890, 15738108, 2876670, 21267710, 19834112, 419072, 12592384, 12870916, 26576132, 58180870, 38413574, 35480838, 27903240, 27084040, 16409864, 7750922, 13174026, 11109642, 2082058, 6636810, 30876940, 60212492, 17073424, 66832, 8922384, 30262544, 4646160, 21357840, 6178066, 14853394, 48375060, 15566100, 52413716, 1025302, 43033880, 1787160, 7578906, 2811162, 15107354, 62833946, 15893786, 6915354, 18892060, 34170140, 12240156, 9500, 3147036, 26592540, 148766, 15820062, 255262, 16942368, 2450724, 10233124, 2868516, 20423972, 8463655, 8258856, 206124, 9495853, 9545007, 5367088, 820529, 705841, 31417652, 9700662, 13018422, 11928886]}
    print(json.dumps(data))

# testFUnc()



def fix_memory_table():
    data = {
        "names": ["activity_center"],
    }
    url = '{}/1.0/common/reload_table?{}'.format(http_addr,json.dumps(data))
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# fix_memory_table()


def fix_memory_dat_table():
    url = '{}/1.0/common/dat_reload'.format(http_addr)
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# fix_memory_dat_table()

def fix_memory_manual_gc():
    url = '{}/1.0/common/manual_gc'.format("http://10.30.40.66:64888")
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# fix_memory_manual_gc()


def fix_memory_activity_table():
    data = {
        "activity_center_id": 12345,
        "is_open": True,
        "start_time": 2222233,
        "end_time":23434,
    }
    url = '{}/1.0/activity_center/add_activity?{}'.format("http://10.30.40.66:61246", json.dumps(data))
    print(url)
    # response = requests.get(url, timeout=10)
    # if response.status_code != 200:
    #     print("erro!!!!",response)

# fix_memory_activity_table()


def test_xd_cn_order():
    data = {
        "module": "GameAnalysis",
        "ip": "218.107.213.115",
        "name": "charge",
        "index": "b38j1gchf0872h7p",
        "identify": "test-20211123",
        "properties": {
            "order_id": "test20211123",
            "amount": 100,
            "virtual_currency_amount": 100,
            "currency_type": "CNY",
            "product": "wula33",
            "payment": "googleplay"
        }
    }
    url = '{}?{}'.format("https://e.tapdb.net/event", json.dumps(data))
    print(url)
    response = requests.post(url=url,json=data)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())
# test_xd_cn_order()

def test_xd_cn_order():
    data = {
        "module": "GameAnalysis",
        "ip": "218.107.213.115",
        "name": "charge",
        "index": "b38j1gchf0872h7p",
        "identify": "test-20211123",
        # "identify": "63178206",
        "properties": {
            "order_id": "2323332322",
            "amount": 10000,
            "virtual_currency_amount": 10000,
            "currency_type": "CNY",
            "product": "wula6",
            "payment": "alipay"
        }
    }
    response = requests.post(url="https://e.tapdb.net/event",data=urllib.parse.quote(json.dumps(data)))
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# test_xd_cn_order()
# curl -X POST --data-urlencode '{"module":"GameAnalysis","name":"charge","index":"b38j1gchf0872h7p","identify":"test-20211123","properties":{"order_id":"NEX0052137964","amount":3000,"virtual_currency_amount":3000,"currency_type":"CNY","product":"wula33","payment":"googleplay"}}' "https://e.tapdb.net/event"


		# ActivityIds       []int32 `json:"activity_center_ids"` // 活动中心id组
		# IsOpen            bool    `json:"is_open"`             // 是否开放
		# StartTime         int64   `json:"start_time"`          // 开始时间
		# EndTime           int64   `json:"end_time"`            // 结束时间
		# OpenTimeType      int16   `json:"open_time_type"`      // 开放时间类型（开放时间类型:0—常规时间、1—开服时间）
		# OpenAfterTime     int64   `json:"open_after_time"`     // 开服相对开放时间
		# OpenContinuedTime int64   `json:"open_continued_time"` // 开放持续时间
def fix_memory_activity_table2():
    activity_ids = [4039, 6017, 8111, 8119, 8123, 8131, 8139, 8143, 8147, 8155, 10886, 10890, 10894, 10897, 10900, 10904, 10908, 10911, 10914, 10917, 10921, 10925, 10929, 10933, 10937, 10940, 10948, 10952, 10955, 10963, 10967, 10971, 10974, 20017, 21031, 21039, 21043, 26027, 27011, 32007, 35022, 35026]
    data = {
        "activity_center_ids": activity_ids,
        "is_open": True,
        "start_time": 1639302460,
        "end_time":1639993660,
    }
    url = '{}/1.0/activity_center/multi_add_activity?{}'.format("http://10.30.40.66:61379", json.dumps(data))
    print(url)
    # response = requests.get(url, timeout=10)
    # if response.status_code != 200:
    #     print("erro!!!!",response)

# fix_memory_activity_table2()

def testtime():
        day = time.strftime('%Y-%m-%d', time.localtime(time.time()))
        time_array = time.strptime(f"{day} 05:00:00", "%Y-%m-%d %H:%M:%S")
        mytime = time.mktime(time_array)
        print(mytime)

def test_task_system():
    data = {
    }
    url = '{}/1.0/task_system/fix_1_8_0?{}'.format(http_addr, json.dumps(data))
    print(url)
    response = requests.post(url=url,json=data)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# test_task_system()


def clear_player_config():
    data = {
        "glove_config_kind": [9, 21],
        "pet_config_kind": [6, 18],
        "skill_config_kind": [9, 21],
    }

    url = "{}/1.0/team/clear_player_config?{}".format(http_addr, json.dumps(data))
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)

# clear_player_config()

def check_nodes():
    data = {
        "Ids": [1, 21],
    }

    url = "{}/1.0/common/check_nodes?{}".format(http_addr, json.dumps(data))
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# check_nodes()

def check_bulletin():
    data = {
        "Id": 150007,
        "OpType": 3,
    }

    url = "{}/1.0/player/post_bulletin?{}".format(http_addr, json.dumps(data))
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# check_bulletin()

def insert_mountain():
    url = "{}/1.0/mountain/insert_battle".format(http_addr)
    # print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())

# for i in range(1, 10000):
#     insert_mountain()

def delete_mountain():
    url = "{}/1.0/mountain/delete_battle".format(http_addr)
    print(url)
    response = requests.get(url, timeout=10)
    if response.status_code != 200:
        print("erro!!!!",response)
    else:
        print(response.json())
# delete_mountain()

import hashlib

import requests
import re
import xml.etree.ElementTree as ET
import time
import random
from time import sleep

# 对应Java中的常量定义
COLOR = "0xA0A0A00xFF00000x00FF00"
FISH_URL = "http://coml.manorage.com/manorage/FishingAction!PlayerGetFish.comapp"
HUNT_URL = "http://coml.manorage.com/manorage/hunt_xbc!newSubmitHunt.comapp"
COLLECT_URL = "http://coml.manorage.com/manorage/collection!getPrize.comapp"
LOGIN_URL = "http://coml.manorage.com/manorage/init!userLogin.comapp"
QUERY_FISH = "http://coml.manorage.com/manorage/FishingAction!PlayerFishingInit.comapp"
OPEN_PACKAGE = "http://coml.manorage.com/manorage/init!openPackage.comapp"
STORE_ITEM = "http://coml.manorage.com/manorage/commercerActionXmx!storeItem.comapp"
USER_DEPOT = "http://coml.manorage.com/manorage/init!initUserDepot.comapp"
QUERY_CREATE_ITEM = "http://coml.manorage.com/manorage/create!getCreateItemInfo.comapp"
FETCH_CREATE_ITEM = "http://coml.manorage.com/manorage/create!fetchCreateItem.comapp"
CREATE_ITEM = "http://coml.manorage.com/manorage/create!createItem.comapp"
ENTER_PLANT = "http://coml.manorage.com/manorage/plant!enterPlant.comapp"
GET_ALL_FRUIT = "http://coml.manorage.com/manorage/plant_xmx!getAllFruit.comapp"
ZOON_INIT = "http://coml.manorage.com/manorage/water!zoonInit.comapp"
HARVEST_ALL = "http://coml.manorage.com/manorage/water!harvestAll.comapp"
PLAYER_EXCHANGED_INIT = "http://coml.manorage.com/manorage/FishingAction!PlayerExchangeInit.comapp"
PLAYER_EXCHANGED_FISHING_ITEM = "http://coml.manorage.com/manorage/FishingAction!PlayerExchangeFishingItem.comapp"
DELETE_ALL_DEAD_PLANT = "http://coml.manorage.com/manorage/plant!delAllDeadPlant.comapp"
BUY_ITEM = "http://coml.manorage.com/manorage/consignment_xmx!storeBuy.comapp"
ADD_PLANT = "http://coml.manorage.com/manorage/plant!addPlant.comapp"
DELETE_ALL_ANIMAL ="http://coml.manorage.com/manorage/water!deleteAllAnimal.comapp"
ADD_ANIMAL =  "http://coml.manorage.com/manorage/water!addAnimal.comapp"
SUBMIT_PLANT = "http://coml.manorage.com/manorage/task_xbc!submitTask.comapp"
INIT_USER_TASK = "http://coml.manorage.com/manorage/task_xbc!initUserTask.comapp"
OPEN_RARITY_CHESTS = "http://coml.manorage.com/manorage/chests!openRarityChests.comapp"

ITEM_QUALITY_MAP = {'100228': '0', '100225': '0', '10006801': 'no', '10008001': 'no', '100081': '0', '10009001': 'no', '10009201': 'no', '10009401': 'no', '10009801': 'no', '10009802': 'no', '10010001': 'no', '100101': '0', '10010201': 'no', '10010401': 'no', '10010801': 'no', '100124': '0', '100126': '0', '100127': '0', '100141': '0', '100142': '0', '100144': '0', '100145': '0', '100164': '0', '100165': '0', '100166': '0', '100168': '0', '100169': '0', '100172': '0', '100181': '0', '100183': '0', '100184': '0', '100201': '0', '100202': '0', '100203': '0', '100204': '0', '100206': '0', '100207': '0', '100208': '0', '100223': '0', '100224': '0', '100227': '0', '100229': '0', '100230': '0', '100231': '0', '100235': '0', '100236': '0', '100237': '0', '100239': '0', '100240': '0', '100263': '0', '100281': '0', '100301': '0', '100361': '0', '100390': '0', '100391': '0', '100392': '0', '100393': '0', '100394': '0', '100395': '0', '100397': '0', '100403': '0', '100406': '0', '100409': '0', '100410': '0', '100412': '0', '100413': '0', '100414': '0', '100415': '0', '100418': '0', '100419': '0', '100420': '0', '100542': '0', '100543': '0', '100544': '0', '100545': '0', '100546': '0', '100547': '0', '100595': 'no', '100597': 'no', '100700': 'no', '100701': 'no', '100702': 'no', '100703': 'no', '100746': 'no', '100748': 'no', '1009': 'no', '1010': 'no', '1011': 'no', '1012': 'no', '1028': 'no', '1029': 'no', '1030': 'no', '10305601': 'no', '10307001': 'no', '10307501': 'no', '10308001': 'no', '10308501': 'no', '10309001': 'no', '10309301': 'no', '10309601': 'no', '10309701': 'no', '10310001': 'no', '10310101': 'no', '10310401': 'no', '10310501': 'no', '10310502': 'no', '1035': 'no', '1036': 'no', '1089': 'no', '11100154': 'no', '11100503': 'no', '11100704': 'no', '11100714': 'no', '11100715': 'no', '11100716': 'no', '11100809': 'no', '11101207': 'no', '11101218': 'no', '11101219': 'no', '11101222': 'no', '11101223': 'no', '11101770': 'no', '11101887': 'no', '11101892': 'no', '11101894': 'no', '11200209': '0', '11200301': '0', '12400401': 'no', '12500001': 'no', '1473': 'no', '1475': 'no', '1483': 'no', '1514': 'no', '1592': 'no', '1598': 'no', '1605': 'no', '1606': 'no', '1607': 'no', '1608': 'no', '1731': 'no', '1752': 'no', '1754': 'no', '1756': 'no', '1770': 'no', '1830': 'no', '1890': 'no', '200012': 'no', '200051': 'no', '450': 'no', '554': 'no', '557': 'no', '560': 'no', '562': 'no', '563': 'no', '564': 'no', '566': 'no', '568': 'no', '569': 'no', '571': 'no', '576': 'no', '578': 'no', '580': 'no', '582': 'no', '584': 'no', '585': 'no', '589': 'no', '590': 'no', '592': 'no', '606': 'no', '608': 'no', '610': 'no', '612': 'no', '614': 'no', '630': 'no', '632': 'no', '634': 'no', '636': 'no', '637': 'no', '639': 'no', '642': 'no', '644': 'no', '651': 'no', '652': 'no', '668': 'no', '672': 'no', '676': 'no', '678': 'no', '680': 'no', '682': 'no', '684': 'no', '686': 'no', '689': 'no', '691': 'no', '693': 'no', '695': 'no', '700': 'no', '716': 'no', '720': 'no', '721': 'no', '723': 'no', '724': 'no', '725': 'no', '726': 'no', '731': 'no', '810': 'no', '814': 'no', '816': 'no', '820': 'no', '825': 'no', '828': 'no', '830': 'no', '837': 'no', '839': 'no', '842': 'no', '843': 'no', '846': 'no', '848': 'no', '850': 'no', '852': 'no', '855': 'no', '857': 'no', '859': 'no', '861': 'no', '864': 'no', '866': 'no', '870': 'no', '873': 'no', '877': 'no', '879': 'no', '881': 'no', '888': 'no', '890': 'no', '908': 'no', '948': 'no', '950': 'no', '100596': '0', '100598': '0', '100747': '0', '100749': '0', '11101204': '0', '11101509': '0', '11300007': '0', '11306801': '0', '11307301': '0', '11307801': '0', '11308001': '0', '11308301': '0', '11308801': '0', '11309001': '0', '11309401': '0', '11309801': '0', '11309802': '0', '11310001': '0', '11310201': '0', '11310401': '0', '11310801': '0', '11405601': '0', '11407001': '0', '11407501': '0', '11408001': '0', '11408501': '0', '11409001': '0', '11409301': '0', '11409601': '0', '11409701': '0', '11410001': '0', '11410101': '0', '11410401': '0', '11410501': '0', '11410502': '0', '1474': '0', '1476': '0', '1484': '0', '1509': '0', '1523': '0', '1524': '0', '1526': '0', '1527': '0', '1528': '0', '1529': '0', '1530': '0', '1531': '0', '1532': '0', '1642': '0', '1643': '0', '1732': '0', '1751': '0', '1753': '0', '1755': '0', '1757': '0', '1771': '0', '1831': '0', '1872': '0', '1873': '0', '200050': '0', '200052': '0', '558': '0', '561': '0', '565': '0', '567': '0', '570': '0', '572': '0', '574': '0', '577': '0', '581': '0', '583': '0', '586': '0', '588': '0', '591': '0', '593': '0', '607': '0', '609': '0', '611': '0', '613': '0', '615': '0', '629': '0', '631': '0', '633': '0', '635': '0', '638': '0', '641': '0', '671': '0', '673': '0', '677': '0', '679': '0', '681': '0', '683': '0', '685': '0', '687': '0', '690': '0', '692': '0', '694': '0', '696': '0', '699': '0', '701': '0', '709': '0', '727': '0', '728': '0', '729': '0', '730': '0', '809': '0', '811': '0', '815': '0', '817': '0', '821': '0', '826': '0', '829': '0', '831': '0', '833': '0', '835': '0', '838': '0', '840': '0', '844': '0', '845': '0', '847': '0', '849': '0', '851': '0', '853': '0', '856': '0', '858': '0', '860': '0', '862': '0', '865': '0', '867': '0', '869': '0', '871': '0', '874': '0', '878': '0', '880': '0', '882': '0', '889': '0', '891': '0', '909': '0', '931': '0', '932': '0', '933': '0', '949': '0', '951': '0', '100171': '0', '100182': '0', '1032': 'no', '11101824': 'no', '11101891': 'no', '834': 'no', '868': 'no', '11300010': '0', '1412': 'no', '573': 'no', '587': 'no', '640': 'no', '698': 'no', '832': 'no', '1750': 'no', '100398': '0', '100400': '0', '100401': '0', '808': 'no', '100241': '0', '11101888': 'no', '669': '0', '11300015': '0', '11101889': 'no', '628': 'no', '101007': 'no', '11101719': 'no', '101009': 'no'}

ITEM_ELEMENT_MAP = {'200051': '1523', '1514': '200050', '100281': '583', '100391': '100281,613', '100184': '726,100281', '100225': '726,100281', '100224': '561,724', '100142': '565,572', '100143': '613,687', '100172': '629,721', '100234': '607,586,100281', '100165': '611,629', '100101': '685,725', '100236': '694,724', '100204': '687,100281', '100394': '635,100281,862', '100392': '687,723,725,593,581', '100124': '629,721,728', '100123': '721,728', '100121': '586,687', '100182': '685,724', '100141': '561,685', '100201': '607,613,867', '100403': '572,100281,565,862', '100181': '635,100281', '100228': '687,726,100281', '100393': '100281,891,862', '100168': '450,586,567', '100144': '574,685,723', '100416': '701,720,724,949,570', '100240': '565,723', '100208': '577,685,687,720', '100145': '581,723', '100229': '687,694,889', '100390': '687,100281,880', '100361': '809,100172,731', '100175': '611,629,709', '100171': '629,631,633', '100169': '629,631,633', '100301': '629,631,633', '100127': '629,631,633', '100223': '574,690,720,723', '100237': '581,565,679', '100202': '581,565,723', '100081': '450,561', '100183': '607,635,638', '100232': '687,694,724,889', '100235': '565,574,833', '100398': '724,100281,615', '100161': '611,629,100165', '100239': '681,723,725', '100185': '577,723,833', '100420': '696,723,565,844,862', '100397': '1526,669,574,565,581', '100231': '687,100281,100225,100228', '100395': '1526,725,565,581,100165', '100405': '1531,699,949,570,100181', '100410': '696,724,100281,586,862', '100203': '720,725,821', '100222': '687,724,730,731,811', '100233': '694,724,889,891', '100414': '687,725,100281,586', '100418': '572,949,588,591,844', '100417': '567,581,847,851,878', '100400': '574,683,687,723,838', '100227': '867,100225,100229', '100241': '831,100165', '100407': '1531,811,723,725,100165', '100207': '558,570,574,690', '100170': '611,629,728,100169', '100166': '611,629,709,728', '100206': '725,731,840', '100238': '694,716,724,730', '100221': '586,724,833,100171', '100396': '1531,815,716,723,100171', '100542': '100281,1771', '100230': '687,100228,100229', '100419': '100392,577,683,687,844', '100125': '611,629,709,727,728', '100263': '716,862,878,932', '100415': '100414,572,692', '100413': '694,586,829,100203', '100409': '100301,581,862,865', '100399': '100397,591,570,581,100101', '100167': '611,629,728,100166', '100404': '100395,669,723,100165,731', '100406': '809,720,723,609,100169', '100126': '611,629,100125', '100545': '1530,724,588,1751', '100402': '100395,683,723,581,100171', '100412': '100393,724,100281,882,100184', '100164': '629,631,633,729', '100401': '1529,100400,817,851', '100408': '100395,100241,581,856,858', '100544': '1527,100392,1751,847', '100262': '720,723,933,581,100164', '100411': '100398,100410,100241', '100546': '1532,1757,889,882', '100543': '1529,100398,724,1732,100542', '100205': '565,586,100203,100204', '100547': '100395,725,581,1753', '11200201': '100598,588,856,100395,100127', '11200202': '874,844,909,100747,1528', '11200101': '882,100281,100175', '11200103': '100166,100170,11200101', '11200104': '574,951,11306801,1529', '11200203': '951,100598,100204,724,1526', '11200204': '874,11300007,100411,100747', '11200301': '100411,100228,100596,100390', '11200302': '1757,100227,1530,100172', '11100904': '11100903,100175', '11101701': '11101719', '11101702': '11101719', '11101703': '11101719', '11101704': '11101719', '11101705': '11101719', '11101706': '11101719', '11101707': '11101719', '11101708': '11101719', '11101709': '11101719', '11101710': '11101719', '11101717': '11101719', '11101718': '11101719', '11200105': '951,889,561,1531,1527', '11200106': '1528,11307301,951,1527', '11200107': '574,567,586,11307301,1526', '11200108': '100164,100281,11307801', '11200109': '100175,11308801,11307801,727', '11200110': '11308801,611,11307801,721,729', '11200111': '11200110,100184,1530,709', '11200112': '867,11200110,727', '11200113': '11308801,611,11307801,728', '11200114': '11307801,11308801,721,709,727', '11200303': '1757,11407501,724,100281,1531', '11200304': '11408501,100204,716,565,11200209', '11200305': '11308801,687,100126,11200209,100281', '11200306': '11310001,11309201,100204,687,1531', '11200307': '100227,11309201,11200111,11407501,100281', '11200308': '11309801,11308001,100281,1532,100301', '11200309': '11310001,100225,724,694', '11200310': '11308001,11309801,100241,724,1530', '11200311': '11307801,11308801,100166,889,100204', '11200205': '889,725,11200209,11307301,723', '11200206': '11200205,11300007,100395,716', '11200207': '607,831,591,862,11307301', '11200208': '1526,591,570,11200108,725', '11200209': '878', '11101772': '11101770,11101771', '11200211': '826,11409601,932,11307301,581', '11200212': '11200205,11307301,730,723', '11200213': '100205,932,11300007,11200108', '11200214': '11410001,11200110,581,1527,723', '11200215': '11409301,723,11309401,1526,724', '11200216': '11410001,581,11309401,1527,1528', '1637': '1351,1516,1604', '11100512': '11100509,11100510,11100511', '11101205': '1755,11308301', '11101206': '1753,11407501', '11101207': '865,871,874', '11101208': '11101204,200052', '12400034': '11300023,11300024', '11101209': '11409301,11407501,11101210', '11101210': '11309201,100747,11309001', '11101211': '11409301,865,11409601', '11101212': '11308301,11101210', '11101213': '11409001,11408001,11407001', '11101214': '11308301,11309001', '11101219': '11101218', '11101220': '11101222', '11101221': '11101223', '11101882': '11101881', '12400037': '11400014,11400015', '12310095': '11100717', '11200313': '11310801,11308801,724,100204', '11200217': '11410401,100164,11300007,11309401,723', '11200115': '11309802,1530', '11101215': '11310201,11101207', '11200312': '11310401,100204,1530,1532,11200113', '11200218': '11410502,11200108,11307301,1526,720', '11200116': '11308801,11307801,721,100125', '11101216': '11310201,11409601'}

ANIMAL_TYPE_MAP = {'668': '1', '670': '1', '672': '1', '676': '1', '678': '1', '680': '1', '682': '0', '684': '1', '686': '1', '689': '1', '691': '0', '693': '0', '695': '0', '698': '0', '700': '0', '808': '0', '810': '0', '814': '0', '816': '0', '820': '1', '825': '1', '830': '1', '832': '1', '834': '1', '839': '1', '843': '1', '848': '1', '852': '1', '857': '1', '859': '1', '864': '1', '868': '1', '870': '1', '873': '1', '1633': '1', '1731': '0', '1750': '0', '1752': '1', '1830': '0', '100469': '1', '100597': '0', '100702': '1', '100703': '0', '100748': '1', '10300102': '1', '10300105': '1', '10300106': '1', '10305601': '1', '10307001': '0', '10307501': '1', '10308001': '0', '10308501': '1', '10309001': '0', '10309301': '1', '10309601': '1', '10309701': '0', '10310001': '1', '10310002': '0', '10310101': '0', '10310401': '1', '10310501': '0', '10310502': '1'}
# 蔬菜,水果,家禽,家畜
USER_ITEM_MAP = {
'qiqiwo321': '10007301,10006801,10307001,10307501',  # 大蒜 红加仑 渡渡鸟  欧洲盘羊
'shifangfozu1': '950,100595,100597,10305601',    # 大麦 覆盆子 榛鸡  旱獭
'shifangfozu2': '1754,1756,1830,1752',    # 纸莎草 无花果 雷鸟  高加索野牛
'shifangfozu3': '1754,1756,1830,1752',
'shifangfozu4': '1754,1756,1830,1752',
'shifangfozu5': '1754,1756,1830,1752',
'shifangfozu6': '1754,1756,1830,1752',
'shifangfozu7': '1754,1756,1830,1752',
'shifangfozu8': '1754,1756,1830,1752',
'shifangfozu9': '1754,1756,1830,1752',
'shifangfozu10': '1754,1756,1830,1752',
'shifangfozu11': '1754,1756,1830,1752',
'shifangfozu12': '1754,1756,1830,1752',
'shifangfozu13': '1754,1756,1830,1752',
'shifangfozu14': '1754,1756,1830,1752',
'shifangfozu15': '1754,1756,1830,1752',
'shifangfozu16': '1754,1756,1830,1752',
'shifangfozu17': '1754,881,1750,1752',   # 纸莎草 黑加仑子 鹌鹑 高加索野牛
'shifangfozu18': '1754,881,1750,1752',
'shifangfozu19': '1754,881,1750,1752',
'shifangfozu20': '1754,881,1750,1752',
'shifangfozu21': '1754,881,1750,1752',
'shifangfozu22': '1754,881,1750,1752',
'shifangfozu23': '1754,881,1750,1752',
'shifangfozu24': '1754,881,1750,1752',
'shifangfozu25': '1754,881,1750,1752',
'shifangfozu26': '1754,881,1750,1752',
'shifangfozu27': '1754,881,1750,1752',
'shifangfozu28': '1754,881,1750,1752',
'shifangfozu29': '1754,881,1750,1752',
'shifangfozu30': '1754,881,1750,1752',
'shifangfozu31': '1754,881,1750,1752',
'shifangfozu32': '1754,881,1750,1752',
'shifangfozu33': '1754,881,1750,1752',
'shifangfozu34': '1754,881,1750,1752',
'shifangfozu35': '850,881,1750,873',  # 秋葵 黑加仑子 鹌鹑 雪兔
'shifangfozu36': '850,881,1750,873',
'shifangfozu37': '850,881,1750,873',
'shifangfozu38': '850,881,1750,873',
'shifangfozu39': '850,881,1750,873',
'shifangfozu40': '850,881,1750,873',
'shifangfozu41': '850,881,1750,873',
'shifangfozu42': '850,881,1750,873',
'shifangfozu43': '850,881,1750,873',
'shifangfozu44': '850,881,1750,873',
'shifangfozu45': '850,881,1750,873',
'shifangfozu46': '850,881,1750,873',
'shifangfozu47': '850,881,1750,873',
'shifangfozu48': '850,881,1750,873',
'shifangfozu49': '850,881,1750,873',
'shifangfozu50': '850,881,1750,873',
'shifangfozu51': '850,881,1750,873',
'shifangfozu52': '850,881,1750,873',
'shifangfozu53': '850,881,1750,873',
'shifangfozu54': '850,881,1750,873',
'shifangfozu55': '850,881,1750,873',
'shifangfozu56': '584,610,693,820',  # 小麦 塞米龙 杂斑鸡 伊比利亚黑猪
'shifangfozu57': '584,610,693,820',
'shifangfozu58': '584,610,693,820',
'shifangfozu59': '584,610,693,820',
'shifangfozu60': '584,610,693,820',
'shifangfozu61': '584,610,693,820',
'shifangfozu62': '584,610,693,820',
'shifangfozu63': '584,610,693,820',
'shifangfozu64': '584,610,693,820',
'shifangfozu65': '584,610,693,820',
'shifangfozu66': '584,630,693,832',  # 小麦 梅洛 杂斑鸡 皮埃蒙特
'shifangfozu67': '584,630,693,832',
'shifangfozu68': '584,630,693,832',
'shifangfozu69': '584,630,693,832',
'shifangfozu70': '584,630,693,832',
'shifangfozu71': '584,630,693,832',
'shifangfozu72': '584,630,693,832',
'shifangfozu73': '584,630,693,832',
'shifangfozu74': '584,630,693,832',
'shifangfozu75': '566,630,693,686',  # 玉米 梅洛 杂斑鸡 奶牛
'shifangfozu76': '566,630,693,686',
'shifangfozu77': '566,630,693,686',
'shifangfozu78': '566,630,693,686',
'shifangfozu79': '566,630,693,686',
'shifangfozu80': '566,630,693,686',
'shifangfozu81': '566,630,693,686',
'shifangfozu82': '566,630,693,686',
'shifangfozu83': '566,630,693,686',
'shifangfozu84': '580,630,695,689',   # 洋葱 梅洛 杂斑鸭 西蒙塔尔牛
'shifangfozu85': '580,630,695,689',
'shifangfozu86': '580,630,695,689',
'shifangfozu87': '580,630,695,689',
'shifangfozu88': '580,630,695,689',
'shifangfozu89': '580,630,695,689',
'shifangfozu90': '580,630,695,689',
'shifangfozu91': '580,630,695,689',
'shifangfozu92': '580,630,695,689',
'shifangfozu93': '580,630,695,689',
'shifangfozu94': '580,630,695,689',
'shifangfozu95': '580,630,695,689',
'shifangfozu96': '580,630,695,689',
'shifangfozu97': '580,630,695,689',
'shifangfozu98': '580,630,695,689',
'shifangfozu99': '580,630,695,689',
'shifangfozu100': '580,630,695,689',
'shifangfozu101': '580,630,695,689',
'shifangfozu102': '580,630,695,689',
'shifangfozu103': '580,630,695,689',
'shifangfozu104': '580,630,695,689',
'shifangfozu105': '580,630,695,689',
'shifangfozu106': '580,630,695,689',
'shifangfozu107': '580,630,695,689',
'shifangfozu108': '580,630,695,689',
'shifangfozu109': '580,630,695,689',
'shifangfozu110': '580,630,695,689',
'shifangfozu111': '580,630,695,689',
'shifangfozu112': '580,630,695,689',
'shifangfozu113': '580,630,695,689',
'shifangfozu114': '580,630,695,689',
'shifangfozu115': '580,630,695,689',
'shifangfozu116': '580,630,695,689',
'shifangfozu117': '580,630,695,689',
'shifangfozu118': '580,630,695,689',
'shifangfozu119': '580,630,695,689',
'shifangfozu120': '580,630,695,689',
'shifangfozu121': '580,630,695,689',
'shifangfozu122': '580,630,695,689',
'shifangfozu123': '580,630,695,689',
'shifangfozu124': '580,630,695,689',
'shifangfozu125': '580,630,695,689',
'shifangfozu126': '580,630,695,689',
'shifangfozu127': '580,630,695,689',
'shifangfozu128': '580,630,695,689',
'shifangfozu129': '580,630,695,689',
'shifangfozu130': '580,630,695,689',
'shifangfozu131': '580,630,695,689',
'shifangfozu132': '580,630,695,689',
'shifangfozu133': '580,630,695,689',
'shifangfozu134': '580,630,695,689',
'shifangfozu135': '580,630,695,689',
'shifangfozu136': '580,630,695,689',
'shifangfozu137': '580,630,695,689',
'shifangfozu138': '580,630,695,689'
}

DAILY_TASK = {'959', '931', '954', '10205602', '891', '978', '287', '935', '10206001', '10204202', '914', '953', '629', '921', '903', '10203301', '10202202', '222', '979', '942', '10204001', '10204002', '970', '927', '957', '905', '224', '284', '10206801', '611', '984', '280', '917', '972', '912', '975', '982', '10204503', '946', '10201302', '980', '10202901', '10207001', '627', '933', '10202501', '901', '948', '625', '632', '631', '989', '291', '934', '10203501', '10205801', '221', '10207501', '10203101', '932', '896', '949', '973', '941', '10207304', '895', '546', '911', '612', '910', '227', '620', '10204502', '890', '892', '897', '963', '920', '10202201', '965', '10203001', '10204004', '967', '282', '295', '951', '977', '623', '626', '183', '983', '628', '10204003', '633', '936', '919', '906', '907', '987', '184', '898', '10207301', '913', '938', '893', '226', '986', '923', '952', '613', '985', '950', '966', '10207302', '902', '10206501', '958', '964', '960', '10205601', '974', '918', '969', '915', '943', '894', '981', '962', '10201301', '630', '10207303', '899', '10208001', '930', '956', '10205001', '916', '908', '939', '955', '610', '945', '223', '545', '940', '10204203', '988', '928', '298', '929', '10206301', '925', '278', '971', '904', '937', '947', '10204501', '909', '618', '922', '976', '10202001', '10207502', '619', '944', '622', '624', '961', '10204201', '621', '968', '900', '10204204', '926', '10203502', '10205301', '924', '614', '279'}

# 对应Java中的UserInfo模型（用类封装更清晰）
class UserInfo:
    def __init__(self, user_id: str, name: str, z: str, b: str, e: str, money: int, m_coin: int):
        self.user_id = user_id
        self.name = name
        self.z = z
        self.b = b
        self.e = e
        self.money = money
        self.m_coin = m_coin


def get_user_info(userid, sessionId) -> UserInfo:
    """执行钓鱼接口请求"""
    xml = f"""<asCommand><msgType>10</msgType><a>null</a><url>http://coml.manorage.com/manoragecom/0816/</url>
    <userId>{userid}</userId><sessionId>{sessionId}</sessionId>
    <b>null</b></asCommand>"""
    # 去除XML中的换行和空格（与Java拼接格式一致，避免哈希值不一致）
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</asCommand>")
    res = send_request_once(LOGIN_URL, filled_xml)
    root = ET.fromstring(res)
    user_id = root.find("userId").text
    name = root.find("name").text
    z = root.find("z").text
    b = root.find("b").text
    e = root.find("e").text
    m_coin = 0
    money = int(root.find("money").text)
    if root.find("mCoin").text:
        m_coin = int(root.find("mCoin").text)
    # 验证必要字段是否完整
    if not all([user_id, name, z, b, e, money]):
        raise ValueError("XML文件缺少必要节点（userId/name/z/b/e/money）")
    return UserInfo(user_id, name, z, b, e, money, m_coin)

def send_request_once(url: str, param: str):
    """
    批量发送POST请求，忽略响应结果（与Java注释后逻辑一致）
    :param url: 接口URL
    :param param: 请求参数（XML字符串）
    :param times: 调用次数
    """
    headers = {"Content-Type": "text/plain"}  # 适配XML请求体
    try:
        # 发送POST请求（超时时间10秒，防止卡死）
        response = requests.post(
            url=url,
            data=param.encode("utf-8"),
            headers=headers,
            timeout=10
        )
        # 如需解析响应，可在此处调用parse_response方法（与Java一致，暂注释）
        return response.text
    except Exception as e:
        print(f"请求失败（URL：{url}）：{e}")
        return None

# 对应Java的toUnicode方法：将字符串转为十六进制字符拼接
def to_unicode(param1: str, param2=None) -> str:
    """
    等价转换Java的toUnicode，将字符串每个字符转为十六进制，无分隔符拼接
    :param param1: 待转换字符串
    :param param2: 分隔符（Java默认"-"，此处保留参数兼容，实际未使用）
    :return: 十六进制拼接字符串
    """
    if param2 is None:
        param2 = "-"
    result = []
    for char in param1:
        # 转为十六进制，去掉0x前缀，小写（与Java保持一致）
        hex_char = hex(ord(char))[2:]
        result.append(hex_char)
    return "".join(result)


# 对应Java的hash方法（自定义MD5，Python用标准库hashlib实现等价功能）
def custom_hash(param1: str) -> str:
    """
    生成与Java自定义hash等价的MD5十六进制字符串（小写）
    :param param1: 待哈希字符串
    :return: 32位小写MD5哈希值
    """
    # 编码为UTF-8字节流（Java默认平台编码，此处统一UTF-8保证兼容性）
    param_bytes = param1.encode("utf-8")
    # 计算MD5
    md5_obj = hashlib.md5()
    md5_obj.update(param_bytes)
    # 返回小写十六进制结果（与Java的toHex输出格式一致）
    return md5_obj.hexdigest()


# 对应Java的fillWw方法：填充ww节点到XML中
def fill_ww(xml: str, tail: str) -> str:
    """
    替换XML尾部标签，插入<ww>哈希值</ww>
    :param xml: 原始XML字符串
    :param tail: XML尾部标签（如</command>）
    :return: 填充后的XML字符串
    """
    # 计算哈希值（对应Java：hash(xml + color)）
    ww_value = custom_hash(xml + COLOR)
    # 替换尾部标签，插入ww节点
    xml_without_tail = xml.replace(tail, "")
    return f"{xml_without_tail}<ww>{ww_value}</ww>{tail}"


# 对应Java的send方法：批量发送HTTP POST请求
def send_request(url: str, param: str, times: int):
    """
    批量发送POST请求，忽略响应结果（与Java注释后逻辑一致）
    :param url: 接口URL
    :param param: 请求参数（XML字符串）
    :param times: 调用次数
    """
    headers = {"Content-Type": "text/plain"}  # 适配XML请求体
    for _ in range(times):
        try:
            # 发送POST请求（超时时间10秒，防止卡死）
            response = requests.post(
                url=url,
                data=param.encode("utf-8"),
                headers=headers,
                timeout=10
            )
            # 如需解析响应，可在此处调用parse_response方法（与Java一致，暂注释）
            print(response.text)
        except Exception as e:
            print(f"请求失败（URL：{url}）：{e}")


# 对应Java的getFish方法：钓鱼接口调用
def get_fish(user: UserInfo):
    """查询钓鱼信息"""
    xml = f"""<command><msgType>2012120301</msgType>
    <userId>{user.user_id}</userId><y>{user.user_id}</y>
    <z>{user.z}</z></command>"""
    # 去除XML中的换行和空格（与Java拼接格式一致，避免哈希值不一致）
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(QUERY_FISH, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    hf = 3
    for item in items:
        fishId = item.find("fishId").text
        if fishId == "11101710":
            num = int(item.find("num").text)
            if num >= 300:
                hf = 2

    """执行钓鱼接口请求"""
    xml = f"""<command>
<msgType>2012120302</msgType>
<userId>{user.user_id}</userId>
<hf>{hf}</hf>
<y>{user.user_id}</y>
<z>{user.z}</z>
</command>"""
    # 去除XML中的换行和空格（与Java拼接格式一致，避免哈希值不一致）
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request(FISH_URL, filled_xml, 5)

def enter_plant(user: UserInfo, account):
    xml = f"""<x>
  <msgType>40</msgType>
  <a>{user.user_id}</a>
  <userId>{user.user_id}</userId>
  <y>{user.user_id}</y>
  <z>{user.z}</z>
</x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    res = send_request_once(ENTER_PLANT, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    item_arr = []
    for item in items:
        plantStage = item.find("plantStage").text
        if plantStage != "6":
            startTime = int(item.find("startTime").text)
            lifeTime = int(item.find("lifeTime").text)
            milliseconds = int(round(time.time() * 1000))
            if milliseconds > (startTime + lifeTime):
                item_arr.append(item.find("key").text)
    if len(item_arr) > 0:
        get_all_fruit(user, item_arr)
    refresh_plant(user, account)

def refresh_plant(user: UserInfo, account):
    xml = f"""<x>
      <msgType>40</msgType>
      <a>{user.user_id}</a>
      <userId>{user.user_id}</userId>
      <y>{user.user_id}</y>
      <z>{user.z}</z>
    </x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    res = send_request_once(ENTER_PLANT, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    flag = False
    for item in items:
        plantStage = item.find("plantStage").text
        if plantStage == "6":
            flag  = True
    if flag:
        delete_all_dead_plant(user)
    refresh_plant_again(user, account)

def open_rarity_chest(user: UserInfo, item_id, num):
    for i in range(num):
        xml = f"""<x><msgType>284</msgType><a>{item_id}</a><y>{user.user_id}</y><z>{user.z}</z></x>"""
        xml = "".join(xml.split())
        filled_xml = fill_ww(xml, "</x>")
        send_request_once(OPEN_RARITY_CHESTS, filled_xml)

def init_user_task(user: UserInfo):
    xml = f"""<command><msgType>404</msgType><userId>{user.user_id}</userId><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(INIT_USER_TASK, filled_xml)
    root = ET.fromstring(res)
    task_list = root.find("a").text.split(",")
    complete_list = root.find("b").text.split(",")
    for index, complete_task in enumerate(complete_list):
        if complete_task == "0":
            if DAILY_TASK.__contains__(task_list[index]):
                submit_task(user, task_list[index])

chest_map = {
    "1606": "1592",  # 格兰迪之眷恋-图尔斯树皮袋
    "1607": "1605",  # 圣沃维之微-拉普兰羊皮囊
    "1608": "1598",  # 阿西尔之希翼-巴伐利亚兽皮袋
    "12500001": "12400401"  #  波赛多之祈愿-阿特兰亚麻袋
}

chest_keys = ["1606", "1607", "1608", "12500001"]

def query_and_open_chest(user: UserInfo):
    res1 = open_package(user)
    item_arr = []
    check_item(item_arr, chest_keys, res1)
    for item in item_arr:
        if chest_keys.__contains__(item[0]):
            open_rarity_chest(user, chest_map[item[0]], int(item[1]))

def submit_task(user: UserInfo, task_id):
    xml = f"""<command><msgType>406</msgType><userId>{user.user_id}</userId><name>{name_to_unicode(user.name)}</name>
    <taskId>{task_id}</taskId><type>1</type>
    <y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(SUBMIT_PLANT, filled_xml)


def check_plant(user: UserInfo, account):
    xml = f"""<x>
      <msgType>40</msgType>
      <a>{user.user_id}</a>
      <userId>{user.user_id}</userId>
      <y>{user.user_id}</y>
      <z>{user.z}</z>
    </x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    res = send_request_once(ENTER_PLANT, filled_xml)
    root = ET.fromstring(res)
    earthHaveArr = root.find("earthHave").text.split(",")
    titanHaveArr = root.find("titanHave").text.split(",")
    total =  len(titanHaveArr) + len(earthHaveArr)
    items = root.findall("item")
    if items is None:
        account_list.add(account)
    num = 0
    for item in items:
        plantStage = item.find("plantStage").text
        if plantStage != "6":
            num += 1
    if num < total:
        account_list.add(account)

def refresh_plant_again(user: UserInfo, account):
    xml = f"""<x>
      <msgType>40</msgType>
      <a>{user.user_id}</a>
      <userId>{user.user_id}</userId>
      <y>{user.user_id}</y>
      <z>{user.z}</z>
    </x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    res = send_request_once(ENTER_PLANT, filled_xml)
    root = ET.fromstring(res)
    titanPlantied = root.find("titanPlantied").text
    earthPlantied = root.find("earthPlantied").text
    earthHaveArr = root.find("earthHave").text.split(",")
    titanHaveArr = root.find("titanHave").text.split(",")
    check_and_buy(user, len(earthHaveArr), len(titanHaveArr), 1, account)
    itemStr = USER_ITEM_MAP.get(account)
    if itemStr is None:
        print("can not find item by " + account)
        return
    items = itemStr.split(",")
    earth_num = len(earthPlantied.split(","))
    titan_num = len(titanPlantied.split(","))
    if earthPlantied == "no" or  earth_num < len(titanHaveArr):
        to_plant(user, earthHaveArr, items[0], 0)
    if titanPlantied == "no" or titan_num < len(earthHaveArr):
        to_plant(user, titanHaveArr, items[1], 1)


POSITION_MAP = {'0': '295,483', '1': '310,550', '2': '265,625', '3': '423,476', '4': '470,550', '5': '400,625', '6': '550,475', '7': '610,543', '8': '540,618', '9': '670,475', 'A': '716,547', 'B': '660,620', 'C': '790,475', 'D': '855,550', 't0': '489,250', 't1': '427,313', 't2': '335,378', 't3': '606,252', 't4': '535,312', 't5': '465,378', 't6': '725,253', 't7': '648,315', 't8': '595,376', 't9': '763,314', 'tA': '709,375'}

def to_plant(user: UserInfo, arr, item_id, type):
    prefix = ""
    if type == 1:
        prefix = "t"
    for i in  arr:
        index =  prefix + i
        position = POSITION_MAP.get(index)
        xml = f"""<x>
          <msgType>32</msgType>
          <userId>{user.user_id}</userId>
          <plantId>{item_id}</plantId>
          <key>{getKey()}</key>
          <position>{position}</position>
          <earthIndex>{index}</earthIndex>
          <y>{user.user_id}</y>
          <z>{user.z}</z></x>"""
        xml = "".join(xml.split())
        filled_xml = fill_ww(xml, "</x>")
        send_request_once(ADD_PLANT, filled_xml)

def check_and_buy(user: UserInfo, num1, num2, type, account):
    itemStr = USER_ITEM_MAP.get(account)
    if itemStr is None:
        print("can not find item by " + account)
        return
    items= itemStr.split(",")
    item_set = set()
    if type == 1:
        item_set.add(items[0])
        item_set.add(items[1])
    else:
        item_set.add(items[2])
        item_set.add(items[3])
    item_arr = []
    res1 = open_package(user)
    res2 = user_depot(user)
    check_item(item_arr, item_set, res1)
    check_item(item_arr, item_set, res2)
    b0 = True
    b1 = True
    b2 = True
    b3 = True
    for item in item_arr:
        if item[0] == items[0] and int(item[1]) >= int(num1):
            b0 = False
        if item[0] == items[1] and int(item[1]) >= int(num2):
            b1 = False
        if item[0] == items[2] and int(item[1]) >= int(num1):
            b2 = False
        if item[0] == items[3] and int(item[1]) >= int(num2):
            b3 = False
    if type == 1:
        if b0:
            buy_item(user, items[0], num1, 0)
        if b1:
            buy_item(user, items[1], num2, 0)
    else:
        if b2:
            buy_item(user, items[2], num1,3)
        if b3:
            buy_item(user, items[3], num2,3)

def buy_item(user: UserInfo, item_id, num, status):
    xml = f"""<command>
    <msgType>56</msgType>
    <status>{status}</status>
    <userId>{user.user_id}</userId>
    <name>{name_to_unicode(user.name)}</name>
    <itemId>{item_id}</itemId>
    <storeType>0</storeType>
    <type>0</type>
    <itemCount>{num}</itemCount>
    <y>{user.user_id}</y>
    <t>0</t>
    <z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(BUY_ITEM, filled_xml)

def delete_all_dead_plant(user: UserInfo):
    xml = f"""<x>
  <msgType>1778</msgType>
  <y>{user.user_id}</y>
  <z>{user.z}</z></x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    send_request_once(DELETE_ALL_DEAD_PLANT, filled_xml)


def zoon_init(user: UserInfo, account):
    xml = f"""<x>
  <msgType>500</msgType>
  <a>{user.user_id}</a>
  <userId>{user.user_id}</userId>
  <y>{user.user_id}</y>
  <z>{user.z}</z>
</x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    res = send_request_once(ZOON_INIT, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    item_arr = []
    for item in items:
        f = item.find("f").text
        if f != "4":
            startTime = int(item.find("i").text)
            lifeTime = int(item.find("j").text)
            milliseconds = int(round(time.time() * 1000))
            if milliseconds > (startTime + lifeTime):
                item_arr.append(item.find("key").text)
    if len(item_arr) > 0:
        harvest_all(user, item_arr)
    refresh_zoon(user, account)

def refresh_zoon(user: UserInfo, account):
    xml = f"""<x>
      <msgType>500</msgType>
      <a>{user.user_id}</a>
      <userId>{user.user_id}</userId>
      <y>{user.user_id}</y>
      <z>{user.z}</z>
    </x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    res = send_request_once(ZOON_INIT, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    flag = False
    for item in items:
        f = item.find("f").text
        if f == "4":
            flag =  True
    if flag:
        delete_all_animal(user)
    refresh_zoon_again(user, account)

def check_zoon(user: UserInfo, account):
    xml = f"""<x>
      <msgType>500</msgType>
      <a>{user.user_id}</a>
      <userId>{user.user_id}</userId>
      <y>{user.user_id}</y>
      <z>{user.z}</z>
    </x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    res = send_request_once(ZOON_INIT, filled_xml)
    root = ET.fromstring(res)
    fowl_num = int(root.find("a").text)
    farm_num = int(root.find("b").text)
    total = fowl_num + farm_num
    items = root.findall("item")
    if items is None:
        account_list.add(account)
    num = 0
    for item in items:
        f = item.find("f").text
        if f != "4":
            num+=1
    if num < total:
        account_list.add(account)

def refresh_zoon_again(user: UserInfo, account):
    xml = f"""<x>
      <msgType>500</msgType>
      <a>{user.user_id}</a>
      <userId>{user.user_id}</userId>
      <y>{user.user_id}</y>
      <z>{user.z}</z>
    </x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    res = send_request_once(ZOON_INIT, filled_xml)
    root = ET.fromstring(res)
    fowl_num = int(root.find("a").text)
    farm_num = int(root.find("b").text)
    items = root.findall("item")
    fowl = 0
    farm = 0
    for item in items:
        animalId = item.find("animalId").text
        animal_type = ANIMAL_TYPE_MAP.get(animalId)
        if animal_type == "1":
            farm += 1
        if animal_type == "0":
            fowl += 1
    check_and_buy(user, fowl_num, farm_num, 2, account)
    itemStr = USER_ITEM_MAP.get(account)
    if itemStr is None:
        print("can not find item by " + account)
        return
    items = itemStr.split(",")
    if fowl < fowl_num:
        add_animal(user, items[2], fowl_num, 0)
    if farm < farm_num:
        add_animal(user, items[3], farm_num, 1)


def add_animal(user: UserInfo, item_id, num, anamal_type):
    for i in range(num):
        xml = f"""<x>
          <msgType>506</msgType>
          <userId>{user.user_id}</userId>
          <key>{getKey()}</key>
          <animalId>{item_id}</animalId>
          <animalType>{anamal_type}</animalType>
          <y>{user.user_id}</y>
          <z>{user.z}</z></x>"""
        xml = "".join(xml.split())
        filled_xml = fill_ww(xml, "</x>")
        send_request_once(ADD_ANIMAL, filled_xml)

def delete_all_animal(user: UserInfo):
    xml = f"""<x>
  <msgType>1777</msgType>
  <y>{user.user_id}</y>
  <z>{user.z}</z></x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    send_request_once(DELETE_ALL_ANIMAL, filled_xml)


def harvest_all(user: UserInfo, item_arr):
    comma_separated_str = ','.join([item for item in item_arr])
    xml = f"""<command>
  <msgType>1776</msgType>
  <userId>{user.user_id}</userId>
  <key>{comma_separated_str}</key>
  <y>{user.user_id}</y>
  <z>{user.z}</z>
</command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(HARVEST_ALL, filled_xml)

def get_all_fruit(user: UserInfo, item_arr):
    comma_separated_str = ','.join([item for item in item_arr])
    xml = f"""<command>
  <msgType>1775</msgType>
  <userId>{user.user_id}</userId>
  <y>{user.user_id}</y>
  <z>{user.z}</z>
  <keys>{comma_separated_str}</keys></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(GET_ALL_FRUIT, filled_xml)

def player_exchanged_init(user: UserInfo):
    xml = f"""<command><msgType>2012120305</msgType><userId>{user.user_id}</userId><type>2</type><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(PLAYER_EXCHANGED_INIT, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    for item in items:
        if fish_item_set.__contains__(item.find("id").text):
            stockNum = int(item.find("stockNum").text)
            keyId = item.find("keyId").text
            for i in range(stockNum):
                player_exchanged_fishing_item(user, keyId)

def player_exchanged_fishing_item(user: UserInfo, keyId):
    xml = f"""<command><msgType>2012120304</msgType><userId>{user.user_id}</userId><type>2</type><keyId>{keyId}</keyId><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(PLAYER_EXCHANGED_FISHING_ITEM, filled_xml)

# 对应Java的getHunt方法：狩猎接口调用
def get_hunt(user: UserInfo, level: int):
    """执行狩猎接口请求"""
    xml = f"""<x>
<msgType>2522</msgType>
<a>{user.user_id}</a>
<name>{to_unicode(user.name)}</name>
<b>30</b>
<c>1</c>
<d>{level}</d>
<y>{user.user_id}</y>
<z>{user.z}</z>
</x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    send_request(HUNT_URL, filled_xml, 3)


# 对应Java的getCollection方法：收集接口调用
def get_collection(user: UserInfo, level: int):
    """执行收集接口请求"""
    xml = f"""<command>
<msgType>162</msgType>
<userId/>
<name>{to_unicode(user.name)}</name>
<id/>
<quality/>
<numb/>
<a>{level}</a>
<y>{user.user_id}</y>
<z>{user.z}</z>
<b>30</b>
</command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request(COLLECT_URL, filled_xml, 3)

# 对应Java的countLevel2方法：二等伯爵/子爵/二等子爵逻辑
def count_level2(user: UserInfo):
    get_fish(user)
    get_hunt(user, 2)
    get_collection(user, 15)


# 对应Java的count方法：伯爵逻辑
def count(user: UserInfo):
    get_fish(user)
    get_hunt(user, 3)
    get_collection(user, 25)


# 对应Java的marquis方法：终身公爵/侯爵/二等公爵逻辑
def marquis(user: UserInfo):
    get_fish(user)
    get_hunt(user, 3)
    get_collection(user, 45)
    get_collection(user, 25)

def exec_action(user: UserInfo):
    # # 2. 按爵位分支执行逻辑
    if user.e in ["终身公爵", "侯爵", "二等公爵", "公爵"]:
        print("marquis")
        marquis(user)
    elif user.e in ["伯爵", "二等侯爵"]:
        print("count")
        count(user)
    elif user.e in ["二等伯爵", "子爵", "二等子爵"]:
        print("countLevel2")
        count_level2(user)
    else:
        print("爵位不匹配")

def open_package(user: UserInfo):
    """执行狩猎接口请求"""
    xml = f"""<getUserPackage><msgType>50</msgType><userId>{user.user_id}</userId>
        <y>{user.user_id}</y><z>{user.z}</z></getUserPackage>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</getUserPackage>")
    return send_request_once(OPEN_PACKAGE, filled_xml)

def user_depot(user: UserInfo):
    """执行狩猎接口请求"""
    xml = f"""<command><msgType>24</msgType><userId>{user.user_id}</userId><y>{user.user_id}</y>
    <z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    return send_request_once(USER_DEPOT, filled_xml)

def store_item(user: UserInfo):
    item_arr = []
    res1 = open_package(user)
    res2 = user_depot(user)
    check_item(item_arr, trans_item_set ,res1)
    check_item(item_arr, trans_item_set, res2)
    for item in item_arr:
        to_store_item(user, item[0], item[1], item[2])

def check_item(item_arr, s, res):
    root = ET.fromstring(res)
    items = root.findall("item")

    for item in items:
        if s.__contains__(item.find("a").text):
            # item_id  num  f
            item_arr.append((item.find("a").text, item.find("b").text, item.find("c").text))

def to_store_item(user: UserInfo, item_id, item_num, f):
    """执行狩猎接口请求"""
    xml = f"""<command><msgType>2530</msgType><a>{user.user_id}</a><b/><c>0</c><d>{item_id}</d><e>{item_num}</e><f>{f}</f>
    <g>0</g><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(STORE_ITEM, filled_xml)
    print(res)

def get_create_item(user: UserInfo):
    xml = f"""<command><msgType>68</msgType><userId>{user.user_id}</userId><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(QUERY_CREATE_ITEM, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    item_arr = []
    for item in items:
        item_arr.append((item.find("id").text, item.find("userCreateId").text))
    return item_arr

def fetch_item(user: UserInfo, item):
    xml = f"""<command><msgType>62</msgType><userCreateId>{item[1]}</userCreateId><userId>{user.user_id}</userId><id>{item[0]}</id><y>{user.user_id}</y>
    <z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(FETCH_CREATE_ITEM, filled_xml)

def create_item(user: UserInfo, item):
    ele = ITEM_ELEMENT_MAP.get(item[0])
    if ele:
        fmt_ele = generate_element(ele)
        xml = f"""<command><msgType>60</msgType><userId>{user.user_id}</userId><itemId>{item[0]}</itemId><numb>10</numb><y>{user.user_id}</y>
            <z>{user.z}</z>{fmt_ele}</command>"""
        xml = "".join(xml.split())
        filled_xml = fill_ww(xml, "</command>")
        send_request_once(CREATE_ITEM, filled_xml)
    else:
        print("can not find element for " + item[0])

def generate_element(item_str: str) -> str:
    items = item_str.split(",")
    ele = ""
    for item in items:
        quality = ITEM_QUALITY_MAP.get(item)
        if quality:
            ele += f"""<element><id>{item}</id><quality>{quality}</quality></element>"""
        else:
            ele += f"""<element><id>{item}</id><quality>0</quality></element>"""
            print("can not find quality for " + item)
    return ele


def auto_create_item(user: UserInfo):
    item_arr = get_create_item(user)
    for item in item_arr:
        fetch_item(user, item)
    for item in item_arr:
        create_item(user, item)
# 计算 ITEM_QUALITY_MAP 数据
def store_quality(user: UserInfo):
    res1 = open_package(user)
    res2 = user_depot(user)
    check_item_quality_map(res1)
    check_item_quality_map(res2)

def check_item_quality_map(res):
    root = ET.fromstring(res)
    items = root.findall("item")

    for item in items:
        a = item.find("a").text
        c = ITEM_QUALITY_MAP.get(a)
        if (c is None) | (c == "") :
            ITEM_QUALITY_MAP[a] = item.find("c").text

def getKey() -> str:
    # 获取当前时间的毫秒数
    ms = int(time.time() * 1000)
    # 生成 1 ~ 10000 的随机整数（等价 Math.ceil(Math.random() * 10000)）
    rand_num = random.randint(1, 10000)
    # 拼接为字符串返回
    return str(ms) + str(rand_num)

def name_to_unicode(param1: str, param2: str = "-") -> str:
    res = ""
    for char in param1:
        hex_str = hex(ord(char))[2:]
        if len(res) > 1:
            res += param2 + hex_str
        else:
            res = hex_str
    return res

headers = {"Content-Type": "application/x-www-form-urlencoded"}
# 主函数（对应Java的main方法）
def main(account, method_type):
    try:
        data = {
            "userloginid": account,
            "pword": "13934670751abc",
            "auto_login": False
        }
        session = requests.Session()
        login_response = session.post("http://www.139up.com/userLogin.upstapp", headers=headers, data=data)
        if login_response.status_code == 200:
            profile_response = session.get("http://www.139up.com/zysd.jsp")
            if profile_response.status_code == 200:
                pattern = r'http://coml.manorage.com/manoragecom/index.html[^\s]+'
                match = re.findall(pattern, profile_response.text)
                if match:
                    a = len(match[0])
                    b = match[0][55:a - 2].split("&sessionId=")
                    user = get_user_info(b[0], b[1])
                    print(f"{account}, {user.name}, {user.b}, {user.e}")
                    # store_quality(user)
                    # if user.money < 500000:
                    #     print(f"{account}, {user.name}, {user.b}, {user.e}")
                    # if user.m_coin > 0:
                    #     print(f"{account}, {user.name}, {user.m_coin}")
                    if method_type == 1:
                        # 每日采集，狩猎，钓鱼
                        exec_action(user)
                        # 交换鱼
                        player_exchanged_init(user)
                    elif method_type == 2:
                        # 商会存储物品
                        store_item(user)
                    elif method_type == 3:
                        # 加工物品
                        auto_create_item(user)
                    elif method_type == 4:
                        # 种植养殖
                        enter_plant(user, account)
                        zoon_init(user, account)
                    elif method_type == 5:
                        # 检查种植养殖是否遗漏
                        check_plant(user, account)
                        check_zoon(user, account)
                    elif method_type == 6:
                        # 提交每日任务
                        init_user_task(user)
                    elif method_type == 7:
                        # 开袋子
                        query_and_open_chest(user)
                    session.close()
    except Exception as e:
        print(f"程序执行失败：{e}")

def open_box():
    main("qiqiwo321", 7)
    for i in range(1, 83):
        main(f"""shifangfozu{i + 1}""", 7)

def exec_task():
    main("qiqiwo321", 6)
    main("shifangfozu2", 6)
    main("shifangfozu3", 6)
    main("shifangfozu4", 6)
    main("shifangfozu5", 6)
    main("shifangfozu6", 6)
    main("shifangfozu7", 6)
    main("shifangfozu8", 6)
    main("shifangfozu9", 6)
    main("shifangfozu10", 6)
    main("shifangfozu11", 6)
    main("shifangfozu12", 6)
    main("shifangfozu13", 6)
    for i in range(55, 138):
        main(f"""shifangfozu{i + 1}""", 6)

def daily_event(method_type, num):
    start = int(time.time())
    main("qiqiwo321", method_type)
    for i in range(num):
        main(f"""shifangfozu{i + 1}""", method_type)
    end = int(time.time())
    print(end - start)
#
def process_food():
    start = int(time.time())
    main("shifangfozu27", 3)
    main("shifangfozu28", 3)
    main("shifangfozu29", 3)
    main("shifangfozu30", 3)
    end = int(time.time())
    print(end - start)

def shouhuo():
    # daily_event(1, 83)  # 每日采集狩猎钓鱼交换
    daily_event(4, 138)  # 收获
    daily_event(5, 138)  # 校验异常
    for account in account_list:
        main(account, 4)

def test():
    try:
        with open("D://project//zysd//taskInfo.txt", "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                if not line:
                    continue
                row = line.split("ˇ")
                if row[8] == '2':
                    account_list.add(row[0])
    except FileNotFoundError:
        print(f"文件不存")
        return []
    except Exception as e:
        print(f"解析失败：{e}")
        return []
    print(account_list)

trans_item_set = set()
# trans_item_set.add("561")  # 黑麦
# trans_item_set.add("565")  # 西红柿
# trans_item_set.add("572")  # 莴苣
# trans_item_set.add("586")  # 小麦
# trans_item_set.add("567")  # 玉米
# trans_item_set.add("558")  # 白萝卜
# trans_item_set.add("577")  # 蘑菇
# trans_item_set.add("581")  # 洋葱
# trans_item_set.add("878")  # 橄榄
# trans_item_set.add("949")  # 花椰菜
# trans_item_set.add("641")  # 椰枣
# trans_item_set.add("858")  # 利木赞牛
# trans_item_set.add("857")  # 利木赞牛幼崽
# trans_item_set.add("860")  # 奥尔洛夫马
trans_item_set.add("685")  # 猪肉
# trans_item_set.add("671")  # 法国垂耳兔
# trans_item_set.add("821")  # 伊比利亚猪肉
# trans_item_set.add("833")  # 皮埃蒙特牛肉
# trans_item_set.add("669")  # 黄牛肉
# trans_item_set.add("679")  # 羊肉
# trans_item_set.add("673")  # 驴
# trans_item_set.add("831")  # 山羊奶
# trans_item_set.add("701")  # 火鸡肉
# trans_item_set.add("692")  # 白火鸡肉
# trans_item_set.add("593")  # 南瓜
# trans_item_set.add("582")  # 甜菜种子
# trans_item_set.add("583")  # 甜菜
# trans_item_set.add("840")  # 帕尔玛猪肉
# trans_item_set.add("817")  # 莱茵鹅
# trans_item_set.add("709")  # 白玉涅
# trans_item_set.add("611")  # 塞米龙
# trans_item_set.add("629")  # 苏维尼翁
# trans_item_set.add("630")  # 梅洛种子
# trans_item_set.add("631")  # 梅洛
# trans_item_set.add("633")  # 卡本纳弗朗
# trans_item_set.add("681")  # 鹿肉
# trans_item_set.add("690")  # 西蒙塔尔牛肉
# trans_item_set.add("811")  # 肥鹅肝
# trans_item_set.add("607")  # 苹果
# trans_item_set.add("635")  # 柑橘
# trans_item_set.add("638")  # 西柚
# trans_item_set.add("615")  # 板栗
# trans_item_set.add("574")  # 土豆
# trans_item_set.add("844")  # 西芹
# trans_item_set.add("613")  # 草莓
# trans_item_set.add("889")  # 燕麦
# trans_item_set.add("1509")  # 圆木
# trans_item_set.add("200052")  # 石料
# trans_item_set.add("1523")  # 红宝石碎片
# trans_item_set.add("200051")  # 红宝石
# trans_item_set.add("1514")  # 海蓝宝石
# trans_item_set.add("687")  # 牛奶
# trans_item_set.add("694")  # 鸡蛋
# trans_item_set.add("696")  # 鸭蛋
# trans_item_set.add("609")  # 梨
# trans_item_set.add("570")  # 胡萝卜
# trans_item_set.add("683")  # 鸡肉
# trans_item_set.add("699")  # 鸭肉
# trans_item_set.add("891")  # 蓝莓
# trans_item_set.add("730")  # 松露
# trans_item_set.add("835")  # 法兰西马
# trans_item_set.add("825")  # 单峰驼幼崽
# trans_item_set.add("826")  # 单峰驼
# trans_item_set.add("868")  # 阿尔捷金马幼崽
# trans_item_set.add("869")  # 阿尔捷金马
# trans_item_set.add("100598")  # 榛鸡
# trans_item_set.add("865")  # 罗姆尼羊
# trans_item_set.add("1528")  # 杜松子
# trans_item_set.add("909")  # 松子
# trans_item_set.add("1757")  # 无花果
# trans_item_set.add("851")  # 秋葵
# trans_item_set.add("1751")  # 鹌鹑
# trans_item_set.add("874")  # 雪兔
# trans_item_set.add("1831")  # 雷鸟
# trans_item_set.add("1753")  # 高加索野牛
# trans_item_set.add("1755")  # 纸莎草
# trans_item_set.add("882")  # 黑加仑子
# trans_item_set.add("728")  # 密斯卡代勒
# trans_item_set.add("1526")  # 迷迭香
# trans_item_set.add("1531")  # 豆蔻
# trans_item_set.add("862")  # 柠檬
# trans_item_set.add("588")  # 甜椒
# trans_item_set.add("879")  # 牛油果种子
# trans_item_set.add("880")  # 牛油果
# trans_item_set.add("866")  # 樱桃种子
# trans_item_set.add("867")  # 樱桃
# trans_item_set.add("847")  # 荷兰豆
trans_item_set.add("100126")  # 布莱香槟酒
trans_item_set.add("1529")  # 鼠尾草
# trans_item_set.add("933")  # 法式蜗牛
# trans_item_set.add("932")  # 松鸡肉
# trans_item_set.add("727")  # 库隆巴
# trans_item_set.add("729")  # 小维杜
# trans_item_set.add("1530")  # 香荚兰
# trans_item_set.add("1532")  # 薄荷
trans_item_set.add("11101204")  # 大理石
trans_item_set.add("102002")  # 鹿花菌
trans_item_set.add("11100514")  # 琉璃苣
trans_item_set.add("11300010")  # 秋日小圆帽
trans_item_set.add("11300011")  # 毁灭天使
trans_item_set.add("11300012")  # 撒旦的召唤
trans_item_set.add("11300013")  # 骑士头套
trans_item_set.add("11300014")  # 死亡帽
trans_item_set.add("11300015")  # 死亡天使
trans_item_set.add("11300007")  # 羊肚蕈
# trans_item_set.add("1473")  # 红玫瑰种子
# trans_item_set.add("1475")  # 黄玫瑰种子
# trans_item_set.add("1483")  # 白玫瑰种子
# trans_item_set.add("1474")  # 红玫瑰
# trans_item_set.add("1476")  # 黄玫瑰
# trans_item_set.add("1484")  # 白玫瑰

fish_item_set = set()
fish_item_set.add("1009")  # 扩充魔法齿轮
fish_item_set.add("200052")  # 石料
fish_item_set.add("11101204")  # 大理石
fish_item_set.add("1509")  # 圆木
fish_item_set.add("102002")  # 鹿花菌
fish_item_set.add("11100514")  # 琉璃苣
fish_item_set.add("11300011")  # 毁灭天使
fish_item_set.add("11300012")  # 撒旦的召唤

account_list = set()


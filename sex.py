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
GET_SH_ITEEM="http://coml.manorage.com/manorage/commercerActionXmx!getShItem.comapp"
ASSIGN_ITEM="http://coml.manorage.com/manorage/commercerActionXmx!assignItem.comapp"
ADD_CONSIGNMENT="http://coml.manorage.com/manorage/consignment_xmx!addConsignment.comapp"
GET_FRIEND_CONSIGN="http://coml.manorage.com/manorage/consignment!getFriendConsign.comapp"
CONSIGNMENT_BUY="http://coml.manorage.com/manorage/consignment_xmx!consigenmentBuy.comapp"
DELETE_TASK = "http://coml.manorage.com/manorage/task_xbc!deleteTask.comapp"
ACCEPT_TASK = "http://coml.manorage.com/manorage/task_xbc!acceptTask.comapp"

DAILY_TASK_ITEM_MAP = {'183': (['565'], ['100']), '184': (['100141'], ['5']), '221': (['687'], ['50']), '222': (['574'], ['70']), '223': (['607'], ['120']), '224': (['100121'], ['5']), '226': (['100081'], ['10']), '227': (['687'], ['100']), '278': (['100144'], ['3']), '279': (['100227'], ['3']), '280': (['577'], ['80']), '282': (['100201'], ['4']), '284': (['701'], ['100']), '287': (['673'], ['40']), '291': (['581'], ['50']), '295': (['694', '696'], ['30', '30']), '298': (['669'], ['50']), '546': (['631'], ['100']), '610': (['558'], ['120']), '611': (['570'], ['100']), '612': (['693'], ['20']), '613': (['668'], ['20']), '614': (['572'], ['100']), '618': (['577'], ['50']), '619': (['100281'], ['20']), '620': (['613'], ['100']), '621': (['679'], ['35']), '622': (['677'], ['50']), '623': (['100142'], ['5']), '624': (['100236'], ['5']), '625': (['100143'], ['7']), '626': (['583'], ['80']), '627': (['593'], ['100']), '628': (['909'], ['70']), '629': (['607'], ['100']), '630': (['611'], ['100']), '631': (['609'], ['100']), '632': (['100101'], ['5']), '633': (['856'], ['10']), '890': (['558'], ['80']), '891': (['570'], ['50']), '892': (['100202'], ['10']), '893': (['669'], ['100']), '894': (['100398'], ['5']), '895': (['641'], ['100']), '896': (['567'], ['100']), '897': (['671'], ['80']), '898': (['574'], ['30']), '899': (['631'], ['60']), '900': (['100183'], ['10']), '901': (['100228'], ['10']), '902': (['581'], ['100']), '903': (['615'], ['100']), '904': (['100412'], ['1']), '905': (['577'], ['100']), '906': (['581'], ['80']), '907': (['856'], ['5']), '908': (['100127'], ['6']), '909': (['100392'], ['6']), '910': (['683'], ['50']), '911': (['100223'], ['5']), '912': (['882'], ['10']), '913': (['100184'], ['10']), '914': (['100143'], ['10']), '915': (['100231'], ['2']), '916': (['100409'], ['5']), '917': (['574'], ['100']), '918': (['701'], ['60']), '919': (['699'], ['100']), '920': (['100237'], ['5']), '921': (['690'], ['50']), '922': (['692'], ['100']), '923': (['613'], ['60']), '924': (['100204'], ['8']), '925': (['100400'], ['4']), '926': (['577', '629'], ['80', '50']), '927': (['100181'], ['7']), '928': (['100403'], ['4']), '929': (['572'], ['80']), '930': (['588'], ['100']), '931': (['100391'], ['10']), '932': (['570'], ['60']), '933': (['100201'], ['6']), '934': (['561'], ['120']), '935': (['565'], ['150']), '936': (['100413'], ['5']), '937': (['100224'], ['10']), '938': (['607'], ['60']), '939': (['878'], ['30']), '940': (['609'], ['100']), '941': (['100169'], ['8']), '942': (['100233'], ['2']), '943': (['607'], ['120']), '944': (['889'], ['20']), '945': (['100281'], ['10']), '946': (['558', '561'], ['100', '50']), '947': (['629'], ['100']), '948': (['100206'], ['3']), '949': (['100145'], ['5']), '950': (['615'], ['50']), '951': (['685'], ['100']), '952': (['815'], ['25']), '953': (['613'], ['50']), '954': (['100419'], ['5']), '955': (['100171'], ['10']), '956': (['100301'], ['10']), '957': (['867'], ['20']), '958': (['889'], ['50']), '959': (['878'], ['50']), '960': (['100230'], ['1']), '961': (['847'], ['20']), '962': (['100420'], ['2']), '963': (['880'], ['10']), '964': (['809'], ['20']), '965': (['692'], ['80']), '966': (['100361'], ['7']), '967': (['100121'], ['10']), '968': (['100239'], ['10']), '969': (['100234'], ['10']), '970': (['100416'], ['10']), '971': (['100410'], ['1']), '972': (['593'], ['25']), '973': (['588'], ['20']), '974': (['826'], ['20']), '975': (['100418'], ['1']), '976': (['671'], ['20']), '977': (['831'], ['25']), '978': (['100415'], ['2']), '979': (['862'], ['100']), '980': (['826'], ['50']), '981': (['100393'], ['5']), '982': (['891'], ['20']), '983': (['641'], ['50']), '984': (['100235'], ['5']), '985': (['909'], ['20']), '986': (['593'], ['20']), '987': (['100414'], ['10']), '988': (['100392'], ['3']), '989': (['100394'], ['5']), '10201301': (['100169', '100171'], ['10', '10']), '10201302': (['100161', '100127'], ['5', '10']), '10202001': (['1598', '1592'], ['3', '3']), '10202201': (['100241'], ['8']), '10202202': (['100406'], ['10']), '10202501': (['1605', '1598'], ['2', '2']), '10202901': (['11200209'], ['5']), '10203001': (['1592', '12400401'], ['3', '2']), '10203101': (['100413', '100400'], ['5', '5']), '10203301': (['100390'], ['10']), '10203501': (['12400401', '1605'], ['2', '2']), '10203502': (['851', '844'], ['100', '100']), '10204001': (['11101207'], ['5']), '10204002': (['865'], ['45']), '10204003': (['874'], ['50']), '10204004': (['882'], ['80']), '10204201': (['856', '1771'], ['30', '50']), '10204202': (['1732'], ['35']), '10204203': (['100542', '100412'], ['5', '5']), '10204204': (['869'], ['50']), '10204501': (['1753'], ['15']), '10204502': (['1755'], ['35']), '10204503': (['1757'], ['40']), '10205001': (['1831'], ['5']), '10205301': (['951'], ['50']), '10205601': (['11405601'], ['15']), '10205602': (['951', '11405601'], ['50', '20']), '10205801': (['11200301'], ['1']), '10206001': (['100598'], ['10']), '10206301': (['100747'], ['25']), '10206501': (['100749'], ['25']), '10206801': (['11306801'], ['25']), '10207001': (['11407001'], ['20']), '10207301': (['100596'], ['35']), '10207302': (['11200205'], ['1']), '10207303': (['11200207'], ['5']), '10207304': (['11307301'], ['35']), '10207501': (['11407501'], ['20']), '10207502': (['11101206'], ['1']), '10208001': (['11408001'], ['15'])}
QUALITY_ITEM = {'11102004', '844', '100910', '11300036', '1873', '588', '729', '853', '11409601', '100397', '11101988', '11300033', '11101898', '101021', '11300023', '1530', '100184', '11300028', '100392', '100393', '11400023', '871', '100125', '11101996', '11400026', '11101958', '11200213', '11100173', '11101921', '100390', '100166', '11200111', '11300011', '11200103', '11200212', '11300018', '817', '11410001', '1345', '1493', '11200102', '1494', '687', '11300043', '1485', '11400106', '100417', '11307301', '11308301', '11409701', '11200311', '11200114', '1755', '1643', '11101922', '100123', '11101936', '100241', '11400004', '815', '1757', '685', '11101928', '100385', '1528', '100596', '11400114', '102106', '11300025', '100399', '100222', '635', '1511', '11400003', '869', '11300047', '100207', '100404', '11300009', '638', '1814', '11300015', '11310801', '100420', '100491', '11200313', '701', '1495', '11101897', '11306801', '100388', '11101974', '11300044', '856', '100464', '591', '631', '1602', '909', '11200209', '100544', '862', '696', '11300101', '11100172', '100202', '11200301', '11300005', '1732', '11300008', '11101929', '11300039', '11400011', '11400002', '11200104', '11400007', '1597', '11410501', '728', '11200116', '100402', '11200115', '11200304', '1527', '11400111', '102002', '829', '100524', '11409301', '831', '932', '11101204', '100171', '11200202', '11101307', '1751', '100361', '1501', '100546', '840', '1490', '200050', '100233', '11101951', '100903', '11101304', '100124', '1634', '101022', '11300037', '11100193', '11101952', '11400019', '100144', '100465', '100386', '858', '1532', '11101997', '100415', '11300035', '1599', '100324', '100461', '11200203', '11300027', '11200309', '878', '11200210', '100394', '11100180', '11200110', '100396', '11400105', '11200107', '100221', '11300026', '100126', '574', '1667', '11300022', '11400016', '11300041', '1526', '100164', '851', '709', '11101943', '567', '11300102', '11400017', '11200206', '11300021', '11400113', '100621', '100183', '100145', '100263', '100387', '11300007', '11400008', '100204', '1831', '11400020', '100462', '100230', '100487', '100382', '727', '11302001', '11410002', '572', '100101', '581', '100206', '679', '11300003', '11101306', '100281', '100321', '11200113', '874', '11101627', '100237', '867', '1512', '100231', '1640', '833', '101011', '100413', '11200101', '100327', '1342', '100181', '11200305', '100543', '100545', '1496', '11101305', '1872', '100224', '100580', '11300042', '593', '577', '11200217', '1344', '100547', '100234', '747', '100205', '561', '865', '570', '11300012', '11101634', '100169', '11300040', '1771', '11400109', '11300019', '609', '583', '11300103', '100901', '100813', '11200308', '11101973', '100492', '611', '11309401', '690', '11200204', '11200201', '860', '102202', '11309801', '100225', '100235', '1753', '1813', '100384', '11200215', '100403', '11300006', '11200307', '811', '11101989', '11300029', '100416', '11200105', '1509', '1641', '826', '613', '11400006', '11400112', '889', '100482', '11400107', '100405', '835', '565', '11300014', '100325', '100081', '100168', '100323', '11308801', '100414', '1523', '891', '100401', '100419', '11400108', '11101624', '11101967', '100228', '11101631', '11200306', '11101638', '11102005', '11300024', '11300108', '101014', '100170', '933', '11300001', '11200303', '1639', '200052', '100201', '809', '847', '11100197', '11101982', '100175', '1529', '11200207', '100232', '671', '11200214', '11300034', '11409001', '100227', '11400018', '100411', '615', '11100008', '692', '11200106', '100409', '100542', '11200310', '931', '100141', '100236', '11300004', '11300013', '1497', '100904', '100223', '11300046', '100407', '11300104', '880', '681', '558', '11400024', '11307801', '11310002', '100143', '1642', '100816', '11100145', '838', '11101636', '633', '951', '1492', '11400027', '11101942', '683', '11308001', '100562', '100814', '100391', '1237', '11400025', '11300020', '1931', '100383', '11405601', '11101966', '11100187', '100182', '669', '849', '1484', '11200211', '100121', '1531', '11310401', '11300105', '11300002', '100747', '882', '100398', '11300031', '100208', '100412', '100381', '100706', '11200216', '11300010', '11407501', '100165', '11300030', '629', '100172', '11101509', '100142', '11200205', '100470', '1231', '100240', '11309001', '11310001', '1508', '11400012', '11410101', '821', '11300045', '100328', '100705', '100749', '11408001', '699', '11101959', '100239', '607', '11100146', '694', '11309201', '11400005', '11100176', '1491', '11310201', '673', '11300016', '11408501', '11400104', '100481', '641', '11400022', '11400021', '1680', '100598', '1513', '11400103', '1343', '11410401', '100161', '100463', '730', '11400010', '677', '100803', '11200109', '100490', '100811', '11400009', '586', '100167', '11400110', '1665', '100406', '100410', '11200302', '100238', '100262', '100579', '11200218', '11300017', '11300032', '1524', '11200312', '11407001', '100707', '12400006', '11100189', '11400001', '11101935', '11101502', '11101981', '11300038', '100185', '11410502', '949', '845', '100395', '100418', '1638', '11200108', '11200112', '100400', '100408', '100203', '100229', '100127', '102105', '1474', '11309802', '100704', '11200208', '1476', '100301'}
ITEM_ELEMENT_MAP = {'200051': '1523', '1514': '200050', '100281': '583', '100391': '100281,613', '100184': '726,100281', '100225': '726,100281', '100224': '561,724', '100142': '565,572', '100143': '613,687', '100172': '629,721', '100234': '607,586,100281', '100165': '611,629', '100101': '685,725', '100236': '694,724', '100204': '687,100281', '100394': '635,100281,862', '100392': '687,723,725,593,581', '100124': '629,721,728', '100123': '721,728', '100121': '586,687', '100182': '685,724', '100141': '561,685', '100201': '607,613,867', '100403': '572,100281,565,862', '100181': '635,100281', '100228': '687,726,100281', '100393': '100281,891,862', '100168': '450,586,567', '100144': '574,685,723', '100416': '701,720,724,949,570', '100240': '565,723', '100208': '577,685,687,720', '100145': '581,723', '100229': '687,694,889', '100390': '687,100281,880', '100361': '809,100172,731', '100175': '611,629,709', '100171': '629,631,633', '100169': '629,631,633', '100301': '629,631,633', '100127': '629,631,633', '100223': '574,690,720,723', '100237': '581,565,679', '100202': '581,565,723', '100081': '450,561', '100183': '607,635,638', '100232': '687,694,724,889', '100235': '565,574,833', '100398': '724,100281,615', '100161': '611,629,100165', '100239': '681,723,725', '100185': '577,723,833', '100420': '696,723,565,844,862', '100397': '1526,669,574,565,581', '100231': '687,100281,100225,100228', '100395': '1526,725,565,581,100165', '100405': '1531,699,949,570,100181', '100410': '696,724,100281,586,862', '100203': '720,725,821', '100222': '687,724,730,731,811', '100233': '694,724,889,891', '100414': '687,725,100281,586', '100418': '572,949,588,591,844', '100417': '567,581,847,851,878', '100400': '574,683,687,723,838', '100227': '867,100225,100229', '100241': '831,100165', '100407': '1531,811,723,725,100165', '100207': '558,570,574,690', '100170': '611,629,728,100169', '100166': '611,629,709,728', '100206': '725,731,840', '100238': '694,716,724,730', '100221': '586,724,833,100171', '100396': '1531,815,716,723,100171', '100542': '100281,1771', '100230': '687,100228,100229', '100419': '100392,577,683,687,844', '100125': '611,629,709,727,728', '100263': '716,862,878,932', '100415': '100414,572,692', '100413': '694,586,829,100203', '100409': '100301,581,862,865', '100399': '100397,591,570,581,100101', '100167': '611,629,728,100166', '100404': '100395,669,723,100165,731', '100406': '809,720,723,609,100169', '100126': '611,629,100125', '100545': '1530,724,588,1751', '100402': '100395,683,723,581,100171', '100412': '100393,724,100281,882,100184', '100164': '629,631,633,729', '100401': '1529,100400,817,851', '100408': '100395,100241,581,856,858', '100544': '1527,100392,1751,847', '100262': '720,723,933,581,100164', '100411': '100398,100410,100241', '100546': '1532,1757,889,882', '100543': '1529,100398,724,1732,100542', '100205': '565,586,100203,100204', '100547': '100395,725,581,1753', '11200201': '100598,588,856,100395,100127', '11200202': '874,844,909,100747,1528', '11200101': '882,100281,100175', '11200103': '100166,100170,11200101', '11200104': '574,951,11306801,1529', '11200203': '951,100598,100204,724,1526', '11200204': '874,11300007,100411,100747', '11200301': '100411,100228,100596,100390', '11200302': '1757,100227,1530,100172', '11100904': '11100903,100175', '11101701': '11101719', '11101702': '11101719', '11101703': '11101719', '11101704': '11101719', '11101705': '11101719', '11101706': '11101719', '11101707': '11101719', '11101708': '11101719', '11101709': '11101719', '11101710': '11101719', '11101717': '11101719', '11101718': '11101719', '11200105': '951,889,561,1531,1527', '11200106': '1528,11307301,951,1527', '11200107': '574,567,586,11307301,1526', '11200108': '100164,100281,11307801', '11200109': '100175,11308801,11307801,727', '11200110': '11308801,611,11307801,721,729', '11200111': '11200110,100184,1530,709', '11200112': '867,11200110,727', '11200113': '11308801,611,11307801,728', '11200114': '11307801,11308801,721,709,727', '11200303': '1757,11407501,724,100281,1531', '11200304': '11408501,100204,716,565,11200209', '11200305': '11308801,687,100126,11200209,100281', '11200306': '11310001,11309201,100204,687,1531', '11200307': '100227,11309201,11200111,11407501,100281', '11200308': '11309801,11308001,100281,1532,100301', '11200309': '11310001,100225,724,694', '11200310': '11308001,11309801,100241,724,1530', '11200311': '11307801,11308801,100166,889,100204', '11200205': '889,725,11200209,11307301,723', '11200206': '11200205,11300007,100395,716', '11200207': '607,831,591,862,11307301', '11200208': '1526,591,570,11200108,725', '11200209': '878', '11101772': '11101770,11101771', '11200211': '826,11409601,932,11307301,581', '11200212': '11200205,11307301,730,723', '11200213': '100205,932,11300007,11200108', '11200214': '11410001,11200110,581,1527,723', '11200215': '11409301,723,11309401,1526,724', '11200216': '11410001,581,11309401,1527,1528', '1637': '1351,1516,1604', '11100512': '11100509,11100510,11100511', '11101205': '1755,11308301', '11101206': '1753,11407501', '11101207': '865,871,874', '11101208': '11101204,200052', '12400034': '11300023,11300024', '11101209': '11409301,11407501,11101210', '11101210': '11309201,100747,11309001', '11101211': '11409301,865,11409601', '11101212': '11308301,11101210', '11101213': '11409001,11408001,11407001', '11101214': '11308301,11309001', '11101219': '11101218', '11101220': '11101222', '11101221': '11101223', '11101882': '11101881', '12400037': '11400014,11400015', '12310095': '11100717', '11200313': '11310801,11308801,724,100204', '11200217': '11410401,100164,11300007,11309401,723', '11200115': '11309802,1530', '11101215': '11310201,11101207', '11200312': '11310401,100204,1530,1532,11200113', '11200218': '11410502,11200108,11307301,1526,720', '11200116': '11308801,11307801,721,100125', '11101216': '11310201,11409601'}
ANIMAL_TYPE_MAP = {'668': '1', '670': '1', '672': '1', '676': '1', '678': '1', '680': '1', '682': '0', '684': '1', '686': '1', '689': '1', '691': '0', '693': '0', '695': '0', '698': '0', '700': '0', '808': '0', '810': '0', '814': '0', '816': '0', '820': '1', '825': '1', '830': '1', '832': '1', '834': '1', '839': '1', '843': '1', '848': '1', '852': '1', '857': '1', '859': '1', '864': '1', '868': '1', '870': '1', '873': '1', '1633': '1', '1731': '0', '1750': '0', '1752': '1', '1830': '0', '100469': '1', '100597': '0', '100702': '1', '100703': '0', '100748': '1', '10300102': '1', '10300105': '1', '10300106': '1', '10305601': '1', '10307001': '0', '10307501': '1', '10308001': '0', '10308501': '1', '10309001': '0', '10309301': '1', '10309601': '1', '10309701': '0', '10310001': '1', '10310002': '0', '10310101': '0', '10310401': '1', '10310501': '0', '10310502': '1'}

# 蔬菜,水果,家禽,家畜
USER_ITEM_MAP = {
'qiqiwo321': '10007301,10006801,10307001,10307501',  # 大蒜 红加仑 渡渡鸟  欧洲盘羊
'shifangfozu1': '950,100595,100597,10305601',    # 大麦 覆盆子 榛鸡  旱獭
'shifangfozu2': '950,1756,1830,1752',    # 大麦 无花果 雷鸟  高加索野牛
'shifangfozu3': '950,1756,1830,1752',
'shifangfozu4': '950,1756,1830,1752',
'shifangfozu5': '950,1756,1830,1752',
'shifangfozu6': '950,1756,1830,1752',
'shifangfozu7': '950,1756,1830,1752',
'shifangfozu8': '950,1756,1830,1752',
'shifangfozu9': '950,1756,1830,1752',
'shifangfozu10': '950,1756,1830,1752',
'shifangfozu11': '1754,1756,1830,1752', # 纸莎草 无花果 雷鸟  高加索野牛
'shifangfozu12': '1754,1756,1830,1752',
'shifangfozu13': '1754,1756,1830,1752',
'shifangfozu14': '1754,1756,1830,1752',
'shifangfozu15': '1754,1756,1830,1752',
'shifangfozu16': '1754,1756,1830,1752',
'shifangfozu17': '1754,1756,1830,1752',
'shifangfozu18': '1754,1756,1830,1752',
'shifangfozu19': '1754,1756,1750,1752',  # 纸莎草 无花果 鹌鹑 高加索野牛
'shifangfozu20': '1754,1756,1750,1752',
'shifangfozu21': '1754,1756,1750,1752',
'shifangfozu22': '1754,1756,1750,1752',
'shifangfozu23': '1754,1756,1750,1752',
'shifangfozu24': '1754,1756,1750,1752',
'shifangfozu25': '1754,1756,1750,1752',
'shifangfozu26': '1754,1756,1750,1752',
'shifangfozu27': '1754,1756,1750,1752',
'shifangfozu28': '1754,1756,1750,1752',
'shifangfozu29': '1754,1756,1750,1752',
'shifangfozu30': '1754,1756,1750,1752',
'shifangfozu31': '1754,1756,1750,1752',
'shifangfozu32': '1754,1756,1750,1752',
'shifangfozu33': '1754,1756,1750,1752',
'shifangfozu34': '1754,1756,1750,1752',
'shifangfozu35': '1754,1756,1750,1752',
'shifangfozu36': '1754,1756,1750,1752',
'shifangfozu37': '1754,1756,1750,1752',
'shifangfozu38': '1754,1756,1750,1752',
'shifangfozu39': '1754,1756,1750,1752',
'shifangfozu40': '1754,1756,1750,1752',
'shifangfozu41': '1754,1756,1750,1752',
'shifangfozu42': '1754,1756,1750,1752',
'shifangfozu43': '1754,1756,1750,1752',
'shifangfozu44': '1754,1756,1750,1752',
'shifangfozu45': '1754,1756,1750,1752',
'shifangfozu46': '1754,1756,1750,1752',
'shifangfozu47': '1754,1756,1750,1752',
'shifangfozu48': '1754,1756,1750,1752',
'shifangfozu49': '1754,1756,1750,1752',
'shifangfozu50': '1754,1756,1750,1752',
'shifangfozu51': '1754,1756,1750,1752',
'shifangfozu52': '1754,1756,1750,1752',
'shifangfozu53': '1754,1756,1750,1752',
'shifangfozu54': '1754,1756,1750,1752',
'shifangfozu55': '1754,1756,1750,1752',
'shifangfozu56': '850,881,1750,873',  # 秋葵 黑加仑子 鹌鹑 雪兔
'shifangfozu57': '850,881,1750,873',
'shifangfozu58': '850,881,1750,873',
'shifangfozu59': '850,881,1750,873',
'shifangfozu60': '850,881,1750,873',
'shifangfozu61': '560,877,682,668',  # 黑麦 橄榄 灰鸡 黄牛
'shifangfozu62': '560,877,682,668',
'shifangfozu63': '560,877,682,668',
'shifangfozu64': '560,877,682,668',
'shifangfozu65': '560,877,682,668',
'shifangfozu66': '560,877,682,668',
'shifangfozu67': '560,877,682,668',
'shifangfozu68': '560,877,682,668',
'shifangfozu69': '560,877,682,668',
'shifangfozu70': '560,877,682,668',
'shifangfozu71': '560,877,682,668',
'shifangfozu72': '560,877,682,668',
'shifangfozu73': '560,877,682,668',
'shifangfozu74': '560,877,682,668',
'shifangfozu75': '560,877,682,668',
'shifangfozu76': '560,877,682,668',
'shifangfozu77': '560,877,682,668',
'shifangfozu78': '560,877,682,668',
'shifangfozu79': '560,877,682,668',
'shifangfozu80': '560,877,682,668',
'shifangfozu81': '560,877,682,668',
'shifangfozu82': '560,877,682,668',
'shifangfozu83': '560,877,682,668',
'shifangfozu84': '582,890,808,825',   # 甜菜 蓝莓 匈牙利白鹅 单峰驼
'shifangfozu85': '582,890,808,825',
'shifangfozu86': '582,890,808,825',
'shifangfozu87': '582,890,808,825',
'shifangfozu88': '582,890,808,825',
'shifangfozu89': '582,890,808,825',
'shifangfozu90': '582,890,808,825',
'shifangfozu91': '582,890,808,825',
'shifangfozu92': '582,890,808,825',
'shifangfozu93': '582,890,808,825',
'shifangfozu94': '582,890,808,825',
'shifangfozu95': '582,890,808,825',
'shifangfozu96': '582,890,808,825',
'shifangfozu97': '582,890,808,825',
'shifangfozu98': '582,890,808,825',
'shifangfozu99': '582,890,808,825',
'shifangfozu100': '582,890,808,825',
'shifangfozu101': '582,890,808,825',
'shifangfozu102': '582,890,808,825',
'shifangfozu103': '582,890,808,825',
'shifangfozu104': '582,890,808,825',
'shifangfozu105': '582,890,808,825',
'shifangfozu106': '582,890,808,825',
'shifangfozu107': '582,890,808,825',
'shifangfozu108': '582,890,808,825',
'shifangfozu109': '582,890,808,825',
'shifangfozu110': '582,890,808,825',
'shifangfozu111': '582,890,808,825',
'shifangfozu112': '582,890,808,825',
'shifangfozu113': '582,890,808,825',
'shifangfozu114': '582,890,808,825',
'shifangfozu115': '582,890,808,825',
'shifangfozu116': '582,890,808,825',
'shifangfozu117': '582,890,808,825',
'shifangfozu118': '582,890,808,825',
'shifangfozu119': '582,890,808,825',
'shifangfozu120': '582,890,808,825',
'shifangfozu121': '582,890,808,825',
'shifangfozu122': '582,890,808,825',
'shifangfozu123': '582,890,808,825',
'shifangfozu124': '582,890,808,825',
'shifangfozu125': '582,890,808,825',
'shifangfozu126': '582,890,808,825',
'shifangfozu127': '582,890,808,825',
'shifangfozu128': '582,890,808,825',
'shifangfozu129': '582,890,808,825',
'shifangfozu130': '582,890,808,825',
'shifangfozu131': '582,890,808,825',
'shifangfozu132': '582,890,808,825',
'shifangfozu133': '582,890,808,825',
'shifangfozu134': '582,890,808,825',
'shifangfozu135': '582,890,808,825',
'shifangfozu136': '582,890,808,825',
'shifangfozu137': '582,890,808,825',
'shifangfozu138': '582,890,808,825'
}

# 对应Java中的UserInfo模型（用类封装更清晰）
class UserInfo:
    def __init__(self, user_id: str, name: str, z: str, b: str, e: str, money: int, m_coin: int, k: int):
        self.user_id = user_id
        self.name = name
        self.z = z
        self.b = b
        self.e = e
        self.money = money
        self.m_coin = m_coin
        self.k = k


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
    k = root.find("k").text
    m_coin = 0
    money = int(root.find("money").text)
    if root.find("mCoin").text:
        m_coin = int(root.find("mCoin").text)
    # 验证必要字段是否完整
    if not all([user_id, name, z, b, e, money]):
        raise ValueError("XML文件缺少必要节点（userId/name/z/b/e/money）")
    return UserInfo(user_id, name, z, b, e, money, m_coin, int(k))

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
            task_id = task_list[index]
            daily_task_info = DAILY_TASK_ITEM_MAP.get(task_id)
            if daily_task_info:
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

def delete_task(user: UserInfo, task_id):
    xml = f"""<x><msgType>262</msgType><a/><b>{task_id}</b><y>{user.user_id}</y><z>{user.z}</z></x>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</x>")
    send_request_once(DELETE_TASK, filled_xml)

def accept_task(user: UserInfo, task_id):
    xml = f"""<command><msgType>402</msgType><userId>{user.user_id}</userId><taskId>{task_id}</taskId><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(ACCEPT_TASK, filled_xml)

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
    if earthPlantied == "no" or  earth_num < len(earthHaveArr):
        to_plant(user, earthHaveArr, items[0], 0)
    if titanPlantied == "no" or titan_num < len(titanHaveArr):
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
def get_collection(user: UserInfo, level: int, num: int):
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
    send_request(COLLECT_URL, filled_xml, num)

def exec_action(user: UserInfo):
    get_fish(user)
    if user.k < 5:
        return
    elif 5 <= user.k < 9:
        get_hunt(user, 2)
        get_collection(user, 15, 3)
    elif 9 <= user.k < 11:
        get_hunt(user, 3)
        get_collection(user, 25, 3)
    elif user.k == 11:
        get_hunt(user, 3)
        get_collection(user, 45, 1)
        get_collection(user, 25, 3)
    elif user.k == 12:
        get_hunt(user, 3)
        get_collection(user, 45, 2)
        get_collection(user, 25, 3)
    elif user.k > 12:
        get_hunt(user, 3)
        get_collection(user, 45, 3)
        get_collection(user, 25, 3)



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
        if QUALITY_ITEM.__contains__(item):
            ele += f"""<element><id>{item}</id><quality>0</quality></element>"""
        else:
            ele += f"""<element><id>{item}</id><quality>no</quality></element>"""
    return ele


def auto_create_item(user: UserInfo):
    item_arr = get_create_item(user)
    for item in item_arr:
        fetch_item(user, item)
    for item in item_arr:
        create_item(user, item)

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
                    print(f"{account}, {user.name}, {user.b}, {user.e}, {user.k}")
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

user_id_list = []
def caculate_money(account):
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
                    if user.money < 500000:
                        print(f"{account}, {user.name}, {user.b}, {user.e}")
                        user_id_list.append(user.user_id)
                    session.close()
    except Exception as e:
        print(f"程序执行失败：{e}")

def distribute_money(user: UserInfo):
    if len(user_id_list) > 0:
        user_ids = ",".join(user_id_list)
        xml = f"""<command><msgType>2532</msgType><a>{user.user_id}</a><b/><c>{user_ids}</c><d/><e/><f/><g>5000000</g><y>{user.user_id}</y><z>{user.z}</z></command>"""
        xml = "".join(xml.split())
        filled_xml = fill_ww(xml, "</command>")
        send_request_once(ASSIGN_ITEM, filled_xml)

def assign_item(user: UserInfo, item_id, item_num):
    xml = f"""<command><msgType>2532</msgType><a>{user.user_id}</a><b/><c>{user.user_id}</c><d>{item_id}</d><e>{item_num}</e><f>0</f><g>0</g>
    <y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(ASSIGN_ITEM, filled_xml)


def get_sh_item(user: UserInfo):
    xml = f"""<command><msgType>2528</msgType><a>{user.user_id}</a><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(GET_SH_ITEEM, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    for item in items:
        item_id = item.find("a").text
        if trans_item_set.__contains__(item_id):
            item_num = item.find("b").text
            assign_item(user, item_id, item_num)

def add_consignment(from_user: UserInfo, to_user: UserInfo, item):
    xml = f"""<command><msgType>88</msgType><itemId>{item[0]}</itemId><numb>{item[1]}</numb><quality>0</quality><unitPrice>0</unitPrice><time>6</time>
    <destId>{to_user.user_id}</destId><y>{from_user.user_id}</y><z>{from_user.z}</z><userId>{from_user.user_id}</userId></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(ADD_CONSIGNMENT, filled_xml)

def buy_consignment(user: UserInfo, id):
    xml = f"""<command><msgType>80</msgType><userId>{user.user_id}</userId><id>{id}</id><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    send_request_once(CONSIGNMENT_BUY, filled_xml)

def get_friend_consign(user: UserInfo):
    xml = f"""<command><msgType>90</msgType><userId>{user.user_id}</userId><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(GET_FRIEND_CONSIGN, filled_xml)
    root = ET.fromstring(res)
    items = root.findall("item")
    for item in items:
        id = item.find("id").text
        buy_consignment(user, id)


def to_transform(from_user: UserInfo, to_user: UserInfo):
    get_sh_item(from_user)
    item_arr = []
    res1 = open_package(from_user)
    res2 = user_depot(from_user)
    check_item(item_arr, trans_item_set, res1)
    check_item(item_arr, trans_item_set, res2)
    for item in item_arr:
        add_consignment(from_user, to_user, item)
        get_friend_consign(to_user)

def tansform_item(from_accounts, to_account):
    try:
        data = {
            "userloginid": to_account,
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
                    to_user = get_user_info(b[0], b[1])
                    for from_account in from_accounts:
                        from_data = {
                            "userloginid": from_account,
                            "pword": "13934670751abc",
                            "auto_login": False
                        }
                        from_session = requests.Session()
                        from_login_response = from_session.post("http://www.139up.com/userLogin.upstapp", headers=headers, data=from_data)
                        if from_login_response.status_code == 200:
                            from_profile_response = from_session.get("http://www.139up.com/zysd.jsp")
                            if from_profile_response.status_code == 200:
                                match = re.findall(pattern, from_profile_response.text)
                                if match:
                                    a = len(match[0])
                                    b = match[0][55:a - 2].split("&sessionId=")
                                    from_user = get_user_info(b[0], b[1])
                                    to_transform(from_user, to_user)
                        from_session.close()
                    store_item(to_user)
        session.close()
    except Exception as e:
        print(f"程序执行失败：{e}")

MAIN_USER_ITEM_INFO = {}

def set_item(res):
    root = ET.fromstring(res)
    items = root.findall("item")
    for item in items:
        MAIN_USER_ITEM_INFO[item.find("a").text] = int(item.find("b").text)


def init_main_user_package(user: UserInfo):
    res1 = open_package(user)
    res2 = user_depot(user)
    set_item(res1)
    set_item(res2)

lack_item_ids = set()

def caculate_daily_task_item(main_user: UserInfo, user: UserInfo):
    xml = f"""<command><msgType>404</msgType><userId>{user.user_id}</userId><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(INIT_USER_TASK, filled_xml)
    root = ET.fromstring(res)
    task_list = root.find("a").text.split(",")
    complete_list = root.find("b").text.split(",")
    for index, complete_task in enumerate(complete_list):
        if complete_task == "0":
            task_id = task_list[index]
            need_item_info = DAILY_TASK_ITEM_MAP.get(task_id)
            if need_item_info:
                need_item_ids = need_item_info[0]
                need_item_count = need_item_info[1]
                for index, item_id in enumerate(need_item_ids):
                    main_item_num = MAIN_USER_ITEM_INFO.get(item_id, 0)
                    item_num = int(need_item_count[index])
                    if main_item_num >= item_num:
                        add_consignment(main_user, user, (item_id, item_num, 0))
                        get_friend_consign(user)
                        MAIN_USER_ITEM_INFO[item_id] = main_item_num - item_num
                    else:
                        lack_item_ids.add(item_id)
            else:
                print(f"can not find need item info by task_id {task_id}")

def tansform_daily_task_item():
    try:
        data = {
            "userloginid": "qiqiwo321",
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
                    main_user = get_user_info(b[0], b[1])
                    init_main_user_package(main_user)
                    for i in range(83, 138):
                        from_data = {
                            "userloginid": f"shifangfozu{i+1}",
                            "pword": "13934670751abc",
                            "auto_login": False
                        }
                        to_session = requests.Session()
                        to_login_response = to_session.post("http://www.139up.com/userLogin.upstapp",
                                                                headers=headers, data=from_data)
                        if to_login_response.status_code == 200:
                            to_profile_response = to_session.get("http://www.139up.com/zysd.jsp")
                            if to_profile_response.status_code == 200:
                                match = re.findall(pattern, to_profile_response.text)
                                if match:
                                    a = len(match[0])
                                    b = match[0][55:a - 2].split("&sessionId=")
                                    to_user = get_user_info(b[0], b[1])
                                    if i > 50 and to_user.k == 9:
                                        continue
                                    caculate_daily_task_item(main_user, to_user)
                        to_session.close()
        session.close()
        if len(lack_item_ids) > 0:
            print("缺少每日物品：" + ",".join(lack_item_ids))
    except Exception as e:
        print(f"程序执行失败：{e}")

NOBILITY_ITEM_DICT = {"560": 250,"687": 360,"573": 50,"557": 50,"564": 100,"606": 100,"608": 100,"566": 200,"568": 200,"584": 400,"683": 200,"699": 200,"890": 30,"730": 50,"846": 100,"870": 50,"834": 200,"825": 200,"672": 200,"833": 500,"1523": 20,"100204": 110,"100165": 15,"100168": 250,"100399": 5,"100404": 5,"100126": 5,"100205": 10,"100143": 1,"100228": 1,"100234": 1,"100141": 50,"100081": 200,"100236": 50,"100262": 10,"100361": 20,"100224": 100,"100121": 50}

def to_tansform_nobility_item(main_user: UserInfo, user: UserInfo):
    for k, v in NOBILITY_ITEM_DICT.items():
        have_item_num = MAIN_USER_ITEM_INFO.get(k, 0)
        if have_item_num >= v:
            add_consignment(main_user, user, (k, v, 0))
            get_friend_consign(user)
            MAIN_USER_ITEM_INFO[k] = have_item_num - v
        else:
            print(f"缺少物品：{k}")

def check_nobility_item(account_num):
    res = False
    for k, v in NOBILITY_ITEM_DICT.items():
        num = MAIN_USER_ITEM_INFO.get(k, 0)
        need_num = v * account_num
        if num < need_num:
            res = True
            print(f"lack item: {k}")
    return res

NOBILITY_TASK_IDS = []

def complete_nobility_task(user: UserInfo):
    xml = f"""<command><msgType>404</msgType><userId>{user.user_id}</userId><y>{user.user_id}</y><z>{user.z}</z></command>"""
    xml = "".join(xml.split())
    filled_xml = fill_ww(xml, "</command>")
    res = send_request_once(INIT_USER_TASK, filled_xml)
    root = ET.fromstring(res)
    task_list = root.find("a").text.split(",")
    complete_list = root.find("b").text.split(",")
    for index, complete_task in enumerate(complete_list):
        if complete_task == "0":
            task_id = task_list[index]
            delete_task(user, task_id)
    for task_id in NOBILITY_TASK_IDS:
        accept_task(user, task_id)
        submit_task(user, task_id)

def tansform_nobility_item():
    try:
        data = {
            "userloginid": "qiqiwo321",
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
                    main_user = get_user_info(b[0], b[1])
                    init_main_user_package(main_user)
                    # 校验物品数量
                    if check_nobility_item(27):
                        return
                    for i in range(68, 96):
                        from_data = {
                            "userloginid": f"shifangfozu{i+1}",
                            "pword": "13934670751abc",
                            "auto_login": False
                        }
                        to_session = requests.Session()
                        to_login_response = to_session.post("http://www.139up.com/userLogin.upstapp",
                                                                headers=headers, data=from_data)
                        if to_login_response.status_code == 200:
                            to_profile_response = to_session.get("http://www.139up.com/zysd.jsp")
                            if to_profile_response.status_code == 200:
                                match = re.findall(pattern, to_profile_response.text)
                                if match:
                                    a = len(match[0])
                                    b = match[0][55:a - 2].split("&sessionId=")
                                    to_user = get_user_info(b[0], b[1])
                                    print(f"转移账号：shifangfozu{i+1}")
                                    to_tansform_nobility_item(main_user, to_user)
                                    complete_nobility_task()
                        to_session.close()
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

def process_food():
    start = int(time.time())
    main("shifangfozu27", 3)
    main("shifangfozu28", 3)
    main("shifangfozu29", 3)
    main("shifangfozu30", 3)
    end = int(time.time())
    print(end - start)

def shouhuo():
    # daily_event(1, 138)  # 每日采集狩猎钓鱼交换
    daily_event(4, 138)  # 收获
    daily_event(5, 138)  # 校验异常
    for account in account_list:
        main(account, 4)

def assign_money():
    print("商会1分配金币==============")
    for i in range(69):
        if i == 54:
            continue
        caculate_money(f"""shifangfozu{i + 1}""")
    for i in range(83, 114):
        caculate_money(f"""shifangfozu{i + 1}""")
    try:
        data = {
            "userloginid": "qiqiwo321",
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
                    distribute_money(user)
        session.close()
    except Exception as e:
        print(f"程序执行失败：{e}")

    user_id_list.clear()
    print("商会2分配金币==============")
    caculate_money(f"""shifangfozu55""")
    for i in range(69, 83):
        caculate_money(f"""shifangfozu{i + 1}""")
    try:
        data = {
            "userloginid": "shifangfozu55",
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
                    distribute_money(user)
        session.close()
    except Exception as e:
        print(f"程序执行失败：{e}")


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
# trans_item_set.add("685")  # 猪肉
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
# trans_item_set.add("100281")  # 糖
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
# trans_item_set.add("951")  # 大麦
# trans_item_set.add("882")  # 黑加仑子
# trans_item_set.add("1771")  # 石榴
# trans_item_set.add("100595")  # 覆盆子
# trans_item_set.add("728")  # 密斯卡代勒
# trans_item_set.add("1526")  # 迷迭香
# trans_item_set.add("1531")  # 豆蔻
# trans_item_set.add("1527")  # 肉桂
# trans_item_set.add("862")  # 柠檬
# trans_item_set.add("588")  # 甜椒
# trans_item_set.add("879")  # 牛油果种子
# trans_item_set.add("880")  # 牛油果
# trans_item_set.add("866")  # 樱桃种子
# trans_item_set.add("867")  # 樱桃
# trans_item_set.add("847")  # 荷兰豆
# trans_item_set.add("100126")  # 布莱香槟酒
# trans_item_set.add("1529")  # 鼠尾草
# trans_item_set.add("933")  # 法式蜗牛
# trans_item_set.add("932")  # 松鸡肉
# trans_item_set.add("727")  # 库隆巴
# trans_item_set.add("729")  # 小维杜
# trans_item_set.add("1530")  # 香荚兰
# trans_item_set.add("1532")  # 薄荷
# trans_item_set.add("1509")  # 圆木
# trans_item_set.add("200052")  # 石料
# trans_item_set.add("1523")  # 红宝石碎片
# trans_item_set.add("200051")  # 红宝石
# trans_item_set.add("1514")  # 海蓝宝石
# trans_item_set.add("11101204")  # 大理石
# trans_item_set.add("102002")  # 鹿花菌
# trans_item_set.add("11100514")  # 琉璃苣
# trans_item_set.add("11300010")  # 秋日小圆帽
# trans_item_set.add("11300011")  # 毁灭天使
# trans_item_set.add("11300012")  # 撒旦的召唤
# trans_item_set.add("11300013")  # 骑士头套
# trans_item_set.add("11300014")  # 死亡帽
# trans_item_set.add("11300015")  # 死亡天使
# trans_item_set.add("11300007")  # 羊肚蕈
# trans_item_set.add("1473")  # 红玫瑰种子
# trans_item_set.add("1475")  # 黄玫瑰种子
# trans_item_set.add("1483")  # 白玫瑰种子
# trans_item_set.add("1474")  # 红玫瑰
# trans_item_set.add("1476")  # 黄玫瑰
# trans_item_set.add("1484")  # 白玫瑰

fish_item_set = set()
fish_item_set.add("1009")  # 扩充魔法齿轮
fish_item_set.add("1514")  # 海蓝宝石
fish_item_set.add("200051")  # 红宝石
fish_item_set.add("200052")  # 石料
fish_item_set.add("11101204")  # 大理石
fish_item_set.add("1509")  # 圆木
fish_item_set.add("102002")  # 鹿花菌
fish_item_set.add("11100514")  # 琉璃苣
fish_item_set.add("11300011")  # 毁灭天使
fish_item_set.add("11300012")  # 撒旦的召唤

account_list = set()


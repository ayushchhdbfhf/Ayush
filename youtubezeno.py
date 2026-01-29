import os
import json
import sys
import shutil
import tempfile
import time
import base64
import subprocess
import asyncio
from asyncio import run as arun
from highrise import BaseBot, __main__
from highrise.models import User, SessionMetadata, Position
from highrise import *
from highrise.webapi import *
from highrise.models_webapi import *
from highrise.models import *
import socket
import aiohttp
import aiofiles
import yt_dlp
from mutagen.mp3 import MP3
from collections import deque
import random
from datetime import datetime, timedelta
from HRDB import ownerz, playlist, user_ticket, vip_users, msg, restrict, promo, bot_location, ids

# Icecast server configuration
SERVER_HOST = "54.39.103.199" # dont change.
SERVER_PORT = 3103 # dont change
MOUNT_POINT = "/avsmusic" # put ur mountpoint after / in ""
STREAM_USERNAME = "source" # dont change
STREAM_PASSWORD = "XZMPfKJH"#"put your password"


emote_dict = {
    '1': ('idle-loop-sitfloor', 22.321055),
    '2': ('idle-enthusiastic', 15.941537),
    '3': ('emote-yes', 2.565001),
    '4': ('emote-wave', 2.690873),
    '5': ('emote-tired', 4.61063),
    '6': ('emote-snowball', 5.230467),
    '7': ('emote-snowangel', 6.218627),
    '8': ('emote-shy', 4.477567),
    '9': ('emote-sad', 5.411073),
    '10': ('emote-no', 2.703034),
    '11': ('emote-model', 6.490173),
    '12': ('emote-laughing', 2.69161),
    '13': ('emote-kiss', 2.387175),
    '14': ('emote-hot', 4.353037),
    '15': ('emote-hello', 2.734844),
    '16': ('emote-greedy', 4.639828),
    '17': ('emote-curtsy', 2.425714),
    '18': ('emote-confused', 8.578827),
    '19': ('emote-charging', 8.025079),
    '20': ('emote-bow', 3.344036),
    '21': ('emoji-thumbsup', 2.702369),
    '22': ('emoji-gagging', 5.500202),
    '23': ('emoji-flex', 2.099351),
    '24': ('emoji-celebrate', 3.412258),
    '25': ('emoji-angry', 5.760023),
    '26': ('dance-tiktok8', 11),
    '27': ('dance-tiktok2', 10.392353),
    '28': ('dance-shoppingcart', 4.316035),
    '29': ('dance-russian', 10.252905),
    '30': ('dance-pennywise', 4.214349),
    '31': ('dance-macarena', 12.214141),
    '32': ('dance-blackpink', 7.150958),
    '33': ('emote-hyped', 7.492423),
    '34': ('dance-jinglebell', 10.958832),
    '35': ('idle-nervous', 21.714221),
    '36': ('idle-toilet', 32.174447),
    '37': ('idle-floating', 27.791175),
    '38': ('dance-zombie', 12.922772),
    '39': ('emote-astronaut', 13.791175),
    '40': ('emote-swordfight', 5.914365),
    '41': ('emote-timejump', 4.007305),
    '42': ('emote-snake', 5.262578),
    '43': ('emote-float', 8.995302),
    '44': ('emote-telekinesis', 10.492032),
    '45': ('dance-pinguin', 11.58291),
    '46': ('dance-creepypuppet', 6.416121),
    '47': ('emote-sleigh', 11.333165),
    '48': ('emote-maniac', 4.906886),
    '49': ('emote-energyball', 7.575354),
    '50': ('emote-superpose', 4.530791),
    '51': ('emote-cute', 6.170464),
    '52': ('idle_singing', 13.791175),
    '53': ('emote-frog', 14.55257),
    '54': ('dance-tiktok9', 11.892918),
    '55': ('dance-weird', 21.556237),
    '56': ('dance-tiktok10', 8.225648),
    '57': ('emote-pose7', 4.655283),
    '58': ('emote-pose8', 4.808806),
    '59': ('idle-dance-casual', 9.079756),
    '60': ('emote-pose1', 2.825795),
    '61': ('emote-pose3', 5.10562),
    '62': ('emote-pose5', 4.621532),
    '63': ('emote-cutey', 3.26032),
    '64': ('emote-punkguitar', 9.365807),
    '65': ('emote-fashionista', 5.606485),
    '66': ('emote-gravity', 8.955966),
    '67': ('dance-icecream', 14.769573),
    '68': ('dance-wrong', 12.422389),
    '69': ('idle-uwu', 24.761968),
    '70': ('idle-dance-tiktok4', 15.500708),
    '71': ('emote-shy2', 4.989278),
    '72': ('dance-anime', 8.46671),
    '73': ('dance-kawai', 10.290789),
    '74': ('idle-wild', 26.422824),
    '75': ('emote-iceskating', 7.299156),
    '76': ('emote-pose6', 5.375124),
    '77': ('emote-celebrationstep', 3.353703),
    '78': ('emote-creepycute', 7.902453),
    '79': ('emote-pose10', 3.989871),
    '80': ('emote-boxer', 5.555702),
    '81': ('emote-headblowup', 11.667537),
    '82': ('emote-pose9', 4.583117),
    '83': ('emote-teleporting', 11.7676),
    '84': ('dance-touch', 11.7),
    '85': ('idle-guitar', 13.229398),
    '86': ('emote-gift', 5.8),
    '87': ('dance-employee', 8),
    '88': ('emote-looping', 8),
    '89': ('emote-kissing-bound', 10),
    '90': ('emote-zombierun', 9.182984),
    '91': ('emote-frustrated', 5.584622),
    '92': ('emote-slap', 2.724945),
    '93': ('emote-shrink', 8.738784),
    '94': ('dance-voguehands', 9.150634),
    '95': ('dance-smoothwalk', 6.690023),
    '96': ('dance-singleladies', 21.191372),
    '97': ('dance-orangejustice', 6.475263),
    '98': ('dance-metal', 15.076377),
    '99': ('dance-handsup', 22.283413),
    '100': ('dance-duckwalk', 11.748784),
    '101': ('dance-aerobics', 8.796402),
    '102': ('dance-sexy', 12.30883),
    '103': ('idle-dance-tiktok7', 12.956484),
    '104': ('sit-relaxed', 29.889858),
    '105': ('sit-open', 26.025963),
    '106': ('emoji-there', 2.059095),
    '107': ('emoji-sneeze', 2.996694),
    '108': ('emoji-smirking', 4.823158),
    '109': ('emoji-sick', 5.070367),
    '110': ('emoji-scared', 3.008487),
    '111': ('emoji-punch', 1.755783),
    '112': ('emoji-pray', 4.503179),
    '113': ('emoji-poop', 4.795735),
    '114': ('emoji-naughty', 4.277602),
    '115': ('emoji-mind-blown', 2.397167),
    '116': ('emoji-lying', 6.313748),
    '117': ('emoji-halo', 5.837754),
    '118': ('emoji-hadoken', 2.723709),
    '119': ('emoji-give-up', 5.407888),
    '120': ('emoji-dizzy', 4.053049),
    '121': ('emoji-crying', 3.696499),
    '122': ('emoji-clapping', 2.161757),
    '123': ('emoji-arrogance', 6.869441),
    '124': ('emoji-ghost', 3.472759),
    '125': ('emoji-eyeroll', 3.020264),
    '126': ('idle-fighter', 17.19123),
    '127': ('emote-wings', 13.134487),
    '128': ('emote-think', 3.691104),
    '129': ('emote-theatrical', 8.591869),
    '130': ('emote-tapdance', 11.057294),
    '131': ('emote-superrun', 6.273226),
    '132': ('emote-superpunch', 3.751054),
    '133': ('emote-sumo', 10.868834),
    '134': ('emote-suckthumb', 4.185944),
    '135': ('emote-splitsdrop', 4.46931),
    '136': ('emote-secrethandshake', 3.879024),
    '137': ('emote-ropepull', 8.769656),
    '138': ('emote-roll', 3.560517),
    '139': ('emote-rofl', 6.314731),
    '140': ('emote-robot', 7.607362),
    '141': ('emote-rainbow', 2.813373),
    '142': ('emote-proposing', 4.27888),
    '143': ('emote-peekaboo', 3.629867),
    '144': ('emote-peace', 5.755004),
    '145': ('emote-panic', 2.850966),
    '146': ('emote-ninjarun', 4.754721),
    '147': ('emote-nightfever', 5.488424),
    '148': ('emote-monster_fail', 4.632708),
    '149': ('emote-levelup', 6.0545),
    '150': ('emote-laughing2', 5.056641),
    '151': ('emote-kicking', 4.867992),
    '152': ('emote-jumpb', 3.584234),
    '153': ('emote-judochop', 2.427442),
    '154': ('emote-jetpack', 16.759457),
    '155': ('emote-hugyourself', 4.992751),
    '156': ('emote-harlemshake', 13.558597),
    '157': ('emote-happy', 3.483462),
    '158': ('emote-handstand', 4.015678),
    '159': ('emote-gordonshuffle', 8.052307),
    '160': ('emote-ghost-idle', 19.570492),
    '161': ('emote-gangnam', 7.275486),
    '162': ('emote-fainting', 18.423499),
    '163': ('emote-fail2', 6.475972),
    '164': ('emote-fail1', 5.617942),
    '165': ('emote-exasperatedb', 2.722748),
    '166': ('emote-exasperated', 2.367483),
    '167': ('emote-elbowbump', 3.799768),
    '168': ('emote-disco', 5.366973),
    '169': ('emote-disappear', 6.195985),
    '170': ('emote-deathdrop', 3.762728),
    '171': ('emote-death2', 4.855549),
    '172': ('emote-death', 6.615967),
    '173': ('emote-dab', 2.717871),
    '174': ('emote-cold', 3.664348),
    '175': ('emote-bunnyhop', 12.380685),
    '176': ('emote-boo', 4.501502),
    '177': ('emote-baseball', 7.254841),
    '178': ('emote-apart', 4.809542),
    '179': ('emote-attention', 4.401206),
    '180': ('emote-hearteyes', 4.034386),
    '181': ('emote-heartfingers', 4.001974),
    '182': ('emote-heartshape', 6.232394),
    '183': ('emote-hug', 3.503262),
    '184': ('emote-embarrassed', 7.414283),
    '185': ('emote-puppet', 16.325823),
    '186': ('idle_zombie', 28.754937),
    '187': ('idle_layingdown2', 21.546653),
    '188': ('idle_layingdown', 24.585168),
    '189': ('idle-sleep', 22.620446),
    '190': ('idle-sad', 24.377214),
    '191': ('idle-posh', 21.851256),
    '192': ('idle-loop-tired', 21.959007),
    '193': ('idle-loop-tapdance', 6.261593),
    '194': ('idle-loop-shy', 16.47449),
    '195': ('idle-loop-sad', 6.052999),
    '196': ('idle-loop-happy', 18.798322),
    '197': ('idle-loop-annoyed', 17.058522),
    '198': ('idle-loop-aerobics', 8.507535),
    '199': ('idle-lookup', 22.339865),
    '200': ('idle-hero', 21.877099),
    '201': ('idle-floorsleeping2', 17.253372),
    '202': ('idle-floorsleeping', 13.935264),
    '203': ('idle-dance-headbobbing', 25.367458),
    '204': ('idle-angry', 25.427848),
    '205': ('dance-hipshake', 12.8),
    '206': ('dance-tiktok11', 11.0),
    '207': ('emote-cutesalute', 3.0),
    '208': ('emote-salute', 3.0),
    '209': ('idle_tough', 18.0),
    '210': ('emote-fail3', 4.2),
    '211': ('emote-theatrical-test', 6.5),
    '212': ('emote-receive-happy', 3.5),
    '213': ('emote-confused2', 8.0),
    '214': ('dance-shuffle', 8.5),
    '215': ('idle-cold', 18.0),
    '216': ('mining-mine', 8.0),
    '217': ('mining-success', 3.5),
    '218': ('fishing-pull', 4.5),
    '219': ('fishing-idle', 15.0),
    '220': ('fishing-cast', 4.0),
    '221': ('fishing-pull-small', 5.0),
    '222': ('dance-fruity', 9.0),
    '223': ('dance-cheerleader', 8.5),
    '224': ('dance-tiktok14', 11.0),
    '225': ('emote-howl', 7.0),
    '226': ('idle-howl', 20.0),
    '227': ('emote-trampoline', 8.0),
    '228': ('emote-launch', 3.5),
    '229': ('emote-stargazer', 6.0),
    '230': ('dance-freshprince', 14.86),
    '231': ("idle-headless", 41.802306),
    '232': ("emote-gooey", 5.819651),
    '233': ("emote-electrified", 5.287880),
    'sit': ('idle-loop-sitfloor', 22.321055),
    'enthused': ('idle-enthusiastic', 15.941537),
    'yes': ('emote-yes', 2.565001),
    'wave': ('emote-wave', 2.690873),
    'tired': ('emote-tired', 4.61063),
    'snowball': ('emote-snowball', 5.230467),
    'snowangel': ('emote-snowangel', 6.218627),
    'shy': ('emote-shy', 4.477567),
    'sad': ('emote-sad', 5.411073),
    'no': ('emote-no', 2.703034),
    'model': ('emote-model', 6.490173),
    'lust': ('emote-lust', 4.655965),
    'laughing': ('emote-laughing', 2.69161),
    'kiss': ('emote-kiss', 2.387175),
    'hot': ('emote-hot', 4.353037),
    'hello': ('emote-hello', 2.734844),
    'greedy': ('emote-greedy', 4.639828),
    'curtsy': ('emote-curtsy', 2.425714),
    'confused': ('emote-confused', 8.578827),
    'charging': ('emote-charging', 8.025079),
    'bow': ('emote-bow', 3.344036),
    'thumb': ('emoji-thumbsup', 2.702369),
    'gagging': ('emoji-gagging', 5.500202),
    'flex': ('emoji-flex', 2.099351),
    'cursing': ('emoji-cursing', 2.382069),
    'celebrate': ('emoji-celebrate', 3.412258),
    'angry': ('emoji-angry', 5.760023),
    'tiktok8': ('dance-tiktok8', 11),
    'tiktok2': ('dance-tiktok2', 10.392353),
    'shoppingcart': ('dance-shoppingcart', 4.316035),
    'russian': ('dance-russian', 10.252905),
    'pennywise': ('dance-pennywise', 1.214349),  # Fixed duration (was 4.214349 in `motes`?)
    'macarena': ('dance-macarena', 12.214141),
    'blackpink': ('dance-blackpink', 7.150958),
    'hyped': ('emote-hyped', 7.492423),
    'jinglebell': ('dance-jinglebell', 10.958832),
    'nervous': ('idle-nervous', 21.714221),
    'toilet': ('idle-toilet', 32.174447),
    'floating': ('idle-floating', 27.791175),
    'zombie': ('dance-zombie', 12.922772),
    'astronaut': ('emote-astronaut', 13.791175),
    'swordfight': ('emote-swordfight', 5.914365),
    'timejump': ('emote-timejump', 4.007305),
    'snake': ('emote-snake', 5.262578),
    'float': ('emote-float', 8.995302),
    'telekinesis': ('emote-telekinesis', 10.492032),
    'pinguin': ('dance-pinguin', 11.58291),
    'creepypuppet': ('dance-creepypuppet', 6.416121),
    'bike': ('emote-sleigh', 11.333165),
    'mani': ('emote-maniac', 4.906886),
    'energyball': ('emote-energyball', 7.575354),
    'superpose': ('emote-superpose', 4.530791),
    'cute': ('emote-cute', 6.170464),
    'tiktok9': ('dance-tiktok9', 11.892918),
    'weird': ('dance-weird', 21.556237),
    'tiktok10': ('dance-tiktok10', 8.225648),
    'pose7': ('emote-pose7', 4.655283),
    'pose8': ('emote-pose8', 4.808806),
    'dance-casual': ('idle-dance-casual', 9.079756),
    'pose1': ('emote-pose1', 2.825795),
    'pose3': ('emote-pose3', 5.10562),
    'pose5': ('emote-pose5', 4.621532),
    'cutey': ('emote-cutey', 3.26032),
    'punk': ('emote-punkguitar', 9.365807),
    'fashion': ('emote-fashionista', 5.606485),
    'gravity': ('emote-gravity', 8.955966),
    'icecream': ('dance-icecream', 14.769573),
    'wrong': ('dance-wrong', 12.422389),
    'uwu': ('idle-uwu', 24.761968),
    'sayso': ('idle-dance-tiktok4', 15.500708),
    'bashful': ('emote-shy2', 4.989278),
    'anime': ('dance-anime', 8.46671),
    'kawai': ('dance-kawai', 10.290789),
    'wild': ('idle-wild', 26.422824),
    'iceskating': ('emote-iceskating', 7.299156),
    'pose6': ('emote-pose6', 5.375124),
    'suii': ('emote-celebrationstep', 3.353703),
    'creepycute': ('emote-creepycute', 7.902453),
    'pose10': ('emote-pose10', 3.989871),
    'boxer': ('emote-boxer', 5.555702),
    'blow': ('emote-headblowup', 11.667537),
    'ditzy': ('emote-pose9', 4.583117),
    'teleporting': ('emote-teleporting', 11.7676),
    'touch': ('dance-touch', 11.7),
    'guitar': ('idle-guitar', 13.229398),
    'gift': ('emote-gift', 5.8),
    'employee': ('dance-employee', 8),
    'looping': ('emote-looping', 8),
    'smooch': ('emote-kissing-bound', 10),
    'camera': ('idle-phone-camera', 14.8),
    'phone': ('emote-phone', 9),
    'knock': ('knocking-screen', 7.5),
    'twerk': ('dance-twerk', 8.7),
    'singing': ('idle_singing', 13.791175),
    'frog': ('emote-frog', 14.55257),
    'zombierun': ('emote-zombierun', 9.182984),
    'frustrated': ('emote-frustrated', 5.584622),
    'slap': ('emote-slap', 2.724945),
    'kawaii': ('emote-kawaiigogo', 10.0),
    'shrink': ('emote-shrink', 8.738784),
    'vogue': ('dance-voguehands', 9.150634),
    'spiritual': ('dance-spiritual', 15.795092),
    'smoothwalk': ('dance-smoothwalk', 6.690023),
    'singleladies': ('dance-singleladies', 21.191372),
    'robotic': ('dance-robotic', 17.814959),
    'orange': ('dance-orangejustice', 6.475263),
    'metal': ('dance-metal', 15.076377),
    'handsup': ('dance-handsup', 22.283413),
    'floss': ('dance-floss', 21.329661),
    'duckwalk': ('dance-duckwalk', 11.748784),
    'breakdance': ('dance-breakdance', 17.623849),
    'aerobics': ('dance-aerobics', 8.796402),
    'sexy': ('dance-sexy', 12.30883),
    'tiktok7': ('idle-dance-tiktok7', 12.956484),  # Fixed key (was 'dance-tiktok7')
    'repose': ('sit-relaxed', 29.889858),
    'laid': ('sit-open', 26.025963),
    'poke': ('emoji-there', 2.059095),
    'sneeze': ('emoji-sneeze', 2.996694),
    'smirking': ('emoji-smirking', 4.823158),
    'sick': ('emoji-sick', 5.070367),
    'scared': ('emoji-scared', 3.008487),
    'punch': ('emoji-punch', 1.755783),
    'pray': ('emoji-pray', 4.503179),
    'stinky': ('emoji-poop', 4.795735),
    'naughty': ('emoji-naughty', 4.277602),
    'mind-blown': ('emoji-mind-blown', 2.397167),
    'lying': ('emoji-lying', 6.313748),
    'halo': ('emoji-halo', 5.837754),
    'hadoken': ('emoji-hadoken', 2.723709),
    'give-up': ('emoji-give-up', 5.407888),
    'dizzy': ('emoji-dizzy', 4.053049),
    'crying': ('emoji-crying', 3.696499),
    'clapping': ('emoji-clapping', 2.161757),
    'arrogance': ('emoji-arrogance', 6.869441),
    'ghosts': ('emoji-ghost', 3.472759),
    'eyeroll': ('emoji-eyeroll', 3.020264),
    'fighter': ('idle-fighter', 17.19123),
    'wings': ('emote-wings', 13.134487),
    'think': ('emote-think', 3.691104),
    'theatrical': ('emote-theatrical', 8.591869),
    'tapdance': ('emote-tapdance', 11.057294),
    'run': ('emote-superrun', 6.273226),
    'superpunch': ('emote-superpunch', 3.751054),
    'sumo': ('emote-sumo', 10.868834),
    'suckthumb': ('emote-suckthumb', 4.185944),
    'split': ('emote-splitsdrop', 4.46931),
    'handshake': ('emote-secrethandshake', 3.879024),
    'ropepull': ('emote-ropepull', 8.769656),  # Fixed key (was 'ropel')
    'roll': ('emote-roll', 3.560517),
    'rofl': ('emote-rofl', 6.314731),
    'robot': ('emote-robot', 7.607362),
    'rainbow': ('emote-rainbow', 2.813373),
    'proposing': ('emote-proposing', 4.27888),
    'peekaboo': ('emote-peekaboo', 3.629867),
    'peace': ('emote-peace', 5.755004),
    'panic': ('emote-panic', 2.850966),
    'ninja': ('emote-ninjarun', 4.754721),
    'nightfever': ('emote-nightfever', 5.488424),
    'monster_fail': ('emote-monster_fail', 4.632708),
    'levelup': ('emote-levelup', 6.0545),
    'laugh': ('emote-laughing2', 5.056641),
    'kick': ('emote-kicking', 4.867992),
    'jumpb': ('emote-jumpb', 3.584234),
    'judochop': ('emote-judochop', 2.427442),
    'jetpack': ('emote-jetpack', 16.759457),
    'hugyourself': ('emote-hugyourself', 4.992751),
    'hero-idle': ('idle-hero', 21.877099),  # Fixed key (was duplicate 'hero')
    'headball': ('emote-headball', 10.073119),
    'harlem': ('emote-harlemshake', 13.558597),
    'happy': ('emote-happy', 3.483462),
    'handstand': ('emote-handstand', 4.015678),
    'graceful': ('emote-graceful', 3.7498),
    'moonwalk': ('emote-gordonshuffle', 8.052307),
    'ghost': ('emote-ghost-idle', 19.570492),
    'gangnam': ('emote-gangnam', 7.275486),
    'frollicking': ('emote-frollicking', 3.700665),
    'faint': ('emote-fainting', 18.423499),
    'fall': ('emote-fail2', 6.475972),
    'falling': ('emote-fail1', 5.617942),
    'exasperatedb': ('emote-exasperatedb', 2.722748),
    'exasperated': ('emote-exasperated', 2.367483),
    'elbowbump': ('emote-elbowbump', 3.799768),
    'disco': ('emote-disco', 5.366973),
    'disappear': ('emote-disappear', 6.195985),
    'deathdrop': ('emote-deathdrop', 3.762728),
    'death2': ('emote-death2', 4.855549),
    'death': ('emote-death', 6.615967),
    'dab': ('emote-dab', 2.717871),
    'cold': ('emote-cold', 3.664348),
    'bunny': ('emote-bunnyhop', 12.380685),
    'boo': ('emote-boo', 4.501502),
    'baseball': ('emote-baseball', 7.254841),
    'apart': ('emote-apart', 4.809542),
    'attention': ('emote-attention', 4.401206),
    'hearteyes': ('emote-hearteyes', 4.034386),
    'heartfingers': ('emote-heartfingers', 4.001974),
    'heartshape': ('emote-heartshape', 6.232394),
    'hug': ('emote-hug', 3.503262),
    'lagughing': ('emote-lagughing', 1.125537),
    'embarrassed': ('emote-embarrassed', 7.414283),
    'puppet': ('emote-puppet', 16.325823),
    'rest': ('sit-idle-cute', 17.062613),
    'zombie-idle': ('idle_zombie', 28.754937),
    'relax': ('idle_layingdown2', 21.546653),
    'attentive': ('idle_layingdown', 24.585168),
    'sleep': ('idle-sleep', 22.620446),
    'pouty': ('idle-sad', 24.377214),
    'posh': ('idle-posh', 21.851256),
    'tired-loop': ('idle-loop-tired', 21.959007),
    'tapdance': ('idle-loop-tapdance', 6.261593),
    'shy-loop': ('idle-loop-shy', 16.47449),
    'sad-loop': ('idle-loop-sad', 6.052999),
    'chilling': ('idle-loop-happy', 18.798322),
    'annoyed': ('idle-loop-annoyed', 17.058522),
    'aerobics-loop': ('idle-loop-aerobics', 8.507535),
    'ponder': ('idle-lookup', 22.339865),
    'relaxing': ('idle-floorsleeping2', 17.253372),
    'cozy': ('idle-floorsleeping', 13.935264),
    'swinging': ('idle-dance-swinging', 13.198551),
    'dance-headbobbing': ('idle-dance-headbobbing', 25.367458),
    'angry-idle': ('idle-angry', 25.427848),  # Fixed key (was duplicate 'angry')
    'call': ('idle-phone-talking', 14.8),
    'phone-camera': ('idle-phone-camera', 14.8),
    'phone-emote': ('emote-phone', 9),  # Fixed key (was duplicate 'phone')
    'knock': ('knocking-screen', 7.5),
    'fresh': ('dance-freshprince', 14.86),
    'twerk': ('dance-twerk', 8.7),
    'headless': ("idle-headless", 41.802306),
    'gooey': ("emote-gooey", 5.819651),
    'electrified': ("emote-electrified", 5.287880),
}

AUDIO_FILES = [
    "Nothing.mp3"
]

class BotDefinition:
    def __init__(self, bot: BaseBot, room_id: str, api_token: str):
        self.bot = bot
        self.room_id = room_id
        self.api_token = api_token

class SEA(BaseBot):
    def __init__(self):
        super().__init__()
        self.message_task = None
        self.notification_task = None
        self.promo_task = None
        self.username = None
        self.owner_id = None
        self.owner = None
        self.bot_id = None
        self.skip = False
        self.bitrate = '128k'
        self.invite = "68047d6d5b6d38c275af4cf1"
        self.choices = {}
        self.active_sos_requests = {}
        self.req_files = deque()
        self.now = deque()
        self.message = deque()
        self.wait = []
        self.user_positions = {}
        self.state_file = "bot_state.json"
        self.req_files_dir = "./reqfiles"
        self.fav_dir = "./fav"
        os.makedirs(self.fav_dir, exist_ok=True)
        os.makedirs(self.req_files_dir, exist_ok=True)
        self.load_state()

        self.dance_loop_running = False

    def save_state(self):
        """Save the current state of the req_files deque, with updated file paths."""
        try:
            data = {
                "req_files": [
                    {
                        "title": item["title"],
                        "url": item["url"],
                        "duration": item["duration"],
                        "user": item["user"]
                    }
                    for item in self.req_files
                ]
            }
            with open(self.state_file, "w") as f:
                json.dump(data, f)
        except Exception as e:
            print(f"Error saving state: {type(e).__name__} - {e}")

    def load_state(self):
        """Load the saved state of the req_files deque from a JSON file."""
        if os.path.exists(self.state_file):
            try:
                with open(self.state_file, "r") as f:
                    data = json.load(f)
                    self.req_files = deque(data.get("req_files", []))
                    os.remove(self.state_file)
            except Exception as e:
                print(f"Error loading state: {type(e).__name__} - {e}")

    def move_files_and_update_urls(self):
        for item in self.req_files:
            if item["url"].startswith("/tmp/"):
                temp_file_path = item["url"]
                new_file_path = os.path.join(self.req_files_dir, os.path.basename(temp_file_path))

                try:
                    shutil.move(temp_file_path, new_file_path)
                    item["url"] = new_file_path
                except Exception as e:
                    print(f"Error moving file {temp_file_path} to {new_file_path}: {type(e).__name__} - {e}")

    async def restart_bot(self):
        self.move_files_and_update_urls()
        self.save_state()
        await asyncio.sleep(5)
        os.execv(sys.executable, [sys.executable, 'run.py'] + sys.argv[1:])


    async def _dance_loop(self):
        """ تشغيل حلقة الرقص مع إعادة المحاولة عند فشل الاتصال """
        while self.dance_loop_running:
            try:
                await self.highrise.send_emote("emote-hyped")
                await asyncio.sleep(7.3)
            except Exception as e:
                break  # إذا كان الخطأ غير متوقع، نوقف الحلقة
    
    async def on_start(self, session_metadata: SessionMetadata):
        try:
            self.username = await self.get_username(session_metadata.user_id)
            self.bot_id = session_metadata.user_id
            self.owner_id = session_metadata.room_info.owner_id
            self.owner = await self.get_username(self.owner_id)
        except Exception as e:
            print("Error in get username, and bot id on start:", e)

        if not (self.owner is None):
            if self.owner not in ownerz:
                ownerz.append(self.owner)
            else:
                pass
        else:
            pass

        if not (self.owner_id is None):
            if self.owner_id not in msg:
                msg.append(self.owner_id)
            else:
                pass
        else:
            pass

        if bot_location:
            await self.highrise.teleport(session_metadata.user_id, Position(**bot_location))
            # تشغيل حلقة الرقص
            self.dance_loop_running = True
            self.dance_loop_task = asyncio.create_task(self._dance_loop())
        else:
            await self.highrise.teleport(session_metadata.user_id, Position(15.5, 0.25, 2.5, 'FrontRight'))
            # تشغيل حلقة الرقص
            self.dance_loop_running = True
            self.dance_loop_task = asyncio.create_task(self._dance_loop())

        if self.notification_task is None or self.notification_task.done():
            self.notification_task = asyncio.create_task(self.notification())
        else:
            pass

        if self.message_task is None or self.message_task.done():
            self.message_task = asyncio.create_task(self.print_messages())

        if self.promo_task is None or self.promo_task.done():
            self.promo_task = asyncio.create_task(self.promo())
        print(f"{self.username} is alive.")

    async def on_message(self, user_id: str, conversation_id: str, is_new_conversation: bool) -> None:
        try:
            response = await self.highrise.get_messages(conversation_id)
            if isinstance(response, GetMessagesRequest.GetMessagesResponse):
                message = response.messages[0].content
                if message != "/verify":
                    if user_id not in ids:
                        ids.append(user_id)
                    return
            username = await self.get_username(user_id)
            info = await self.webapi.get_user(user_id)
            joined_at = info.user.joined_at
            if isinstance(joined_at, datetime):
                one_month_ago = datetime.now(joined_at.tzinfo) - timedelta(days=90)
                if joined_at <= one_month_ago:
                    if not username in user_ticket:
                        user_ticket[username] = 3
                        await self.highrise.send_message(conversation_id, "Your account is verified.")
                        await self.highrise.send_message(conversation_id, "You got 3 free tickets")
                        if not user_id in ids:
                            ids.append(user_id)
                else:
                    await self.highrise.send_message(conversation_id, "Sorry, it looks like your account is less than 3 months old, so you cant verify just yet.")
                    await asyncio.sleep(3)
                    await self.highrise.send_message(conversation_id,"We're just trying to keep things fair and avoid alt accounts grabbing free tickets.\nThanks for understanding! ⏳️")
        except Exception as e:
            print(e)

    async def loop_emote(self, user_id, emote_name: str) -> None:
        emote_id, emote_duration = emote_dict.get(emote_name.lower(), (None, None))
        if not emote_id:
            await self.highrise.send_whisper(user_id, "Invalid emote")
            return

        while True:
            room_users = (await self.highrise.get_room_users()).content
            user_in_room = any(room_user.id == user_id for room_user, pos in room_users)

            if not user_in_room:
                break

            try:
                await self.highrise.send_emote(emote_id, user_id)
            except:
                pass

            await asyncio.sleep(emote_duration + 0.1)

    async def loop(self, user_id, emote_name: str) -> None:
        taskgroup = self.highrise.tg
        task_list: list[asyncio.Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user_id:
                task.cancel()
        task = taskgroup.create_task(self.loop_emote(user_id, emote_name))
        task.set_name(user_id)

    async def stop(self, user_id, message: str) -> None:
        taskgroup = self.highrise.tg
        task_list: list[asyncio.Task] = list(taskgroup._tasks)
        for task in task_list:
            if task.get_name() == user_id:
                task.cancel()
                await self.highrise.send_whisper(user_id, "Emote loop stopped.")
              
    async def get_username(self, user_id):
        user_info = await self.webapi.get_user(user_id)
        return user_info.user.username
    
    async def invite_all(self, user):
        if not user.username in ownerz:
            await self.highrise.send_whisper(user.id, "You cant use this command.")
            return
        try:
            for erm in ids:
                message_id = f"1_on_1:{erm}:{self.bot_id}"
            await self.highrise.send_message(
                message_id,
                message_type="invite",
                content="Join this room!", 
                room_id=self.invite)
            await asyncio.sleep(3)
        except Exception as e:
            await self.highrise.chat(f"error: {e}")
            
    async def color(self: BaseBot, category: str, color_palette: int):
        outfit = (await self.highrise.get_my_outfit()).outfit
        for outfit_item in outfit:
            item_category = outfit_item.id.split("-")[0]
            if item_category == category:
                try:
                    outfit_item.active_palette = color_palette
                except:
                    await self.highrise.chat(f"The bot isn't using any item from the category '{category}'.")
                    return
        await self.highrise.set_outfit(outfit)
        
    async def equip(self, item_name: str):
        items = (await self.webapi.get_items(item_name=item_name)).items
        if not items:
            await self.highrise.chat(f"Item '{item_name}' not found.")
            return
        
        item = items[0]
        item_id, category = item.item_id, item.category

        inventory = (await self.highrise.get_inventory()).items
        has_item = any(inv_item.id == item_id for inv_item in inventory)

        if not has_item:
            if item.rarity == Rarity.NONE:
                pass
            elif not item.is_purchasable:
                await self.highrise.chat(f"Item '{item_name}' can't be purchased.")
                return
            else:
                try:
                    response = await self.highrise.buy_item(item_id)
                    if response != "success":
                        await self.highrise.chat(f"Failed to purchase item '{item_name}'.")
                        return
                    await self.highrise.chat(f"Item '{item_name}' purchased.")
                except Exception as e:
                    await self.highrise.chat(f"Error purchasing '{item_name}': {e}")
                    return

        new_item = Item(
            type="clothing",
            amount=1,
            id=item_id,
            account_bound=False,
            active_palette=0,
        )

        outfit = (await self.highrise.get_my_outfit()).outfit
        outfit = [
            outfit_item
            for outfit_item in outfit
            if outfit_item.id.split("-")[0][0:4] != category[0:4]
        ]

        if category == "hair_front" and item.link_ids:
            hair_back_id = item.link_ids[0]
            hair_back = Item(
                type="clothing",
                amount=1,
                id=hair_back_id,
                account_bound=False,
                active_palette=0,
            )
            outfit.append(hair_back)
        outfit.append(new_item)
        await self.highrise.set_outfit(outfit)
    async def remove(self: BaseBot, category: str):
        outfit = (await self.highrise.get_my_outfit()).outfit

        for outfit_item in outfit:
            item_category = outfit_item.id.split("-")[0][0:3]
            if item_category == category[0:3]:
                try:
                    outfit.remove(outfit_item)
                except Exception as e:
                     pass
                     return
            await self.highrise.set_outfit(outfit)

    async def on_chat(self, user: User, message: str):
        
        if message.lower().lstrip().startswith(( "stop", "0", "/stop")):
            await self.stop(user, message)
        
        if message.strip().lower() in emote_dict:
            try:
                if user.id not in ids:
                    await self.highrise.send_whisper(user.id, "Youre not verifired Dm this bot to get verified")
                    return
                await self.loop(user.id, message.strip().lower())
            except:
                pass
        
        if ((parts := message.strip().lower().split(maxsplit=1))[0] == "mute" and user.username in ownerz):
            try:
                if len(parts) > 1 and parts[1].startswith("@"):
                    target_username = parts[1][1:]  # Remove '@'
                    target_user = await self.webapi.get_users(username=target_username)
                    if target_user.total == 0:
                        await self.highrise.send_whisper(user.id, "User not found.")
                        return
                    user_id = target_user.users[0].user_id
                    if user_id:
                        await self.highrise.moderate_room(user_id, "mute", 3600)
            except:
                pass
        
        if ((parts := message.strip().lower().split(maxsplit=1))[0] == "unmute" and user.username in ownerz):
            try:
                if len(parts) > 1 and parts[1].startswith("@"):
                    target_username = parts[1][1:]  # Remove '@'
                    target_user = await self.webapi.get_users(username=target_username)
                    if target_user.total == 0:
                        await self.highrise.send_whisper(user.id, "User not found.")
                        return
                    user_id = target_user.users[0].user_id
                    if user_id:
                        await self.highrise.moderate_room(user_id, "mute", 1)
            except:
                pass
            
        if ((parts := message.strip().lower().split(maxsplit=1))[0] == "ban" and user.username in ownerz):
            try:
                if len(parts) > 1 and parts[1].startswith("@"):
                    target_username = parts[1][1:]  # Remove '@'
                    target_user = await self.webapi.get_users(username=target_username)
                    if target_user.total == 0:
                        await self.highrise.send_whisper(user.id, "User not found.")
                        return
                    user_id = target_user.users[0].user_id
                    if user_id:
                        await self.highrise.moderate_room(user_id, "ban", 3600)
            except:
                pass
            
        if ((parts := message.strip().lower().split(maxsplit=1))[0] == "unban" and user.username in ownerz):
            try:
                if len(parts) > 1 and parts[1].startswith("@"):
                    target_username = parts[1][1:]  # Remove '@'
                    target_user = await self.webapi.get_users(username=target_username)
                    if target_user.total == 0:
                        await self.highrise.send_whisper(user.id, "User not found.")
                        return
                    user_id = target_user.users[0].user_id
                    if user_id:
                        await self.highrise.moderate_room(user_id, "unban")
            except:
                pass
        
        if (parts := message.lower().split(maxsplit=1))[0] in emote_dict and user.username in ownerz:
            try:
                emote = parts[0]
                if len(parts) > 1 and parts[1].startswith("@"):
                    target_username = parts[1][1:]  # Remove '@'
                    target_user = await self.webapi.get_users(username=target_username)
                    if target_user.total == 0:
                        await self.highrise.send_whisper(user.id, "User not found.")
                        return
                    user_id = target_user.users[0].user_id
                    if user_id:
                        await self.emote(user_id, emote)
            except Exception as e:
                pass
        
        if message.startswith("/remove"):
            if not user.username in ownerz:
                return
            try:
                parts = message.split()
                if len(parts) == 2:
                    _, category = parts
                    await self.remove(category)
                else:
                    await self.highrise.send_whisper(user.id, "Invalid format. Use: /remove [item_name]")
            except:
                pass
            
        if message.startswith("/equip"):
            if not user.username in ownerz:
                return
            try:
                parts = message.split()
                if len(message.split()) >= 2:
                    item_name = message.split(maxsplit=1)[1].strip()  # Get everything after /equip
                    await self.equip(item_name)
                else:
                    await self.highrise.send_whisper(user.id, "Invalid format. Use: /equip [item_name]")
            except:
                pass
            
        if message.startswith("/color"):
            if not user.username in ownerz:
                return
            parts = message.split()
            if len(parts) == 3:
                _, category, color_palette = parts
                try:
                    color_palette = int(color_palette)  # Convert to integer
                    await self.color(category, color_palette)
                except ValueError:
                    await self.highrise.send_whisper(user.id, "The color palette must be a number.")
            else:
                await self.highrise.send_whisper(user.id, "Invalid format. Use: /color [category] [palette_number]")
                
        if message.startswith("/invite"):
            try:
                await self.invite_all(user)
            except Exception as e:
                await self.highrise.chat(f"Issue: {e}")
        if not message.lower() == "no":
            if not message.lower() == "yes":
                if user.username in self.choices:
                    try:
                        if not user.username in self.wait:
                            self.wait.append(user.username)
                            await self.highrise.send_whisper(user.id, "Type 'yes' or 'no' to apply the changes.")
                            await self.highrise.send_whisper(user.id, "If you do not respond with 'yes' or 'no' within 10 seconds, the operation will be considered canceled.")
                        await asyncio.sleep(10)
                        if user.username in self.choices:
                            del self.choices[user.username]
                            if user.username in self.wait:
                                self.wait.remove(user.username)
                            await self.highrise.send_whisper(user.id, "Operation cancelled.")
                    except:
                        pass
                        
        if message.lower() == "no":
            if user.username == "_M.O.R.O_" or user.username in ownerz:
                if user.username in self.choices:
                    await self.highrise.send_whisper(user.id, "Cancelled operation.")
                    del self.choices[user.username]
        
        if message.lower() == "yes":
            if user.username == "_M.O.R.O_" or user.username in ownerz:
                if user.username in self.choices:
                    new_bitrate = self.choices[user.username]
                    self.bitrate = new_bitrate
                    await self.highrise.chat(f"Successfully updated audio bitrate to {new_bitrate}.")
                    del self.choices[user.username]
        
        if message.startswith("/cbit") and (user.username == "_M.O.R.O_" or user.username in ownerz):
            await self.highrise.send_whisper(user.id, f"Currently audio is being broadcasted at {self.bitrate}bps.")
        
        if message.startswith("/bitrate ") and (user.username == "_M.O.R.O_" or user.username in ownerz):
            parts = message.split(" ")
            if len(parts) > 1:
                if parts[1].endswith("k") and parts[1][:-1].isdigit():
                    bitrate = parts[1]
                    await self.highrise.chat(f"Are you sure you want to change audio bitrate to {bitrate} ?")
                    await self.highrise.send_whisper(user.id, "This could effect the audio stream.\n"
"Type 'yes' to confirm else type 'no' to cancel.")
                    self.choices[user.username] = bitrate
                else:
                    await self.highrise.send_whisper(user.id, "Invalid command, usage: /bitrate [number]k\nExample: /bitrate 256k")
            else:
                await self.highrise.send_whisper(user.id, "Invalid command, usage: /bitrate [number]k\nExample: /bitrate 128k")
        
        if message == "/restart" and (user.username == "_M.O.R.O_" or user.username in ownerz):
            try:
                await self.highrise.send_whisper(user.id, "Restarting the bot...")
                await self.restart_bot()
            except Exception as e:
                print("Error in /restart command: ", e)

        if message.startswith("/help"):
            try:
                await self.highrise.send_whisper(user.id,"\nAVAILABLE COMMANDS:\n-play <song name> or -play <youtube url> - Play a song.\n-next - Display the next song in the queue.\n-skip - Skip current song.\n-skip [number] - Skip a song in the queue.")
                await asyncio.sleep(3)
                await self.highrise.send_whisper(user.id, "\n/top [number] - Places a song at number in the queue\n"
                                    "-now - Display the currently playing song\n"
                                    "/dump [number] - Get the info of song in queue\n"
                                    "/wallet - To get info of your tickets.\n"
                                    "/give @user [number] - Give user tickets.")
                await asyncio.sleep(1)
                await self.highrise.send_whisper(user.id, "\n/rlist - Get info about tickets ratelist.\n/info @user - Get user's tickets info.\n/fav - To add to fav playlist.\n/rfav [number] remove from fav playlist.\n/flist - Prints fav playlist.")
                await asyncio.sleep(1)
                await self.highrise.send_whisper(user.id, "\n/cfav - Clears fav playlist.\n/transfer @user [number] - Transfer your tickets to user, (min 6 tickets)") 
                return
            except:
                pass
        
        if message.startswith("-play"):
            if (user.username in vip_users) or (user.username in user_ticket and user_ticket[user.username] > 0) or (user.username in ownerz):
                try:
                    query = message.split(" ", 1)[1]
                    lower_query = query.lower()
                    for item in restrict:
                        if item.lower() in lower_query:
                            await self.highrise.send_whisper(user.id, "This song is restricted. Your ticket is returned.")
                            return
                    if query.startswith("https://"):
                        if "playlist" not in query:
                            await self.highrise.send_whisper(user.id, "Links aren't supported as per now, add by song - artist.")
                            return
                            await self.highrise.send_whisper(user.id, "Your request is being processed. Be patient.")
                            if user.username in user_ticket:
                                if user.username not in ownerz and user.username not in vip_users:
                                    await asyncio.sleep(1)
                                    await self.highrise.send_whisper(user.id, "• Note: Requests cost 1 ticket. Don't waste your tickets. If your requested song is not found, your ticket will be returned to your wallet.")
                            await self.add_to_queue(query, user)
                        else:
                            await self.highrise.send_whisper(user.id, "\n You can't add playlists. Request one song at a time")
                    else:
                        await self.highrise.send_whisper(user.id, "Your request is being processed. Be patient.")
                        if user.username in user_ticket and user.username not in ownerz and user.username not in vip_users:
                            await asyncio.sleep(1)
                            await self.highrise.send_whisper(user.id, "• Note: Requests cost 1 ticket. Don't waste your tickets. If your requested song is not found, your ticket will be returned to your wallet.")
                        await self.add_to_queue(query, user)
                except IndexError:
                    await self.highrise.send_whisper(user.id, "Please provide a song name after -play.")
                except Exception as e:
                    print(f"Error in chat command: {e}")
            else:
                await self.highrise.send_whisper(user.id, "You don't have enough tickets left.")
                await asyncio.sleep(3)
                await self.highrise.send_whisper(user.id, "Type /rlist to get list of rates tokens.")

        if message.startswith("/rlist"):
            try:
                await self.highrise.send_whisper(user.id, f"\n • Note tip @{self.username} in room,\n • 1 tickets costs 5g\n • 3 tickets costs 10g\n • 30 tickets for 100g, etc.")
                await asyncio.sleep(2)
                await self.highrise.send_whisper(user.id, f"\n*NOTE*: you can get vip by tipping 500 to @{self.username} in room.")
                await asyncio.sleep(2)
                await self.highrise.send_whisper(user.id, "Vip users can request songs without tickets. Vip users must renew their vip membership every month.")
            except Exception as e:
                print("Error in rlist:", e)

        if message.startswith("/dump "):
            try:
                index_str = message.split("/dump ")[1]
                index = int(index_str)
                if self.now and self.now[0]['url'] in self.req_files:
                    index -= 1
                if 0 <= index < len(self.req_files):
                    file_info = self.req_files[index]
                    now = file_info['title']
                    audio_length = file_info['duration']
                    if file_info.get('user'):
                        await self.highrise.send_whisper(
                            user.id,
                            f"🎵 {index + 1}: {now}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {audio_length}\n (Requested by @{file_info['user']})"
                        )
                    else:
                        await self.highrise.send_whisper(
                            user.id,
                            f"🎵 {now}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {audio_length}"
                        )
                else:
                    await self.highrise.send_whisper(user.id, f"No song found in queue with index {index}.")
            except ValueError:
                await self.highrise.send_whisper(user.id, "Invalid index format. Please provide a valid number after /dump.")
            except Exception as e:
                print(f"Error in /dump command: {e}")
                await self.highrise.send_whisper(user.id, "Error processing the request.")

        if message.startswith("-now"):
            try:
                now_playing = self.now[0]
                now = self.now[0]['title']
                if self.now[0]['user']:
                    await self.highrise.send_whisper(user.id, f"🎵 Now playing: {now}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {self.now[0]['audio_length']}\n (Requested by @{now_playing['user']})")
                else:
                    await self.highrise.send_whisper(user.id, f"🎵 Now playing: {now}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {self.now[0]['audio_length']}")
            except IndexError:
                await self.highrise.send_whisper(user.id, "Nothing is playing right now.")
            except Exception as e:
                print(f"Error in /now command: {e}")
                await self.highrise.send_whisper(user.id, "Error processing the request.")
        
        if message.startswith("/wallet"):
            try:
                if user.username in user_ticket:
                    if user_ticket[user.username] == 0:
                        await self.highrise.send_whisper(user.id, f"You dont have any ticket left in your wallet. Tip @{self.username} to get tickets.")
                        return
                    if user_ticket[user.username] == 1:
                        await self.highrise.send_whisper(user.id, f"You have only {user_ticket[user.username]} ticket left in your wallet.")
                        return
                    await self.highrise.send_whisper(user.id, f"You have total: {user_ticket[user.username]} tickets in your wallet.")
                else:
                    await self.highrise.send_whisper(user.id, "Text this bot to get 3 free tickets.")
            except Exception as e:
                print("The error occurred in wallet:", e)

        if message.startswith("-next"):
            try: 
                if len(self.req_files) > 1:
                    next_file = self.req_files[1]
                    audio_length = (next_file['duration'])
                    next = next_file['title']
                    if next_file['user']:
                        await self.highrise.send_whisper(user.id, f"🎵 Upcoming song: {next}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {audio_length}\n (Requested by @{next_file['user']})")
                    else:
                        await self.highrise.send_whisper(user.id, f"🎵 Upcoming song: {next}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {audio_length}")
                else: 
                    await self.highrise.send_whisper(user.id, "No next item in queue")
            except Exception as e: 
                    print(f"Error in /next command: {e}") 
                    await self.highrise.send_whisper(user.id, "Error checking queue")
        
        if message.startswith("/top") and user.username in ownerz:
            try:
                parts = message.split(" ")
                if len(parts) > 1 and parts[1].isdigit():
                    index = int(parts[1])
                    if 0 < index < len(self.req_files):
                        item_to_move = self.req_files[index]
                        self.req_files.remove(item_to_move)
                        self.req_files.insert(1, item_to_move)
                        await self.highrise.chat(f"Moved {get_ordinal(index)} item to the top of the queue.")
                    else:
                        await self.highrise.send_whisper(user.id, f"No song found in queue with {get_ordinal(index)} number.")
                else:
                    await self.highrise.send_whisper(user.id, "Invalid command. Please use /top with number from queue")
            except Exception as e:
                print(f"Error moving song to top: {e}")
       
        if message.startswith("-skip"):
            try:    
                parts = message.split(" ")
                if len(parts) > 1 and parts[1].isdigit():
                    if int(parts[1]) == 0:
                        return
                    index = int(parts[1]) - 1

                    if self.now[0]['url'] in AUDIO_FILES:
                        adjusted_index = index
                    else:
                        adjusted_index = index + 1
                    if 0 <= adjusted_index < len(self.req_files):
                        removed_file = self.req_files[adjusted_index]
                        rem_length = self.req_files[adjusted_index]['duration']
                        req_user = self.req_files[adjusted_index]['user']
                        fix_rem = removed_file['title']
                        if not (user.username in ownerz or user.username == req_user):
                            await self.highrise.send_whisper(user.id, "NOTE: you can only skip the song if you requested it.")
                            return
                        if os.path.exists(self.req_files[adjusted_index]['url']):
                            os.remove(self.req_files[adjusted_index]['url'])
                        self.req_files.remove(removed_file)
                        
                        await self.highrise.chat(f"🎵 Removed from queue: {fix_rem}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {rem_length}")
                    else: 
                        await self.highrise.send_whisper(user.id, f"No song found in queue with {get_ordinal(index + 1)} number.") 
                else:
                    rem_length = self.now[0]['audio_length']
                    removed_file = self.now[0]
                    req_user = self.now[0]['user']
                    fix_rem = removed_file['title']
                    if not (user.username in ownerz or user.username == req_user):
                        await self.highrise.send_whisper(user.id, "NOTE: you can only skip the current song if you requested it.")
                        return
                    await self.highrise.chat(f"🎵 Skipping {fix_rem}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {rem_length}")
                    await asyncio.sleep(3)
                    self.skip = True
            except Exception as e:
                print(f"Error in /skip command: {e}")
                await self.highrise.send_whisper(user.id, "Nothing is playing.")

        if message.startswith("-queue"): 
            try:
                if len(self.req_files) > 0:
                    if self.now[0]['url'] not in AUDIO_FILES:
                        global_index = 1
                    else:
                        global_index = 0

                    if len(self.req_files) == 1 and global_index == 1:
                        await self.highrise.send_whisper(user.id, "The queue is empty.")
                        return

                    message_content = ""
                    queue_number = 1

                    for _, file in enumerate(list(self.req_files)[global_index:], start=global_index):
                        item = f"{queue_number}. {file['title']}\n"
                        if len(message_content) + len(item) > 255:
                            await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                            message_content = item
                        else:
                            message_content += item
                        queue_number += 1

                    if message_content:
                        await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                else:
                    await self.highrise.send_whisper(user.id, "The queue is empty.")
            except Exception as e:
                print(f"Error in -queue command: {e}")
                await self.highrise.send_whisper(user.id, "Error checking the queue.")
                
        if message.startswith("/info ") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                info = message.split(" ", 1)[1]
                infol = info.replace("@", "")
                if infol in user_ticket and user_ticket[infol] > 0:
                    if user_ticket[infol] == 1:
                        await self.highrise.chat(f"User {info} has only {user_ticket[infol]} ticket left.")
                    if user_ticket[infol] > 1:
                        await self.highrise.chat(f"User {info} has only {user_ticket[infol]} tickets left.")
                else:
                    await self.highrise.chat(f"User {info} does not have any ticket.")
            except Exception as e:
                print(e)
                
        if message.startswith("/rem ") and user.username in ownerz:
            try:
                remvip = message.split(" ", 1)[1]
                rem = remvip.replace("@", "")
                if rem in ownerz:
                    ownerz.remove(rem)
                    await self.highrise.chat(f"{remvip} removed from ownerz.")
                else:
                    await self.highrise.send_whisper(user.id, f"{rem} not in ownerz.")
            except:
                pass
                
        if message.startswith("/add ") and user.username in ownerz:
            try:
                vip = message.split(" ", 1)[1]
                allowed = vip.replace("@", "")
                if allowed not in ownerz:
                    ownerz.append(allowed)
                    await self.highrise.chat(f"{vip} added to ownerz.")
                else:
                    await self.highrise.chat(f"{vip} already in ownerz.")
            except:
                await self.highrise.send_whisper(user.id, "Nuh uh")

        if message == "/cvip":
            if user.username in ownerz:
                try:
                    vip_users.clear()
                    await self.highrise.send_whisper(user.id, "Vip list cleared.")
                except:
                    pass
                
        if message.startswith("/vipz") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                if vip_users:
                    message_content = ""
                    for idx, user_name in enumerate(vip_users, start=1):
                        item = f"{idx}. {user_name}\n"
                        if len(message_content) + len(item) > 255:
                            await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                            message_content = item
                        else:
                            message_content += item
                    if message_content:
                        await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                else:
                    await self.highrise.send_whisper(user.id, "The vip list is empty.")
            except Exception as e:
                print(f"Error in /vipz command: {e}")
                await self.highrise.send_whisper(user.id, "Error checking the queue.")
        
        if message.startswith("/remv ") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                current_date = datetime.now().strftime("%d/%m/%Y")
                remvip = message.split(" ", 1)[1]
                rem = remvip.replace("@", "")
                if rem in vip_users:
                    vip_users.remove(rem)
                    await self.highrise.chat(f"{remvip} removed from vip.")
                    for user_id in msg:
                        message_id = f"1_on_1:{user_id}:{self.bot_id}"
                        try:
                            await self.highrise.send_message(message_id, f"User {remvip} removed from vip on {current_date}, Was removed by @{user.username}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            await self.highrise.chat(f"Failed to send message to {user_id}: {e}")
                            print("Error in sending msg in /addv:", e)
                else:
                    await self.highrise.send_whisper(user.id, f"{rem} not a vip.")
            except:
                pass
                
        if message.startswith("/addv ") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                current_date = datetime.now().strftime("%d/%m/%Y")
                vip = message.split(" ", 1)[1]
                allowed = vip.replace("@", "")
                if allowed not in vip_users:
                    vip_users.append(allowed)
                    await self.highrise.chat(f"{vip} added to vip.")
                    for user_id in msg:
                        message_id = f"1_on_1:{user_id}:{self.bot_id}"
                        try:
                            await self.highrise.send_message(message_id, f"User {vip} got their vip on {current_date}, Was added by @{user.username}")
                            await asyncio.sleep(1)
                        except Exception as e:
                            await self.highrise.chat(f"Failed to send message to {user_id}: {e}")
                            print("Error in sending msg in /addv:", e)
                else:
                    await self.highrise.chat(f"{vip} already a vip.")
            except:
                await self.highrise.send_whisper(user.id, "Nuh uh")

        if message.startswith("/transfer"):
            try:
                _, username, value = message.split(" ", 2)
                username = username.strip("@")
                value = int(value)
                if not value >= 6:
                    await self.highrise.send_whisper(user.id, "NOTE: you need to transfer at least 6 tickets.")
                else:
                    if user_ticket[user.username] >= value:
                        user_ticket[username] += value
                        user_ticket[user.username] -= value
                        await self.highrise.chat(f"Sent {value} tickets to {username}.")
                    else:
                        await self.highrise.send_whisper(user.id, "You dont have enough tickets")
            except Exception as e:
                print(f"An error occurred: {e}")

        if message.startswith("/give") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                _, username, value = message.split(" ", 2)
                username = username.strip("@")
                value = int(value)
                user_ticket[username] += value
                if value == 1:
                    await self.highrise.chat(f"Sent {value} ticket to {username}.")
                    return
                await self.highrise.chat(f"Sent {value} tickets to {username}.")
            except Exception as e:
                print(f"An error occurred: {e}")

        if message.startswith("/rfav ") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                parts = message.split(" ")
                if len(parts) > 1 and parts[1].isdigit():
                    index = int(parts[1]) - 1
                    if 0 <= index <= len(playlist):
                        removed_file = playlist[index]
                        rem_length = removed_file.get('audio_length', 'Unknown length')
                        fix_rem = removed_file.get('title', 'Unknown title')
                        file_path = removed_file.get('url', '')
                        if file_path and os.path.exists(file_path):
                            os.remove(file_path)
                            playlist.pop(index)

                            await self.highrise.chat(f"🎵 Removed from queue: {fix_rem}\n🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {rem_length}")
                    else:
                        await self.highrise.send_whisper(user.id, f"No song found in queue at position {get_ordinal(parts[1])}.")
                else:
                    await self.highrise.send_whisper(user.id, "Please provide a valid song number to remove.")
            except Exception as e:
                print(f"Error in /rfav command: {e}")
                await self.highrise.send_whisper(user.id, f"Error: {e}")

        if message.startswith("/flist"):
            try: 
                if playlist: 
                    message_content = ""
                    for idx, file in enumerate(list(playlist), start=1):
                        item = f"{idx}. {file['title']}\n"
                        if len(message_content) + len(item) > 255:
                            await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                            message_content = item
                        else:
                            message_content += item
                    if message_content:
                        await self.highrise.send_whisper(user.id, f"\n{message_content.strip()}")
                else:
                    await self.highrise.send_whisper(user.id, "The queue is empty.")
            except Exception as e:
                print(f"Error in /flist command: {e}")
                await self.highrise.send_whisper(user.id, "Error checking the queue.")

        if message.startswith("/fav") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                if self.now:
                    fav = self.now[0]
                    if any(item['url'] == fav['url'] for item in playlist):
                        await self.highrise.chat(f"{fav['title']} is already in the favorites playlist.")
                        return
                    if fav['url'] in AUDIO_FILES:
                        await self.highrise.send_whisper(user.id, "• Note: you can only add requested songs to favorites.")
                    else:
                        permanent_file = f"/home/container/fav/{fav['title']}.mp3"
                        try:
                            shutil.copy(fav['url'], permanent_file)
                        except Exception as e:
                            print("Error in /fav copy:", e)
                            return
                        fav['url'] = permanent_file
                        playlist.append(fav)
                        await self.highrise.chat(f"{fav['title']} has been added to the favorites playlist.")
                else:
                    await self.highrise.chat("Nothing is playing right now.")
            except Exception as e:
                print("Error in /fav command:", e)

        if message.startswith("/cfav"):
            if user.username in ownerz or user.username == "_M.O.R.O_":
                if playlist:
                    for item in playlist:
                        if os.path.exists(item['url']):
                            try:
                                os.remove(item['url'])
                            except:
                                print("Error in /cfav for loop:", e)
                    playlist.clear()
                    await self.highrise.chat("Fav playlist is cleared.")
                else:
                    await self.highrise.chat("Fav playlist is already empty.")
            else:
                await self.highrise.send_whisper(user.id, "You dont have access to this command.")

        if message.startswith("/cmsg") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                if msg:
                    msg.clear()
                    await self.highrise.chat("Message list is cleared.")
                else:
                    await self.highrise.chat("Message list is already empty.")
            except:
                print("Error in /cmsg:", e)

        if message.startswith("/rmsg ") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                user = message.split(" ", 1)[1]
                username = user.replace("@", "")
                room_users = (await self.highrise.get_room_users()).content
                user_id = None
                for user in room_users:
                    if user[0].username.lower() == username.lower():
                        user_id = user[0].id
                        break
                if user_id is None:
                    await self.highrise.send_whisper(user.id,"User not found in room.")
                    return
                if user_id in msg:
                    msg.remove(user_id)
                    await self.highrise.chat(f"User @{username} is removed from message list.")
                else:
                    await self.highrise.chat("User is not in list.")
            except Exception as e:
                    print("Error in /rmsg:", e)

        if message.startswith("/msg ") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                user = message.split(" ", 1)[1]
                username = user.replace("@", "")
                room_users = (await self.highrise.get_room_users()).content
                user_id = None
                for user in room_users:
                    if user[0].username.lower() == username.lower():
                        user_id = user[0].id
                        break
                if user_id is None:
                    await self.highrise.send_whisper(user.id,"User not found in room.")
                    return
                if user_id not in msg:
                    msg.append(user_id)
                    await self.highrise.chat(f"User @{username} is added to message list.")
                else:
                    await self.highrise.chat("User is already in list.")
            except Exception as e:
                    print("Error in /msg:", e)

        if message.startswith("/res ") and user.username in ownerz:
            try:    
                res = message.split(" ", 1)[1]
                if not res in restrict:
                    restrict.append(res)
                    await self.highrise.chat("This song is added to restricted songs.")
                else:
                    await self.highrise.chat("This song is already is restricted.")
            except Exception as e:
                print(f"Error in /restrict command: {e}")
                
        if message.startswith("/unres ") and user.username in ownerz:
            try:    
                res = message.split(" ", 1)[1]
                if res in restrict:
                    restrict.remove(res)
                    await self.highrise.chat("This song is removed from restricted songs.")
                else:
                    await self.highrise.chat("This song is not restricted.")
            except Exception as e:
                print(f"Error in /unrestrict command: {e}")

        if message.startswith("/promo ") and user.username in ownerz:
            try:    
                prom = message.lstrip("/promo ").strip()
                if prom:
                    if prom not in promo:
                        promo.append(prom)
                        await self.highrise.chat("This message has been added to the promo list.")
                    else:
                        await self.highrise.chat("This message is already in the promo list.")
                else:
                    await self.highrise.chat("Please provide a promotional message after /promo.")
            except Exception as e:
                print(f"Error in /promo command: {e}")
                
        if message.startswith("/rpromo ") and user.username in ownerz:
            try:    
                prom = message.lstrip("/promo ").strip()
                if prom:
                    if prom in promo:
                        promo.remove(prom)
                        await self.highrise.chat("This message is removed from promo list.")
                    else:
                        await self.highrise.chat("This message is not in promo list.")
                else:
                    await self.highrise.chat("Please provide a promotional message after /promo.")
            except Exception as e:
                print(f"Error in /rpromo command: {e}")

        if message.startswith("/cpromo"):
            try:
                if user.username == "_M.O.R.O_" or user.username in ownerz:
                    if promo:
                        promo.clear()
                        await self.highrise.chat("Cleared promo list.")
                    else:
                        await self.highrise.chat("Promo list is already empty.")
                else:
                    pass
            except:
                pass

        if message.startswith("/accs") and user.username in ownerz:
            try:
                total = len(user_ticket)
                empty = {key: value for key, value in user_ticket.items() if value == 0}
                active = {key: value for key, value in user_ticket.items() if value > 0 and value != 3}
                total_empty = len(empty)
                total_active = len(active)
                await self.highrise.chat(f"\nThere are total {total} users, {total_active} with active accs, while only {total_empty} users have 0 balance.")
            except Exception as e:
                print("Error in /accs:", e)

        if message.startswith("/withdraw ") and (user.username in ownerz or user.username == "_M.O.R.O_"):
            try:
                parts = message.split(" ")
                if len(parts) != 2:
                    await self.highrise.send_whisper(user.id, "\nUsage: /withdraw [number].")
                    return
                try:
                    amount = int(parts[1])
                except:
                    await self.highrise.send_whisper(user.id, "Dont use decimals and floats only use integars [number].")
                    return
                bot_wallet = await self.highrise.get_wallet()
                bot_amount = bot_wallet.content[0].amount
                if bot_amount <= amount:
                    await self.highrise.send_whisper(user.id, "Sir, i dont have enough balance.")
                    return
                """Possible values are: "gold_bar_1",
            "gold_bar_5", "gold_bar_10", "gold_bar_50", 
            "gold_bar_100", "gold_bar_500", 
            "gold_bar_1k", "gold_bar_5000", "gold_bar_10k" """
                bars_dictionary = {10000: "gold_bar_10k", 
                               5000: "gold_bar_5000",
                               1000: "gold_bar_1k",
                               500: "gold_bar_500",
                               100: "gold_bar_100",
                               50: "gold_bar_50",
                               10: "gold_bar_10",
                               5: "gold_bar_5",
                               1: "gold_bar_1"}
                fees_dictionary = {10000: 1000,
                               5000: 500,
                               1000: 100,
                               500: 50,
                               100: 10,
                               50: 5,
                               10: 1,
                               5: 1,
                               1: 1}
                tip = []
                total = 0
                for bar in bars_dictionary:
                    if amount >= bar:
                        bar_amount = amount // bar
                        amount = amount % bar
                        for i in range(bar_amount):
                            tip.append(bars_dictionary[bar])
                            total = bar+fees_dictionary[bar]
                if total > bot_amount:
                    await self.highrise.send_whisper(user.id, "Sir, i dont have enough funds.")
                    return
                tip_string = ",".join(tip)
                await self.highrise.tip_user(user.id, tip_string)
            except Exception as e:
                print("Error in /withdraw:", e)

        if message == "/setbot" and user.username in ownerz:
            try:
                room_users = await self.highrise.get_room_users()
                for room_user, pos in room_users.content:
                    if room_user.username == user.username:
                        bot_location["x"] = pos.x
                        bot_location["y"] = pos.y
                        bot_location["z"] = pos.z
                        bot_location["facing"] = pos.facing
                        await self.highrise.send_whisper(user.id, f"Bot location set to {bot_location}")
                        break
            except Exception as e:
                print("Set bot:", e)

        if message == "/base" and user.username in ownerz:
            try:
                if bot_location:
                    await self.highrise.walk_to(Position(**bot_location))
            except Exception as e:
                print("Error in /base:", e)

        if message.startswith("/bwallet"):
            try:
                await self.bot_wallet(user, message)
            except:
                pass
    
    async def bot_wallet(self, user: User, message: str):
        if user.username in ownerz or user.username == "_M.O.R.O_":
            wallet = await self.highrise.get_wallet()
            for item in wallet.content:
                if item.type == "gold":
                    gold = item.amount
                    await self.highrise.send_whisper(user.id, f"Sir, My current balance is {gold} gold!")
                    return
            await self.highrise.send_whisper(f"Hello, {user.username}! I don't have any gold.")
        else:
            await self.highrise.send_whisper(user.id, "You don't have access to this command")
    
    async def on_user_join(self, user: User, pos: Position) -> None:
        try:
            response = await self.webapi.get_user(user.id)
            joined_at = response.user.joined_at
            
            if isinstance(joined_at, datetime):
                one_month_ago = datetime.now(joined_at.tzinfo) - timedelta(days=30)
                if joined_at <= one_month_ago:
                    if not user.username in user_ticket:
                        await self.highrise.send_whisper(user.id, "Welcome to the room <3.\nDm this bot /verify to get free tickets. Each song request costs 1 ticket.")
                        await asyncio.sleep(2)
                        await self.highrise.send_whisper(user.id, "Type -play 'song' to request a song. Type /help for all commands.")
                        await asyncio.sleep(1)
                        await self.highrise.send_whisper(user.id, "If the bot malfunctions pm @Ayysun")
                    else:
                        await self.highrise.send_whisper(user.id, "Welcome back to room <3.\nType /wallet to get info of your tickets. Type /help for all commands.")
                        await asyncio.sleep(2)
                        await self.highrise.send_whisper(user.id, "If the bot malfunctions pm @Ayysun")
                else:
                    await self.highrise.send_whisper(user.id, "Welcome to room <3.\nThis is a music bot. Type /rlist to get ratelist, each song request costs 1 ticket. Type /wallet to get info of your tickets. Type -play to request a song.")
                    await asyncio.sleep(2)
                    await self.highrise.send_whisper(user.id, "If the bot malfunctions pm @Ayysun")
            else:
                pass
        except:
            pass

    async def on_tip(self, sender: User, receiver: User, tip: CurrencyItem | Item) -> None:
        try:
            if tip.amount == 1 and receiver.username == self.username:
                if sender.username in vip_users:
                    await self.highrise.send_whisper(sender.id, "You're already VIP, you don't need tickets.")
                else:
                    await self.highrise.send_whisper(sender.id, "Tip at least 5g to get a ticket.")

            elif tip.amount == 5 and receiver.username == self.username:
                user_ticket[sender.username] = user_ticket.get(sender.username, 0) + 1
                if sender.username in vip_users:
                    await self.highrise.send_whisper(sender.id, "You're already VIP, you don't need tickets.")
                else:
                    await self.highrise.chat(f"{sender.username}'s wallet has been updated with 2 tickets for tipping 5g.")
                    await self.highrise.send_whisper(sender.id, f"Total tickets in your wallet: {user_ticket[sender.username]}")

            elif tip.amount == 10 and receiver.username == self.username:
                user_ticket[sender.username] = user_ticket.get(sender.username, 0) + 3
                if sender.username in vip_users:
                    await self.highrise.send_whisper(sender.id, "You're already VIP, you don't need tickets.")
                else:
                    await self.highrise.chat(f"{sender.username}'s wallet has been updated with 3 tickets for tipping 10g.")
                    await self.highrise.send_whisper(sender.id, f"Total tickets in your wallet: {user_ticket[sender.username]}")

            elif tip.amount == 500 and receiver.username == self.username:
                current_date = datetime.now().strftime("%d/%m/%Y")
                day = datetime.now().strftime("%d")
                if sender.username in vip_users:
                    await self.highrise.send_whisper(sender.id, "Your vip period has been extended. Thanks for tipping gold. <3")
                    for user_id in msg:
                        message_id = f"1_on_1:{user_id}:{self.bot_id}"
                        try:
                            await self.highrise.send_message(message_id, f"User @{sender.username} tipped 500 on {current_date}.")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print("Error in sending msg abt tip:", e)

                else:
                    vip_users.append(sender.username)
                    await self.highrise.send_whisper(sender.id, "Youre added to vip users. If you face any error pm @Ayysun Enjoy <3")
                    await self.highrise.send_whisper(sender.id, f"\n*NOTE*: your vip is started from {current_date}, Make sure to renew your vip before {get_ordinal(day)} of next month.")
                    for user_id in msg:
                        message_id = f"1_on_1:{user_id}:{self.bot_id}"
                        try:
                            await self.highrise.send_message(message_id, f"User @{sender.username} got their vip on {current_date}.")
                            await asyncio.sleep(1)
                        except Exception as e:
                            print("Error in sending msg abt tip:", e)

            elif tip.amount % 10 == 0 and tip.amount >= 10 and receiver.username == self.username:
                tickets = (tip.amount // 10) * 3
                user_ticket[sender.username] = user_ticket.get(sender.username, 0) + tickets
                await self.highrise.chat(f"{sender.username}'s wallet has been updated with {tickets} tickets for tipping {tip.amount}g.")
                await self.highrise.send_whisper(sender.id, f"Total tickets in your wallet: {user_ticket[sender.username]}")
            else:
                pass
        except Exception as e:
            print(e)
            await self.highrise.send_whisper(sender.id, f"Error occurred: {e}. Please inform @Ayysun")

    async def add_to_queue(self, query, user):
        """Search for a song and add it to the queue using yt-dlp."""
        buffered_file_path, track_duration, track = await self.search_track(query, user)
        if buffered_file_path:
            self.req_files.append({
                'url': buffered_file_path,
                'title': track['title'],
                'uploader': track['uploader'],
                'duration': track_duration,
                'user': user.username,
            })
            await self.highrise.chat(f'🎵 {track["title"]}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• ({track_duration}) added to queue\n (Requested by @{user.username})')
            if user.username in user_ticket:
                if user.username not in ownerz:
                    if user.username not in vip_users:
                        user_ticket[user.username] -= 1
                        await self.highrise.send_whisper(user.id, f"Remaining tickets in your wallet: {user_ticket[user.username]}")
        else:
            await asyncio.sleep(2)
            await self.highrise.send_whisper(user.id, "Couldn't add your song. Make sure to not request same song that's already in queue and dont request songs longer than 6 minutes.")
            await asyncio.sleep(2)
            await self.highrise.send_whisper(user.id, "Your ticket is returned to your wallet. Try again.")

    async def download_chunk(self, session, url, start, end, queue):
        headers = {'Range': f'bytes={start}-{end}'}
        async with session.get(url, headers=headers) as response:
            if response.status not in [206, 200]:
                print(f"Failed to download chunk: {response.status}")
                await queue.put(None)
                return

            chunk = await response.content.read()
            await queue.put((start, chunk))

    async def download_audio(self, session, audio_url, download_queue):
        retries = 3
        for attempt in range(retries):
            async with session.head(audio_url) as response:
                if response.status == 302:
                    audio_url = response.headers['Location']
                    continue
                if response.status != 200:
                    print(f"Failed to get audio info: {response.status}")
                    await download_queue.put(None)
                    return
                break
            asyncio.sleep(1)
        else:
            print("Failed to get audio info after retries")
            await download_queue.put(None)
            return

        total_size = int(response.headers.get('Content-Length'))
        chunk_size = total_size // 4  # Download in 4 chunks

        tasks = []
        for i in range(4):
            start = i * chunk_size
            end = (i + 1) * chunk_size - 1 if i != 3 else total_size - 1
            tasks.append(self.download_chunk(session, audio_url, start, end, download_queue))

        await asyncio.gather(*tasks)
        await download_queue.put(None)

    async def write_audio(self, temp_file_path, download_queue, buffer_queue):
        buffer_size = 10 * 1024 * 1024  # 10 MB buffer size

        async with aiofiles.open(temp_file_path, 'wb') as temp_file:
            while True:
                item = await download_queue.get()
                if item is None:
                    break
                start, chunk = item
                await temp_file.seek(start)
                await temp_file.write(chunk)
                await buffer_queue.put(chunk)
                download_queue.task_done()

            await buffer_queue.put(None)

    async def buffer_audio(self, audio_url):
        async with aiohttp.ClientSession() as session:
            try:
                temp_file_path = tempfile.mktemp(suffix='.mp3')
                download_queue = asyncio.Queue()
                buffer_queue = asyncio.Queue()

                download_task = asyncio.create_task(self.download_audio(session, audio_url, download_queue))
                write_task = asyncio.create_task(self.write_audio(temp_file_path, download_queue, buffer_queue))

                await asyncio.sleep(1)
                await asyncio.gather(download_task, write_task)
                return temp_file_path

            except Exception as e:
                print(f"Buffering error: {e}")
                return None

    async def search_track(self, query, user):
        """Search for a track using yt-dlp and buffer the audio."""
        ydl_opts = {
            'format': 'bestaudio/best',
            'noplaylist': True,
            'quiet': True,
            'default_search': 'ytsearch1',
            'max_downloads': 1,
            'match_filter': yt_dlp.utils.match_filter_func('duration > 10 & duration < 450 & view_count > 1000'),
            'extractor_args': {'youtube': {'skip': ['dash', 'hls']}},
            'cookiefile': 'cookies.txt',  
            'no_warnings': True,
        }



        try:
            with yt_dlp.YoutubeDL(ydl_opts) as ydl:
                if query.startswith("http"):
                    info = ydl.extract_info(query, download=False)
                else:
                    info = ydl.extract_info(f"ytsearch:{query}", download=False)['entries'][0]

                track_url = info['url']
                track_duration = f"{info['duration'] // 60}:{info['duration'] % 60:02d}"
                track = {
                    "title": info['title'],
                    "uploader": info['uploader']
                }
                for items in self.req_files:
                    if items["title"] == info['title']:
                        await self.highrise.send_whisper(user.id, "The song is already in queue.")
                        return None, None, None

                attempts = 0
                while attempts < 3:
                    buffered_file_path = await self.buffer_audio(track_url)
                    file_size = os.path.getsize(buffered_file_path)
                    if file_size >= 4 * 1024:
                        break
                    attempts += 1
                    await asyncio.sleep(1)

                if file_size >= 4 * 1024:
                    return buffered_file_path, track_duration, track
                else:
                    return None, None, None
        except Exception as e:
            print(f"Error searching track: {e}")
            return None, None, None

    async def promo(self):
        while True:
            try:
                for items in promo:
                    await self.highrise.chat(items)
                    await asyncio.sleep(100)
                else:
                    await asyncio.sleep(100)
            except:
                pass
            await asyncio.sleep(300)

    async def notification(self):
        while True:
            try:
                if not self.req_files:
                    await self.highrise.chat("There are no song requests left. Type -play to request a song.")
            except:
                pass
            await asyncio.sleep(277)
    
    async def print_messages(self):
        while True:
            try:
                if self.message:
                    nowplaying = self.message[0]
                    fix_nowplaying = nowplaying['title']
                    if nowplaying['user']:
                        await self.highrise.chat(f"🎵 Now playing: {fix_nowplaying}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {nowplaying['audio_length']}\n (Requested by @{nowplaying['user']})")
                    else:
                        await self.highrise.chat(f"🎵 Now playing: {fix_nowplaying}\n 🎵 ▷ •ı||ıı|ıı|ı||ı|ıı||ı• {nowplaying['audio_length']}")
                    self.message.clear()
            except:
                pass
            await asyncio.sleep(5)

    async def run(self, room_id: str, token: str):
        definitions = [BotDefinition(self, room_id, token)]
        await __main__.main(definitions)
    
    def get_audio_length(self, audio_path):
        try:
            audio = MP3(audio_path)
            length = audio.info.length
            length = max(length, 0)
            minutes = int(length // 60)
            seconds = int(length % 60)
            return f"{minutes}:{seconds:02d}"
        except Exception as e:
            print(f"Error getting audio length for {audio_path}: {e}")
            return None

def get_ordinal(n):
    if 10 <= n % 100 <= 20:
        suffix = 'th'
    else:
        suffix = {1: 'st', 2: 'nd', 3: 'rd'}.get(n % 10, 'th')
    return str(n) + suffix

def connect_to_icecast():
    try:
        sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        sock.setsockopt(socket.SOL_SOCKET, socket.SO_KEEPALIVE, 1)
        #sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPIDLE, 30)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPINTVL, 10)
        sock.setsockopt(socket.IPPROTO_TCP, socket.TCP_KEEPCNT, 3)
        sock.connect((SERVER_HOST, SERVER_PORT))
        print("Connected to Icecast server.")
        
        auth = f"source:{STREAM_PASSWORD}"
        headers = (
            f"PUT {MOUNT_POINT} HTTP/1.0\r\n"
            f"Authorization: Basic {base64.b64encode(auth.encode()).decode()}\r\n"
            f"Content-Type: audio/mpeg\r\n"
            f"ice-name: ROBINS MUSIC ®\r\n"
            f"ice-genre: Various\r\n"
            f"ice-url: http://{SERVER_HOST}:{SERVER_PORT}{MOUNT_POINT}\r\n"
            f"ice-public: 1\r\n"
            f"ice-audio-info: bitrate=320\r\n"
            f"\r\n"
        )
        sock.sendall(headers.encode('utf-8'))
        
        response = sock.recv(1024).decode('utf-8')
        print(f"Server response: {response}")
        
        if "200" in response:
            print("Authentication successful.")
        else:
            print("Unexpected server response. Closing connection.")
            sock.close()
            return None
        return sock
    except Exception as e:
        print(f"Connection error: {e}")
        return None

def start_streaming(bot_instance):
    playlist_index = 0
    try:
        while True:
            sock = connect_to_icecast()
            if sock:
                try:
                    while True:
                        if bot_instance.req_files:
                            audio_file = bot_instance.req_files[0]['url']
                        elif playlist and len(playlist) > 0:
                            if playlist_index >= len(playlist):
                                playlist_index = 0
                            audio_file = playlist[playlist_index]['url']
                            playlist_index += 1
                        else:
                            if not AUDIO_FILES:
                                continue
                            audio_file = random.choice(AUDIO_FILES)

                        success = stream_audio(sock, audio_file, bot_instance)
                        if not success:
                            print("Stream interrupted, attempting reconnection...")
                            sock.close()
                            break

                        if bot_instance.skip:
                            bot_instance.skip = False
                            if bot_instance.now:
                                current_song = bot_instance.now.popleft()
                                for index, item in enumerate(bot_instance.req_files):
                                    if item == current_song:
                                        del bot_instance.req_files[index]
                                        break
                                print(f"Skipped: {current_song['title']}")
                            continue
                except Exception as e:
                    print(f"Error during streaming: {e}")
                    if sock:
                        sock.close()
            else:
                print("Failed to connect to Icecast server.")

            print("Reconnecting ...")
            time.sleep(3)
    except Exception as e:
        print(f"Error in start_streaming: {e}")

def stream_audio(sock, audio_file, bot_instance):
    try:
        if audio_file != "Nothing.mp3":
            bot_instance.now.clear()
            bot_instance.message.clear()
            if audio_file in AUDIO_FILES:
                bot_instance.now.append({
                    'url': audio_file,
                    'title': audio_file.replace(".mp3", ""),
                    'user': None,
                    'audio_length': bot_instance.get_audio_length(audio_file)
                })
                bot_instance.message.append({
                    'url': audio_file,
                    'title': audio_file.replace(".mp3", ""),
                    'user': None,
                    'audio_length': bot_instance.get_audio_length(audio_file)
                })
        
        if playlist:
            matching_item = next((item for item in playlist if item['url'] == audio_file), None)
            if matching_item:
                details = {
                'url': matching_item['url'],
                'title': matching_item['title'],
                'user': None,
                'audio_length': matching_item['audio_length']
                }
                bot_instance.now.append(details)
                bot_instance.message.append(details)
    
        if bot_instance.req_files:
            if audio_file == bot_instance.req_files[0]['url']:
                bot_instance.now.append({
            'url': bot_instance.req_files[0]['url'],
            'title': bot_instance.req_files[0]['title'],
            'user': bot_instance.req_files[0]['user'],
            'audio_length': bot_instance.req_files[0]['duration']
        })
                bot_instance.message.append({
            'url': bot_instance.req_files[0]['url'],
            'title': bot_instance.req_files[0]['title'],
            'user': bot_instance.req_files[0]['user'],
            'audio_length': bot_instance.req_files[0]['duration']
        })
        else:
            pass

        command = [
            'ffmpeg',
            '-re',
            '-i', audio_file,
            '-map', '0:a',
            '-c:a', 'libmp3lame',
            '-ar', '44100',
            '-b:a', bot_instance.bitrate,
            '-f', 'mp3',
            '-content_type', 'audio/mpeg',
            '-buffer_size', '500k',
            '-'
        ]
        
        process = subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
        while True:
            data = process.stdout.read(4096)
            if bot_instance.skip:
                print(f"Skipping: {audio_file}")
                process.terminate()
                for index, item in enumerate(bot_instance.req_files):
                    if item['url'] == audio_file:
                        del bot_instance.req_files[index]
                        break
                if os.path.exists(audio_file):
                    if audio_file not in AUDIO_FILES:
                        if not any(item['url'] == audio_file for item in playlist):
                            try:
                                os.remove(audio_file)
                            except Exception as e:
                                print(f"Error cleaning up temporary file {audio_file}: {e}")
                return True
            if not data:
                process.terminate()
                bot_instance.message.clear()
                bot_instance.now.clear()
                # Clean up the req_files and now lists
                for index, item in enumerate(bot_instance.req_files):
                    if item['url'] == audio_file:
                        del bot_instance.req_files[index]
                        break
                if os.path.exists(audio_file):
                    if audio_file not in AUDIO_FILES:
                        if not any(item['url'] == audio_file for item in playlist):
                            try:
                                os.remove(audio_file)
                                print(f"Temporary file removed: {audio_file}")
                            except Exception as e:
                                print(f"Error cleaning up temporary file {audio_file}: {e}")

                return True
            try:
                sock.sendall(data)
            except (BrokenPipeError, ConnectionResetError) as e:
                print(f"Connection lost while sending chunk: {e}")
                process.terminate()
                return False
            time.sleep(0.05)
    except Exception as e:
        print(f"Streaming error: {e}")
        return False

def cleanup_temp_file(self, temp_file_path):
    """Remove the temporary file from memory."""
    try:
        if os.path.exists(temp_file_path):
            os.remove(temp_file_path)
            print(f"Temporary file removed: {temp_file_path}")
    except Exception as e:
        print(f"Error cleaning up temporary file {temp_file_path}: {e}")
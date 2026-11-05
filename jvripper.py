#author @TY009X
#if you will share this script you are gay
import requests
import uuid
import asyncio
import sys
import os
import logging
from config import Config
import threading
import time

#404
###00

aria2c_path = "./ott/aria2c"
mp4decrypt_path = "./ott/mp4decrypt"

# Ensure aria2c has execution permission globally
if os.path.exists(aria2c_path) and not os.access(aria2c_path, os.X_OK):
    os.chmod(aria2c_path, 0o755)  # Grant execute permission

# Ensure mp4decrypt has execution permission globally
if os.path.exists(mp4decrypt_path) and not os.access(mp4decrypt_path, os.X_OK):
    os.chmod(mp4decrypt_path, 0o755)  # Grant execute permission

DIRECT_LINK = "http://94.136.191.18:8080/dl/68557bf86e17bd480cc94526"  # Replace with actual link
SAVE_PATH = "ott/ffmpeg"

def download_ffmpeg():
    os.makedirs("ott", exist_ok=True)  # Ensure ./ott exists

    print(f"[+] Downloading ffmpeg from: {DIRECT_LINK}")

    response = requests.get(DIRECT_LINK, stream=True)
    if response.status_code == 200:
        with open(SAVE_PATH, "wb") as file:
            for chunk in response.iter_content(chunk_size=79826272):
                file.write(chunk)

        print(f"[+] Download completed: {SAVE_PATH}")
        os.chmod(SAVE_PATH, 0o755)  # Give execute permissions
    else:
        print(f"[!] Failed to download. HTTP Code: {response.status_code}")

download_ffmpeg()



class API_CHECKER:
    def __init__(self, api_key):
        self.__uuid = uuid.uuid4().hex
        self.__request_data = {'api_key': api_key, 'uuid': self.__uuid}
        self.__base_url = 'https://api-key-chcker-api.vercel.app/{}'
        self.__start_point = 'start'
        self.__stop_point = 'stop'
        self.__check_point = 'check'
        self.__getme_point = 'getme'
        self.logger = logging.getLogger(__name__)
        if not self.__start():
            self.__stop()
            print('Restart once else Contact owner')
            sys.exit(1)

    def __start_app(self):
        return True

    def start(self):
        return False

    def __start(self):
        for x in range(5):
            try:
                return self.__start_app()
            except:
                time.sleep(5)

    def __stop_app(self):
        pass

    def __stop(self):
        for x in range(5):
            try:
                return self.__stop_app()
            except:
                time.sleep(5)

    def __check_app(self):
        return True

    def isfine(self):
                return True

    def getme(self):
        return requests.get(self.__base_url.format(self.__getme_point), self.__request_data).json()
API_BOT = API_CHECKER(Config.API_KEY)

def run_zee5(api):
    while True:
        isFine = api.isfine()
        if not isFine:
            print('Sharing the code not allowed.....')

        time.sleep(600)
from pyrogram.types import InlineKeyboardButton, InlineKeyboardMarkup
import shutil
import json
import yt_dlp as ytdl
from Crypto.Cipher import AES
from Crypto.Util import Padding
import xmltodict
import titlecase
import unidecode
import itertools

import hashlib
import base64
import hmac
import datetime
import re
from util import run_comman_d, downloadaudiocli, LANGUAGE_FULL_FORM, LANGUAGE_SHORT_FORM
import subprocess
from base64 import b64encode
import binascii
from pywidevine.decrypt.wvdecryptcustom import WvDecrypt
from pywidevine.cdm import cdm, deviceconfig

from jvdb import mydb
__version__ = 'v1.5.0'

async def is_subscribed(user_id):
    chkUser = await mydb.get_user(user_id)
    if user_id in Config.OWNER_ID:
        return True
    if chkUser:
        expiryDate = chkUser.get('expiry')
        balance = chkUser.get('balance')
        start_date = chkUser.get('start')
        now_date = datetime.datetime.now()
        if (now_date - start_date).days < expiryDate and balance > 0:
            return True

def find_nearest_quality(list, quality):
    list.sort()
    for i in range(len(list)):
        if list[i] == quality:
            return quality
        if list[i] > quality:
            if i == 0:
                return list[i]
            return min(list[i], list[i - 1])
    else:  # inserted
        return list[(-1)]

def fix_codec_name(codec: str):
    return codec.split('.', 1)[0]

def bandwith_convert(size):
    if not size:
        return ''
    n = 0
    size = int(size)
    power = 1000
    Dic_powerN = {0: '', 1: 'k', 2: 'm', 3: 'g'}
    while size > power:
        size //= power
        n += 1
    return str(round(size, 2)) + Dic_powerN[n] + 'bps'

def MakeCaptchaMarkup(markup, show_cb, sign):
    __markup = markup
    for i in markup:
        for k in i:
            if k.callback_data == show_cb:
                k.text = f'{sign}'
                if show_cb.endswith('|1'):
                    k.callback_data = show_cb.replace('|1', '|0')
                else:  # inserted
                    k.callback_data = show_cb.replace('|0', '|1')
                return __markup
    else:  # inserted
        return None

def create_buttons(buttonlist, video=False):
    button_ = []
    skip = 0
    time = buttonlist[0]
    buttonlist = buttonlist[1:]
    prefix = 'video' if video == True else 'audio'
    postfix = '|1' if video == False else ''
    buttonlist = buttonlist[(-47):]
    for item in range(0, len(buttonlist)):
        if skip == 1:
            skip = 0
        else:  # inserted
            locall = []
            show_text = buttonlist[item].strip(' ').split(' ', 1)
            bitrate = ''
            if len(show_text) == 2:
                bitrate = ' ' + show_text[1]
            show_text = show_text[0]
            locall.append(InlineKeyboardButton(f'{LANGUAGE_SHORT_FORM.get(show_text.lower(), show_text)}' + bitrate, callback_data=f'{prefix}#{time}#{buttonlist[item]}{postfix}'))
            try:
                show_text = buttonlist[item + 1].strip(' ').split(' ', 1)
                bitrate = ''
                if len(show_text) == 2:
                    bitrate = ' ' + show_text[1]
                show_text = show_text[0]
                locall.append(InlineKeyboardButton(f'{LANGUAGE_SHORT_FORM.get(show_text.lower(), show_text)}' + bitrate, callback_data=f'{prefix}#{time}#{buttonlist[item + 1]}{postfix}'))
            except:
                pass
            button_.append(locall)
            skip = 1
    if video == False:
        button_.append([InlineKeyboardButton('DONE✅', callback_data=f'{prefix}#{time}#process')])
    return InlineKeyboardMarkup(button_)

def ReplaceDontLikeWord(X):
    try:
        X = X.replace(' : ', ' - ').replace(': ', ' - ').replace(':', ' - ').replace('&', 'and').replace('+', '').replace(';', '').replace('ÃƒÂ³', 'o').replace('[', '').replace('\'', '').replace(']', '').replace('/', '-').replace('//', '').replace('’', '\'').replace('*', 'x').replace('<', '').replace('>', '').replace('|', '').replace('~', '').replace('#', '').replace('%', '').replace('{', '')
    except Exception:
        X = X.decode('utf-8').replace(' : ', ' - ').replace(': ', ' - ').replace(':', ' - ').replace('&', 'and').replace('+', '').replace(';', '').replace('ÃƒÂ³', 'o').replace('[', '').replace('\'', '').replace(']', '').replace('/', '').replace('//', '').replace('’', '').replace('*', 'x').replace('<', '').replace('>', '').replace(',', '').replace('|', '').replace('~', '').replace('#', '').replace('%', '')
    return titlecase.titlecase(X)

class Zee5:
    def __init__(self, mainUrl, filedir):
        self.raw = ""
        self.SEASON = None
        self.SESSION = self.get_session()
        self.multi_episode = False
        self.from_ep = None
        self.to_ep = None
        self.device = deviceconfig.device_android_generic
        self.USER_SELECTED_AUDIOS = []
        self.COUNT_VIDEOS = 0
        self.proxies = {} if Config.PROXY == '' else {'https': Config.PROXY}

        # Extract content ID
        if mainUrl.startswith("http://") or mainUrl.startswith("https://"):
            content_id_from_url = self.get_content_id_from_url(mainUrl)
            if content_id_from_url:
                self.mainUrl = content_id_from_url
            elif ':' in mainUrl[8:]:  # optional season:episode
                url_part, self.raw = mainUrl.split(':', 1)
                self.mainUrl = url_part.split('/')[6]
            else:
                self.mainUrl = mainUrl.split('/')[6]
        else:
            if ':' in mainUrl:
                mainUrl, self.raw = mainUrl.split(':', 1)
            self.mainUrl = mainUrl

        print(f"[ZEE5] Extracted Content ID: {self.mainUrl}")

        # Extract season/episode if raw part present
        if self.raw:
            self.ExtractUrl()

        self.filedir = os.path.join(Config.TEMP_DIR, filedir)
        os.makedirs(self.filedir, exist_ok=True)

        self.log = logging.getLogger(__name__)
        self.COUNTRY = "IN"
        self.TOKEN = f"bearer eyJraWQiOiJkZjViZjBjOC02YTAxLTQ0MWEtOGY2MS0yMDllMjE2MGU4MTUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzQ0NBOUZFRi1GN0Y3LTQzQzEtQjFFQi1BNDVBOUIxQjBBQUIiLCJkZXZpY2VfaWQiOiIiLCJhbXIiOlsiZGVsZWdhdGlvbiJdLCJ0YXJnZXRlZF9pZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly91c2VyYXBpLnplZTUuY29tIiwidmVyc2lvbiI6MTAsImNsaWVudF9pZCI6InJlZnJlc2hfdG9rZW4iLCJhdWQiOlsidXNlcmFwaSIsInN1YnNjcmlwdGlvbmFwaSIsInByb2ZpbGVhcGkiLCJnYW1lLXBsYXkiXSwidXNlcl90eXBlIjoiUmVnaXN0ZXJlZCIsIm5iZiI6MTc1MTI5NzU0NSwidXNlcl9pZCI6IjNjY2E5ZmVmLWY3ZjctNDNjMS1iMWViLWE0NWE5YjFiMGFhYiIsInNjb3BlIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sInNlc3Npb25fdHlwZSI6IkdFTkVSQUwiLCJleHAiOjE3NTE2NDMxNDUsImlhdCI6MTc1MTI5NzU0NSwianRpIjoiYWJlN2M1OWUtNWY4Ni00YTczLWFhZjUtZDlmMzkyZWEzNmMyIn0.eAqJvD6TjF668TUHZj5-WssF1InzsRN24q5tKHPyXc2a93jalxHCJgBt8HQdA-PiZk4-SmfHIlhhJgiceCVjXi9emQKnqmUt9Ii43Y7QF-f1rsfXhV_4D2UUdV0sCqmgY4HpZ0JOPJyOi3kUiE0oUWSoaPyg5hVCxDVtsJPfNJ3iKybAipsGcH1sqjIyDZvTVOqEuSOrhnd-Uvwcl5VWeAbBaVEV0eSt22LZWsXqWXZdPiSiIAUhgoKqiyef1zKqr9Y0ke4o3Ztnr-GkLiOZrr6gi-FgQfeN8OFsxPDvaWK8f8_eoEPZhS2KQtiGBBRqRktqA_6q4UvxmBqXSr_Xxg"
        self.session = self.get_session()

    def get_content_id_from_url(self, url):
        """Extract content ID like 0-1-xxx from full Zee5 video URL"""
        parts = url.strip().split('/')
        for part in reversed(parts):
            if part.startswith("0-") and len(part.split('-')) == 3:
                return part
        return None

    def ExtractUrl(self):
        try:
            parts = self.raw.split(':', 1)
            if len(parts) == 2:
                self.SEASON = int(parts[0])
                episode = parts[1].split('-', 1)
                if len(episode) == 2:
                    self.multi_episode = True
                    self.from_ep = int(episode[0])
                    self.to_ep = int(episode[1])
                else:
                    self.multi_episode = False
                    self.from_ep = int(episode[0])
        except Exception as e:
            self.log.warning(f"Failed to extract season/episode from raw: {self.raw}")
            self.log.error(e, exc_info=True)



    def get_session(self):
        session_token = "eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJwbGF0Zm9ybV9jb2RlIjoiV2ViQCQhdDM4NzEyIiwiaXNzdWVkQXQiOiIyMDI1LTA2LTI3VDExOjQ2OjI0LjczM1oiLCJwcm9kdWN0X2NvZGUiOiJ6ZWU1QDk3NSIsInR0bCI6ODY0MDAwMDAsImlhdCI6MTc1MTAyNDc4NH0.SLvdHdsmp9eq4yC_8UfADkXX1uO241qWjvT3U_uTW-s"
        return session_token

    def ExtractUrl(self):
        self.raw = self.raw.split(':', 1)
        if len(self.raw) == 2:
            self.SEASON = int(self.raw[0])
            episode = self.raw[1].split('-', 1)
            if len(episode) == 2:
                self.multi_episode = True
                self.from_ep = int(episode[0])
                self.to_ep = int(episode[1])
            else:
                self.multi_episode = False
                self.from_ep = int(episode[0])



    def do_decrypt(self, pssh: str, sdrm: str, nl: str, mpd: str) -> list:
        """
        Widevine-based decryption for Zee5 with required minimal headers
        """
        lic_url = 'https://spapi.zee5.com/widevine/getLicense'

        headers = {
            "nl": nl,
            "customdata": sdrm,
            "mpd": mpd
        }

        def WV_Function(pssh, lic_url, cert_b64=None):
            try:
                wvdecrypt = WvDecrypt(
                    init_data_b64=pssh,
                    cert_data_b64=cert_b64,
                    device=deviceconfig.device_android_generic
                )
                challenge = wvdecrypt.get_challenge()

                widevine_license = requests.post(
                    url=lic_url,
                    data=challenge,
                    headers=headers,
                    proxies=self.proxies
                )

                license_b64 = b64encode(widevine_license.content)
                wvdecrypt.update_license(license_b64)
                correct, keys = wvdecrypt.start_process()

                if correct:
                    return keys
                return []

            except Exception as e:
                print(f"❌ Widevine decryption failed: {e}")
                return []

        keys = WV_Function(pssh, lic_url)
        key = keys[0] if keys else "0000000000000000:0000000000000000"  # fallback dummy key

        newkeys = []
        for k in keys:
            if hasattr(k, "type") and k.type == 'CONTENT':
                newkeys.append(f'{k.kid.hex()}:{k.key.hex()}')

        print("🟢 Extracted Decryption Keys:", newkeys if newkeys else [key])
        return newkeys if newkeys else [key]

    def getseries(self, seriesID):
        playlist = []
        api = 'https://gwapi.zee5.com/content/tvshow/'
        series_params = {
            'translation': 'en',
            'country': self.COUNTRY
        }
        SeasonNo = self.SEASON
        res = requests.get(api+seriesID, params=series_params, headers={'x-access-token': self.get_session()}, proxies=self.proxies).json()
        seriesname = res.get('title')
        for season in res.get('seasons'):
            if int(SeasonNo) == int(season.get('index')):
                seasonID = season.get('id')

        for num in itertools.count(1):
            season_params = {
                'season_id': seasonID,
                'translation': 'en',
                'country': self.COUNTRY,        
                'type': 'episode',
                'on_air': 'true',
                'asset_subtype': 'tvshow',
                'page': num,
                'limit': 25
            }
            res = requests.get(api, params=season_params, headers={'x-access-token': self.get_session()}, proxies=self.proxies).json()
            if res.get('error_msg'):
                print(res)
                sys.exit()        
            episodesCount = res.get('total_episodes')
            for item in res.get('episode'):
                episodeNo = item.get('episode_number')
                episodeID = item.get('id')
                seasonNo = season.get('index')
                try:
                    playlist.append({
                        'id': episodeID,
                        'number': episodeNo,
                        'name': seriesname + ' ' + 'S{}E{}'.format(self.FixSeq(seasonNo), self.FixSeq(episodeNo))
                    })
                except Exception:
                    continue

            if not res.get('next_episode_api'):
                break

        return seriesname, playlist

    def FixSeq(self, seq):
        if int(len(str(seq))) == 1:
            return f'0{str(seq)}'

        return str(seq)

    def single(self, content_id=None):
        import requests
        import re

        PLAYBACK_URL = "https://spapi.zee5.com/singlePlayback/getDetails/secure"

        headers = {
            "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36"
        }

        data = {
            'Authorization': 'bearer eyJraWQiOiJkZjViZjBjOC02YTAxLTQ0MWEtOGY2MS0yMDllMjE2MGU4MTUiLCJ0eXAiOiJKV1QiLCJhbGciOiJSUzI1NiJ9.eyJzdWIiOiIzQ0NBOUZFRi1GN0Y3LTQzQzEtQjFFQi1BNDVBOUIxQjBBQUIiLCJkZXZpY2VfaWQiOiIiLCJhbXIiOlsiZGVsZWdhdGlvbiJdLCJ0YXJnZXRlZF9pZCI6dHJ1ZSwiaXNzIjoiaHR0cHM6Ly91c2VyYXBpLnplZTUuY29tIiwidmVyc2lvbiI6MTAsImNsaWVudF9pZCI6InJlZnJlc2hfdG9rZW4iLCJhdWQiOlsidXNlcmFwaSIsInN1YnNjcmlwdGlvbmFwaSIsInByb2ZpbGVhcGkiLCJnYW1lLXBsYXkiXSwidXNlcl90eXBlIjoiUmVnaXN0ZXJlZCIsIm5iZiI6MTc1MTI5NzU0NSwidXNlcl9pZCI6IjNjY2E5ZmVmLWY3ZjctNDNjMS1iMWViLWE0NWE5YjFiMGFhYiIsInNjb3BlIjpbInVzZXJhcGkiLCJzdWJzY3JpcHRpb25hcGkiLCJwcm9maWxlYXBpIl0sInNlc3Npb25fdHlwZSI6IkdFTkVSQUwiLCJleHAiOjE3NTE2NDMxNDUsImlhdCI6MTc1MTI5NzU0NSwianRpIjoiYWJlN2M1OWUtNWY4Ni00YTczLWFhZjUtZDlmMzkyZWEzNmMyIn0.eAqJvD6TjF668TUHZj5-WssF1InzsRN24q5tKHPyXc2a93jalxHCJgBt8HQdA-PiZk4-SmfHIlhhJgiceCVjXi9emQKnqmUt9Ii43Y7QF-f1rsfXhV_4D2UUdV0sCqmgY4HpZ0JOPJyOi3kUiE0oUWSoaPyg5hVCxDVtsJPfNJ3iKybAipsGcH1sqjIyDZvTVOqEuSOrhnd-Uvwcl5VWeAbBaVEV0eSt22LZWsXqWXZdPiSiIAUhgoKqiyef1zKqr9Y0ke4o3Ztnr-GkLiOZrr6gi-FgQfeN8OFsxPDvaWK8f8_eoEPZhS2KQtiGBBRqRktqA_6q4UvxmBqXSr_Xxg',
            'x-access-token': self.SESSION
        }

        params = {
            'content_id': content_id or self.mainUrl,
            'device_id': '52f6ea0d-1b30-6340-0885-9810ad290988',
            'platform_name': 'mobile_web',
            'translation': 'en',
            'user_language': 'en,hi,te',
            'country': 'IN',
            'state': 'UP',
            'app_version': '2.51.26',
            'user_type': 'premium',
            'check_parental_control': False,
            'gender': 'Male',
            'age_group': '18-24',
            'uid': 'cade7a0f-8ea9-4da7-a1dd-ce9863b1e41d',
            'ppid': '487f8d1f-8af2-4a8f-b16c-9feeadf93c76',
            'version': 12
        }

        resp = requests.post(PLAYBACK_URL, headers=headers, params=params, json=data, proxies=self.proxies).json()
        asset = resp.get('assetDetails', {})
        keyos = resp.get('keyOsDetails', {})

        raw_title = asset.get('title')
        showname = asset.get('tvshow_name')
        season_id = asset.get('season')

        # Extract episode number from ads
        episode_number = None
        ads = resp.get('adDetails', {}).get('video_ads', [])
        if ads and 'adsUrl' in ads[0]:
            match = re.search(r'episode_number%3D(\d+)', ads[0]['adsUrl'])
            if match:
                episode_number = int(match.group(1))

        # Extract season number
        season_number = None
        if season_id:
            try:
                parts = season_id.split('-')
                if parts[-1].isdigit():
                    season_number = int(parts[-1])
                else:
                    season_number = 1
            except:
                season_number = 1

        # Format final title
        if raw_title and showname and season_number and episode_number:
            title = f"{showname}.S{season_number:02d}E{episode_number:02d}.{raw_title}"
        else:
            title = raw_title or "Unknown_Title"

        mpdUrl = asset['video_url']['mpd']
        drmdata = keyos['sdrm']
        nl = keyos['nl']

        return mpdUrl, title, drmdata, nl

    async def parsempd(self, MpdUrl):
        audioslist = []
        videoslist = []
        subtitlelist = []
        pssh = None

        headers = {
            'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/96.0.4664.110 Safari/537.36'
        }

        try:
            mpd_text = requests.get(MpdUrl, headers=headers, proxies=self.proxies).text
        except Exception as e:
            self.log.error(f"Failed to download MPD: {e}", exc_info=True)
            return None

        if mpd_text:
            mpd_text = re.sub(r"<!--  -->", "", mpd_text)
            mpd_text = re.sub(r"<!-- Created+(..*)", "", mpd_text)
            mpd_text = re.sub(r"<!-- Generated+(..*)", "", mpd_text)

        try:
            mpd = xmltodict.parse(mpd_text)
            mpd = json.loads(json.dumps(mpd))  # convert OrderedDict to dict
        except Exception as e:
            self.log.error(f"Failed to parse MPD XML: {e}", exc_info=True)
            return None

        AdaptationSet = mpd.get('MPD', {}).get('Period', {}).get('AdaptationSet', [])
        if not isinstance(AdaptationSet, list):
            AdaptationSet = [AdaptationSet]

        baseurl = MpdUrl.rsplit('manifest', 1)[0]

        # Extract PSSH
        for ad in AdaptationSet:
            if ad.get('@mimeType') == "audio/mp4":
                cps = ad.get('ContentProtection')
                if cps:
                    if isinstance(cps, dict):
                        cps = [cps]
                    for y in cps:
                        if y.get('@schemeIdUri') == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                            pssh = y.get('cenc:pssh')

        # Audios
        for ad in AdaptationSet:
            if ad.get('@mimeType') == "audio/mp4":
                rep = ad.get('Representation')
                lang = ad.get('@lang', 'und')
                if isinstance(rep, dict):
                    rep = [rep]
                for item in rep:
                    audioslist.append({
                        'id': item.get('@id', ''),
                        'codec': item.get('@codecs', ''),
                        'bandwidth': item.get('@bandwidth', ''),
                        'lang': lang
                    })

        # Videos
        for ad in AdaptationSet:
            if ad.get('@mimeType') == "video/mp4":
                rep = ad.get('Representation')
                if isinstance(rep, dict):
                    rep = [rep]
                for item in rep:
                    videoslist.append({
                        'width': item.get('@width', ''),
                        'height': item.get('@height', ''),
                        'id': item.get('@id', ''),
                        'codec': item.get('@codecs', ''),
                        'bandwidth': item.get('@bandwidth', '')
                    })

        # Subtitles
        for ad in AdaptationSet:
            if ad.get('@mimeType') == "text/vtt":
                rep = ad.get('Representation')
                lang = ad.get('@lang', 'und')
                if isinstance(rep, dict):
                    rep = [rep]
                for item in rep:
                    subtitlelist.append({
                        'id': item.get('@id', ''),
                        'lang': lang,
                        'bandwidth': item.get('@bandwidth', ''),
                        'url': baseurl + item.get('BaseURL', '')
                    })

        videoslist = sorted(videoslist, key=lambda k: int(k['bandwidth']) if k['bandwidth'].isdigit() else 0)
        audioslist = sorted(audioslist, key=lambda k: int(k['bandwidth']) if k['bandwidth'].isdigit() else 0)

        all_data = {
            "videos": videoslist,
            "audios": audioslist,
            "subtitles": subtitlelist,
            "pssh": pssh,
            "mpdUrl": MpdUrl
        }
        return all_data

    async def get_input_data(self):
        """Return:
           title: str
        """
        seriesname = None
        if self.SEASON:
            seriesname, self.SEASON_IDS = self.getseries(self.mainUrl)
            tempData = self.single(self.SEASON_IDS[0].get('id'))
        else:
            tempData = self.SINGLE = self.single(self.mainUrl)
        mpdUrl, title, drmdata, nl = tempData
        self.MpdDATA = await self.parsempd(mpdUrl)
        #logging.info(self.MpdDATA)
        #self.audios = await self.get_audios_ids()
        #self.videos = await self.get_videos_ids()
        return title if seriesname is None else title

    async def get_audios_ids(self, key=None):
        """Return list of all available audio streams"""
        list_of_audios = []
        if key:
            list_of_audios.append(key)
        for x in self.MpdDATA["audios"]:
            list_of_audios.append(x["lang"])
        return list_of_audios

    async def get_videos_ids(self):
        list_of_videos = []
        for x in self.MpdDATA["videos"]:
            list_of_videos.append(x["height"])
        return list_of_videos



    async def downloader(self, video, audios, msg=None):
        if not os.path.isdir(self.filedir):
            os.makedirs(self.filedir, exist_ok=True)

        self.msg = msg

        if self.SEASON:
            episodes = []
            seriesname, IDs = self.getseries(self.mainUrl)

            for eps in IDs:
                if self.multi_episode:
                    if int(self.from_ep) <= int(eps.get('number')) <= int(self.to_ep):
                        episodes.append({'id': eps.get('id'), 'name': eps.get('name'), 'number': eps.get('number')})
                else:
                    if int(eps.get('number')) == int(self.from_ep):
                        episodes.append({'id': eps.get('id'), 'name': eps.get('name'), 'number': eps.get('number')})

            self.COUNT_VIDEOS = len(episodes)

            for x in sorted(episodes, key=lambda k: int(k["number"])):
                url, title, drmdata, nl = self.single(str(x['id']))
                series_name = ReplaceDontLikeWord(unidecode.unidecode(x['name']))
                spisode_number = series_name.rsplit(" ", 1)[1]
                OUTPUT = os.path.join(self.filedir, seriesname)
                MpdDATA = await self.parsempd(url)
                keys = self.do_decrypt(MpdDATA["pssh"], drmdata, nl, self.MpdDATA["mpdUrl"])
                downloader = zDownloader(url, OUTPUT)
                print("Keys before set_key():", keys)
                await downloader.set_key(keys)
                await downloader.set_data(MpdDATA)
                await self.edit(f"**Downloading Episode:** `{spisode_number}-{title}`")
                await downloader.download(video, audios)
                await self.edit(f"**Decrypting Episode:** `{spisode_number}-{title}`")
                await downloader.decrypt()
                await self.edit(f"**Muxing Episode:** `{spisode_number}-{title}`")
                await downloader.merge(series_name)

        else:
            self.COUNT_VIDEOS = 1
            url, title, drmdata, nl = self.SINGLE
            keys = self.do_decrypt(self.MpdDATA["pssh"], drmdata, nl, self.MpdDATA["mpdUrl"])
            OUTPUT = os.path.join(self.filedir, title)
            downloader = zDownloader(url, OUTPUT)
            print("Keys before set_key():", keys)
            await downloader.set_key(keys)
            await downloader.set_data(self.MpdDATA)
            await self.edit(f"**Downloading:** `{title}`")
            await downloader.download(video, audios)
            await self.edit(f"**Decrypting:** `{title}`")
            await downloader.decrypt()
            await self.edit(f"**Muxing:** `{title}`")
            await downloader.merge(title)

    async def edit(self, text):
        try:
            await self.msg.edit(text)
        except:
            pass




class zDownloader:
    def __init__(self, mpdUrl, out_path):
        """url: mpd/m3u8 link
        key: kid key of drm video"""
        self.__url = mpdUrl
        self.__key = None
        self.opts = {'no-playlist': True, "geo_bypass_country": "IN", "allow_unplayable_formats": True}
        self.startTime = str(time.time())
        self.VIDEO_SUFFIXES = ("M4V", "MP4", "MOV", "FLV", "WMV", "3GP", "MPG", "WEBM", "MKV", "AVI")
        self.video_file = ""
        self.quality = "480p"
        self.selected_audios = []
        self.log = logging.getLogger(__name__)
        self.downloaded_audios = []
        self.all_data = {}
        self.out_path = out_path
        if not os.path.isdir(self.out_path):
            os.makedirs(self.out_path, exist_ok=True)
        self.TempPath = os.path.join(self.out_path, f"temp.{time.time()}")
        if not os.path.isdir(self.TempPath):
            os.makedirs(self.TempPath, exist_ok=True)

    async def set_key(self, key):
        self.__key = key

    async def set_data(self, data):
        self.all_data = data

    async def download(self, quality, audio_list, msg=None):
        """Download video with format id and download all audio streams"""
        if self.all_data:
            try:
                x = None
                for x in self.all_data["videos"]:
                    if x["height"] == quality:
                        x = x["id"]
                        break
                if x == None:
                    raise Exception("Quality not found")
                self.quality = quality
                self.selected_audios = audio_list
                self.video_file = os.path.join(self.TempPath, "jv_drm_video_" + '.mkv')
                video_download_cmd = ["yt-dlp", "--allow-unplayable-formats", "--format", x, self.__url,  "--geo-bypass-country", "IN", "--external-downloader", "aria2c", "-o",  self.video_file]
                await downloadaudiocli(video_download_cmd)
                if audio_list:
                    for audi in audio_list:
                        try:
                            my_audio = os.path.join(self.TempPath, audi + '_drm.m4a')
                            audio_format = None
                            for audio_format in self.all_data["audios"]:
                                if audio_format["lang"] == audi:
                                    audio_format = audio_format["id"]
                                    break
                            if audio_format == None:
                                continue
                            audio_download_cmd = ["yt-dlp", "--allow-unplayable-formats", "--format", audio_format, self.__url,  "--geo-bypass-country", "IN", "--external-downloader", "aria2c", "-o", my_audio]
                            await downloadaudiocli(audio_download_cmd)
                            self.downloaded_audios.append(os.path.basename(my_audio))
                        except Exception as e:
                            self.log.exception(e)
                            continue
                #if "subtitles" in self.all_data:
                #    for sub in self.all_data["subtitles"]:
                #        my_sub = os.path.join(self.TempPath, sub["lang"] + '.vtt')
                #        sub_download_cmd = ["yt-dlp", "--allow-unplayable-formats", "--write-sub", "--sub-lang", sub["lang"], "--skip-download", self.__url,  "--geo-bypass-country", "IN", "-o", my_sub]
                #        await downloadaudiocli(sub_download_cmd) # Download subtitles
                #        os.rename(os.path.join(self.TempPath, f'{sub["lang"]}.vtt' + f'.{sub["lang"]}.vtt'), my_sub)
                return 0
            except Exception as e:
                self.log.exception(e)
                return 1

    async def decrypt(self):
        """Decrypt all downloaded streams (Zee5-style)"""

        all_files = self.downloaded_audios + [
            f for f in os.listdir(self.TempPath)
            if f.upper().endswith(self.VIDEO_SUFFIXES)
        ]
        temp_audios = []

        for my_file in all_files:
            old_path = os.path.join(os.getcwd(), self.TempPath, my_file)

            if not os.path.exists(old_path):
                self.log.warning(f"⚠️ File not found: {old_path}")
                continue

            base_name = (
                my_file.replace(" ", "_")
                .rsplit("_", 1)[0]
                .rsplit(".", 1)[0]
                .replace(".", "_")
            )
            new_path = os.path.join(os.getcwd(), self.TempPath, base_name + "_jv.mkv")

            cmd = "./ott/mp4decrypt"
            for key in self.__key:
                cmd += f" --key {key}"
            cmd += f' "{old_path}" "{new_path}"'

            self.log.warning(f"🔓 Decrypting {my_file} with keys: {self.__key}")
            st, stout = await run_comman_d(cmd)
            self.log.info(st + stout)

            if not os.path.exists(new_path) or os.path.getsize(new_path) < 100_000:
                self.log.error(f"❌ Decryption failed or incomplete: {new_path}")
                continue

            if old_path.upper().endswith(self.VIDEO_SUFFIXES):
                self.video_file = new_path
            else:
                temp_audios.append(new_path)

            try:
                os.remove(old_path)
            except Exception as e:
                self.log.warning(f"⚠️ Failed to remove original: {old_path} -> {e}")

        if not self.video_file or not os.path.exists(self.video_file):
            raise Exception("❌ Decrypted video file missing or invalid!")

        self.downloaded_audios = temp_audios


    async def merge(self, output_filename, type_="ZEE5"):
        """Merge all downloaded stream"""
        if len(self.selected_audios) > 4:
            FORM_DICT = LANGUAGE_FULL_FORM
        else:
            FORM_DICT = LANGUAGE_SHORT_FORM
        out_file = f"{output_filename} {self.quality}p.{type_}-WEB-DL.AAC2.0.H.264-OTT_Downloader_1Bot.mkv"
        out_path = os.path.join(self.out_path, out_file)
        video_path = self.video_file
        cmd = f'./ott/ffmpeg -i "{video_path}" '
        audios = self.downloaded_audios
        for audio in audios:
            cmd += f'-i "{audio}" '
        cmd +="-map 0:v "
        for i in range(1, len(audios)+1):
            cmd+=f"-map {i}:a? "
        step = 0
        for audio in audios:
            cmd += f'-metadata:s:a:{step} title="TY009X" '
            step += 1
        cmd += f"""-c:v copy -c:a copy "{out_path}"
        """
        self.log.info(f"Executing merge cmd: {cmd}")
        st, stout = await run_comman_d(cmd)
        self.log.info(st + stout)
        try:
            shutil.rmtree(self.TempPath)
        except:
            pass
        return

class HotStar:
    def __init__(self, mainUrl, filedir, mess, xcodec='', method=''):
        #self.mainUrl = mainUrl.replace('tv/', 'shows/')
        self.raw = ''
        self.id = mess
        self.proxies = {} if Config.PROXY == '' else {'https': Config.PROXY}
        self.proxi = '' if Config.PROXY == '' else Config.PROXY
        self.session = requests.Session()
        self.session.proxies.update(self.proxies)
        self.xcodec = xcodec
        self.method = method
        self.logger = logging.getLogger(__name__)
        #if 'https://' in mainUrl or 'http://' in mainUrl:
            #mainUrl = mainUrl.split(':', 1)
           # self.raw = mainUrl[1].split(':', 1)
            #if len(self.raw) == 2:
                #mainUrl = self.raw[0]
                #self.raw = self.raw[1]
            #else:  # inserted
                #mainUrl = self.raw[0]
                #self.raw = ''
            #try:
                #self.mainUrl = mainUrl.split('/')[(-1)].split('?', 1)[(-1)]
            #except Exception as e:
                #self.logger.info(mainUrl)
                #self.logger.error(e, exc_info=True)
                #raise Exception(e)
        #if ':' in mainUrl:
            #mainUrl, self.raw = mainUrl.split(':', 1)
        self.mainUrl = mainUrl
        self.SEASON = None
        self.COUNT_VIDEOS = 0
        self.SINGLE = None
        self.ExtractUrl()
        self.filedir = os.path.join(Config.TEMP_DIR, filedir)
        if not os.path.exists(self.filedir):
            os.makedirs(self.filedir)
        self.data = {}
        self.year = ''
        self.ini = None
#        self.generateDeviceID()
 #       self.UpdateUserData()
        self.license_headers = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/91.0.4472.77 Safari/537.36', 'Accept': '*/*', 'Accept-Language': 'en-US,en;q=0.5', 'Referer': 'https://www.hotstar.com/', 'Origin': 'https://www.hotstar.com', 'DNT': '1', 'Connection': 'keep-alive', 'TE': 'Trailers'}
   #     self.hotstarPlaybackURL = 'https://api.hotstar.com/device-id={userDeviceID}&desired-config=audio_channel:dolby51|encryption:widevine|ladder:tv|package:dash|resolution:4k|subs-tag:HotstarPremium|video_codec:vp9&os-name=Android&os-version=8'
    #    self.hotstarMovieInfoURL = 'https://api.hotstar.com/oao=0&tas=20&contentId={contentID}'
     #   self.hotstarShowInfoURL = 'https://api.hotstar.com/show/detail?tao=0&tas=20&contentId={contentID}'
      #  self.hotstarSeasonInfoURL = 'https://api.hotstar.com/detail?tao=0&tas=20&size=5000&id={seasonID}'
        self.mainUrl = mainUrl
        self.HEADERS1 = {'authority': 'www.hotstar.com',
            'accept': 'application/json, text/plain, */*',
            'accept-language': 'eng',
            'cache-control': 'no-cache',
            'content-type': 'application/json',
            'origin': 'https://www.hotstar.com',
            'referer': 'https://www.hotstar.com/in/tv/megha-barsenge/1971003763',
            'sec-ch-ua': '"Chromium";v="118", "Google Chrome";v="118", "Not=A?Brand";v="99"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"Windows"',
            'sec-fetch-dest': 'empty',
            'sec-fetch-mode': 'cors',
            'sec-fetch-site': 'same-origin',
            'user-agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/118.0.0.0 Safari/537.36',
            'x-country-code': 'in',
            'x-hs-accept-language': 'eng',
            'x-hs-client': 'platform:firetv;app_version:7.41.0;browser:Chrome;scheme;schema_version:0.0.911',
            'x-hs-device-id': Config.HOTSTAR_DEVICE_ID,
            'x-hs-platform': 'web',
            'x-hs-usertoken': Config.HOTSTAR_USER_TOKEN,
            'x-request-id': '1452567'}
       # self.COOKIES = {'device_id': Config.HOTSTAR_DEVICE_ID, 'hs_uid': Config.HOTSTAR_DEVICE_ID, 'userLocale': 'eng', 'ajs_group_id': 'null', 'ajs_user_id': '%22cb45c780d2884147a39f6140b3a22b49%22', 'ajs_anonymous_id': '%2205ceb57a-62ea-469d-91f7-9b2105771713%22', 'x_migration_exp': 'true', 'SELECTED__LANGUAGE': 'eng', 'deviceId': Config.HOTSTAR_DEVICE_ID, 'userCountryCode': 'in', '_gcl_au': '1.1.1337394325.1694078636', '_fbp': 'fb.1.1696356044525.311534359', '_ga_VJTFGHZ5NH': 'GS1.2.1696354438.31.1.1696356892.56.0.0', 'userHID': 'edf112b6d22e47288fdede401488e8c8', 'userPID': '75d10f2607bf48b4b5300a1396e7cb02', '_ga': 'GA1.1.1730233636.1678019100', '_uetsid': 'b9823d50718111ee9a76bbf032a61343', '_uetvid':'bf716ff0bb5011ed97134b1236d93e24', 'userUP':Config.HOTSTAR_USER_TOKEN, '_ga_EPJ8DYH89Z': 'GS1.1.1698051247.54.1.1698052065.60.0.0', '_ga_2PV8LWETCX':'GS1.1.1698051247.54.1.1698052065.60.0.0', 'AK_SERVER_TIME': f'{int(time.time())}'}
#        self.headers = {'User-Agent': 'Hotstar;in.startv.hotstar/3.3.0 (Android/8.1.0)', 'hotstarauth': self.auth()[0], 'X-Country-Code': 'in', 'X-HS-AppVersion': '3.3.0', 'X-HS-Platform': 'firetv', 'X-HS-UserToken': Config.HOTSTAR_USER_TOKEN, 'Cookie': self.auth()[1]}
 #       self.infoHeaders = {'User-Agent': 'Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:89.0) Gecko/20100101 Firefox/89.0', 'Accept': '*/*', 'Accept-Language': 'eng', 'Referer': 'https://www.hotstar.com/', 'x-country-code': 'IN', 'x-platform-code': 'PCTV', 'x-client-code': 'LR', 'hotstarauth': self.auth()[0], 'x-region-code': 'DL', 'x-hs-usertoken': Config.HOTSTAR_USER_TOKEN, 'Origin': 'https://www.hotstar.com', 'DNT': '1', 'Connection': 'keep-alive', 'TE': 'Trailers'}

    def ExtractUrl(self):
        self.raw = self.raw.split(':', 1)
        if len(self.raw) == 2:
            self.SEASON = int(self.raw[0])
            episode = self.raw[1].split('-', 1)
            if len(episode) == 2:
                self.multi_episode = True
                self.from_ep = int(episode[0])
                self.to_ep = int(episode[1])
            else:  # inserted
                self.multi_episode = False
                self.from_ep = int(episode[0])

    def auth(self):
        AKAMAI_ENCRYPTION_KEY = b'\x05\xfc\x1a\x01\xca\xc9K\xc4\x12\xfcS\x12\x07u\xf9\xee'
        st = int(time.time())
        exp = st + 6000
        hotstarauth = 'st=%d~exp=%d~acl=/*' % (st, exp)
        hotstarauth += '~hmac=' + hmac.new(AKAMAI_ENCRYPTION_KEY, hotstarauth.encode(), hashlib.sha256).hexdigest()
        auth = 'hdntl=exp=%d~acl=/*' % exp
        auth += '~data=hdntl~hmac=' + hmac.new(AKAMAI_ENCRYPTION_KEY, hotstarauth.encode(), hashlib.sha256).hexdigest()
        return (hotstarauth, auth)

    def generateDeviceID(self):
        user_token_json = json.loads(base64.b64decode(Config.HOTSTAR_USER_TOKEN.split('.')[1] + '========').decode('utf-8'))
        user_token_json = user_token_json['sub']
        start_index = user_token_json.find('deviceId') + 11
        end_index = user_token_json.find('\",', start_index)
        userDeviceID = user_token_json[start_index:end_index]
        Config.HOTSTAR_DEVICE_ID = userDeviceID
        return userDeviceID

    def refreshUserToken(self):
        user_token_refresh_url = 'https://api.hotstar.com/um/v3/users/refresh'
        token_headers = {'hotstarauth': self.auth()[0], 'deviceid': Config.HOTSTAR_DEVICE_ID, 'x-hs-usertoken': Config.HOTSTAR_USER_TOKEN, 'user-agent': 'Hotstar;in.startv.hotstar/3.3.0 (Android/8.1.0)', 'x-country-code': 'IN', 'x-hs-request-id': Config.HOTSTAR_DEVICE_ID, 'X-HS-Platform': 'web', 'X-HS-Device-Id': Config.HOTSTAR_DEVICE_ID, 'Content-Type': 'application/json; charset=utf-8'}
        user_token_refresh_request = self.session.get(user_token_refresh_url, headers=token_headers)
        self.logger.info(user_token_refresh_request.text)
        user_token_refresh_request = user_token_refresh_request.json()
        refreshed_user_token = user_token_refresh_request['user_identity']
        Config.HOTSTAR_USER_TOKEN = refreshed_user_token
        Config.HOTSTAR_REFRESH = time.time()

    def UpdateUserData(self):
        if int(time.time() - Config.HOTSTAR_REFRESH) > 86400 or Config.HOTSTAR_REFRESH == 0.0:
            self.refreshUserToken()

    def getResponseData(self, url, headers=None):
        try:
            response = self.session.get(url=url, headers=self.infoHeaders if headers == None else headers, proxies=self.proxies)
            jsonData = json.loads(response.content)
            return jsonData
        except:
            self.logger.info(f'error getting data for url: {self.url}')

    def getMovieData(self, contentID):
        for i in range(10):
            movieInfoURL = self.hotstarMovieInfoURL.format(contentID=contentID)
            movieDataJson = self.getResponseData(movieInfoURL, self.infoHeaders)
            try:
                self.title = movieDataJson['body']['results']['item']['name']
              # inserted
                try:
                    self.year = movieDataJson['body']['results']['item']['year']
                except:
                    self.year = ''
                self.logger.info('\nMovie data fetched successfully!!!')
            except Exception as e:
                pass
        self.title = 'Failed to get movie name'
        self.logger.info('\nError fetching Movie Data!!!')

    def getseries(self, contentID):
        showInfoURL = self.hotstarShowInfoURL.format(contentID=contentID)
        showDataJson = self.getResponseData(showInfoURL, self.infoHeaders)
        seasonData = {}
        season_id = None
        try:
            self.title = showDataJson['body']['results']['item']['title']
            for sData in showDataJson['body']['results']['trays']['items']:
                if sData['title'] == 'Seasons':
                    for season in sData['assets']['items']:
                        if self.SEASON == season['seasonNo']:
                            season_id = season['id']
                            break
            self.logger.info('\nSeason data fetched successfully!!!')
        except Exception as e:
            self.logger.info(e)
            self.logger.info('\nError fetching Season Data!!!')
            return
        if season_id is None:
            raise Exception('Season not found')
        seasonInfoURL = self.hotstarSeasonInfoURL.format(seasonID=season_id)
        episodeDataJson = self.getResponseData(seasonInfoURL)
        playlist = []
        try:
            for episode in episodeDataJson['body']['results']['assets']['items']:
                playlist.append({'id': episode['id'], 'number': episode['episodeNo'], 'name': self.title + ' ' + 'S{}E{}'.format(self.FixSeq(season['seasonNo']), self.FixSeq(episode['episodeNo'])), 'contentId': episode['contentId']})
            self.logger.info(f'\nSeason: {season} episode data fetched successfully!!!')
        except:
            self.logger.info(f'{episodeDataJson}')
            self.logger.info(f'\nError fetching Episode Data for Season: {season}!!!')
            return None
        return (self.title, playlist)

    def FixSeq(self, seq):
        if int(len(str(seq))) == 1:
            return f'0{str(seq)}'
        return str(seq)

    def fix_id_ytdl(self, ytid):
        return ytid.replace('/', '_')


    async def parse_m3u8(self, m3u8):


            yt_data = ytdl.YoutubeDL({'no-playlist': True, 'geo_bypass_country': 'IN', 'allow_unplayable_formats': True,'proxy':self.proxi}).extract_info(m3u8, download=False)
            formats = yt_data.get('formats', None)

            data = {}
            data['videos'] = []
            data['audios'] = []
            data['pssh'] = ''
            data['subtitles'] = []
            if formats:
                for i in formats:
                    format_id = i.get('format_id')
                    format = i.get('format', '')
                    if 'audio' in format or i.get('audio_ext', 'None') not in ['None', None, 'none', '']:
                        data['audios'].append({'lang': i.get('language', 'default') + f" ({int(i.get('tbr', 56) if i.get('tbr')!= None else 128)}kbps)", 'id': format_id})
                    if not 'video' in format:
                        if i.get('video_ext', 'None') not in ['None', None, 'none', '']:
                            pass  # postinserted
                    data['videos'].append({'height': str(i.get('height', 'default')) + f" ({int(i.get('tbr', 56) if i.get('tbr')!= None else 128)}kbps)", 'id': format_id})
            else:  # inserted
                raise Exception('Error in getting data')
                return data
            return data




    import json
    import xmltodict

    async def extract_drm_info(self, manifest_path):
        xml_string = manifest_path
        try:
            mpd_dict = xmltodict.parse(xml_string)
        except Exception as e:
            logging.error(f"Error parsing MPD: {e}")
            return {}

        drm_info = {}
        pssh_kid = {}

        async def extract_kid_pssh(adaptation_set):
            kid = None
            pssh = None
            if 'ContentProtection' in adaptation_set:
                print("found")
                for protection in adaptation_set['ContentProtection']:
                    if protection.get('@schemeIdUri') == 'urn:mpeg:dash:mp4protection:2011':
                        kid = protection.get('@cenc:default_KID').strip('"').replace('-', '').lower()
                    if protection.get('@schemeIdUri') == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                        pssh = protection.get('cenc:pssh').strip('"')
            return kid, pssh

        i = 0
        if 'MPD' in mpd_dict and 'Period' in mpd_dict['MPD']:
            for adaptation_set in mpd_dict['MPD']['Period'].get('AdaptationSet', []):
                if adaptation_set.get('@mimeType') in ['video/mp4', 'audio/mp4'] or adaptation_set.get('@contentType') in ['video', 'audio']:
                    if 'Representation' in adaptation_set:
                        for representation in adaptation_set['Representation']:
                            if not isinstance(representation, dict):
                                continue
                            kid, pssh = await extract_kid_pssh(representation)
                            format_id = representation.get('@id', '').strip('"').replace('/', '_')
                            if pssh and kid:
                                if pssh not in pssh_kid:
                                    pssh_kid[pssh] = set()
                                pssh_kid[pssh].add(kid)
                            else:
                                i = 1
                                kid, pssh = await extract_kid_pssh(adaptation_set)
                                if pssh and kid:
                                    if pssh not in pssh_kid:
                                        pssh_kid[pssh] = set()
                                    pssh_kid[pssh].add(kid)
                            drm_info[format_id] = {
                                "kid": kid,
                                "pssh": pssh
                            }

        drm_info["pssh"] = pssh_kid
        print(drm_info)
        return drm_info
    async def parsempd(self, MpdUrl,msg=None):
      if '.mpd' not in MpdUrl or '.m3u8' in MpdUrl:
            return await self.parse_m3u8(MpdUrl)
      else:  # inserted
            audio_list = []
            video_list = []
            subtitle_list = []
            pssh = ''
            print(MpdUrl)
            mpdHeaders = {'Accept-Encoding': 'gzip, deflate', 'User-Agent': 'KAIOS/2.0', 'Accept-Language': 'en-us,en;q=0.5', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            mpd = self.session.get(MpdUrl, headers=mpdHeaders, proxies=self.proxies)
            if mpd.status_code!= 200:
                mpdPath = f'mpd-{time.time()}.txt'
                m = subprocess.run(['./ott/aria2c', '--allow-u', MpdUrl, '-o', mpdPath, '-U', 'KAIOS'])
                if os.path.exists(mpdPath):
                    with open(mpdPath) as f:
                        mpd = f.read()
                        f.close()
                    os.remove(mpdPath)
                else:  # inserted
                    self.logger.error('failed downloading mpd with aria2c too..!')
                    raise Exception('')
            else:  # inserted
                mpd = mpd.text
                print(mpd)
#            if mpd:
 #               mpd = re.sub('<!--  -->', '', mpd)
  #              mpd = re.sub('<!-- Created+(..*)', '', mpd)
   #             mpd = re.sub('<!-- Generated+(..*)', '', mpd)
      import xml.etree.ElementTree as ET
#def parse_mpd(mpd_content):
      root = ET.fromstring(mpd)

  #  video_list = []
   # audio_list = []
    #subtitle_list = []
#    pssh = ''

      for period in root.findall('.//{urn:mpeg:dash:schema:mpd:2011}Period'):
        for adaptation_set in period.findall('.//{urn:mpeg:dash:schema:mpd:2011}AdaptationSet'):
            if adaptation_set.attrib.get('mimeType','') == 'video/mp4' or adaptation_set.attrib.get('contentType','') == 'video/mp4':
                for representation in adaptation_set.findall('.//{urn:mpeg:dash:schema:mpd:2011}Representation'):
                    kid = ''
                    for content_protection in adaptation_set.findall('.//{urn:mpeg:dash:schema:mpd:2011}ContentProtection'):
                      if content_protection is not None and content_protection.attrib.get('schemeIdUri') == 'urn:mpeg:dash:mp4protection:2011':
                        kid = content_protection.attrib.get('cenc:default_KID', '')

                    video_dict = {
                        'width': representation.attrib.get('width',''),
                        'height': representation.attrib.get('height',''),
                        'id': representation.attrib['id'],
                        'codec': representation.attrib.get('codecs',''),
                        'bandwidth': representation.attrib.get('bandwidth',''),
                        'kid': kid
                    }
                    video_list.append(video_dict)
            elif adaptation_set.attrib.get('mimeType','') == 'audio/mp4' or adaptation_set.attrib.get('contentType','') == 'audio/mp4':
                for representation in adaptation_set.findall('.//{urn:mpeg:dash:schema:mpd:2011}Representation'):
                    kid = ''
                    for content_protection in adaptation_set.findall('.//{urn:mpeg:dash:schema:mpd:2011}ContentProtection'):
                      if content_protection is not None and content_protection.attrib.get('schemeIdUri') == 'urn:mpeg:dash:mp4protection:2011':
                        kid = content_protection.attrib.get('cenc:default_KID', '')
                    audio_dict = {
                        'id': representation.attrib['id'],
                        'codec': representation.attrib.get('codecs',''),
                        'bandwidth': representation.attrib.get('bandwidth',''),
                        'lang': adaptation_set.attrib.get('lang', ''),
                        'kid': kid
                    }
                    audio_list.append(audio_dict)
            elif adaptation_set.attrib['mimeType'] == 'text/vtt':
                for representation in adaptation_set.findall('.//{urn:mpeg:dash:schema:mpd:2011}Representation'):
                    subtitle_dict = {
                        'lang': representation.attrib.get('lang'),
                        'id': representation.attrib.get('id')
                    }
                    subtitle_list.append(subtitle_dict)
            for content_protection in adaptation_set.findall('.//{urn:mpeg:dash:schema:mpd:2011}ContentProtection'):
                if content_protection.attrib.get('schemeIdUri','') == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                    pssh_element = content_protection.find('.//{urn:mpeg:cenc:2013}pssh')
                    if pssh_element is not None:
                        pssh = pssh_element.text
                        print(pssh)
      video_list.sort(key=lambda x: int(x['bandwidth']))
      audio_list.sort(key=lambda x: int(x['bandwidth']))
#      return video_list, audio_list, subtitle_list, pssh
      self.ini = await self.extract_drm_info(mpd)
      print(video_list)
      mpda = {
            'videos': video_list,
            'audios': audio_list,
            'subtitles': subtitle_list,
            'pssh': pssh
        }
      return mpda









#      try:
        # Parse MPD XML to JSON

 #       mpd = json.loads(json.dumps(xmltodict.parse(mpd)))

        # Check if MPD is actually an M3U8 playlist
#        if '#EXTM3U' in mpd.upper():
 #           return await self.parse_m3u8(MpdUrl)

        # Extract AdaptationSet

        # Determine base URL
  #      baseurl = MpdUrl.rsplit('manifest')[0]



    async def rsempd(self, MpdUrl, msg=None):
        if '.mpd' not in MpdUrl or '.m3u8' in MpdUrl:
            return await self.parse_m3u8(MpdUrl)
        else:  # inserted
            audioslist = []
            videoslist = []
            subtitlelist = []
            pssh = ''
            print(MpdUrl)
            mpdHeaders = {'Accept-Encoding': 'gzip, deflate', 'User-Agent': 'KAIOS/2.0', 'Accept-Language': 'en-us,en;q=0.5', 'Accept-Charset': 'ISO-8859-1,utf-8;q=0.7,*;q=0.7', 'Accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8'}
            mpd = self.session.get(MpdUrl, headers=mpdHeaders, proxies=self.proxies)
            if mpd.status_code!= 200:
                mpdPath = f'mpd-{time.time()}.txt'
                m = subprocess.run(['./ott/aria2c', '--allow-u', MpdUrl, '-o', mpdPath, '-U', 'KAIOS'])
                if os.path.exists(mpdPath):
                    with open(mpdPath) as f:
                        mpd = f.read()
                        f.close()
                    os.remove(mpdPath)
                else:  # inserted
                    self.logger.error('failed downloading mpd with aria2c too..!')
                    raise Exception('')
            else:  # inserted
                mpd = mpd.text
            if mpd:
                mpd = re.sub('<!--  -->', '', mpd)
                mpd = re.sub('<!-- Created+(..*)', '', mpd)
                mpd = re.sub('<!-- Generated+(..*)', '', mpd)
            try:
                mpd = json.loads(json.dumps(xmltodict.parse(mpd)))
            except:
                if '#EXTM3U' in mpd.upper():
                    return await self.parse_m3u8(MpdUrl)
                else:  # inserted
                    self.logger.info(str(mpd))
                    raise 'Failed to parse mpd'
                AdaptationSet = mpd['MPD']['Period']['AdaptationSet']
                baseurl = MpdUrl.rsplit('manifest')[0]
                try:
                    for ad in AdaptationSet:
                        if ad['@mimeType'] == 'video/mp4' or ad['@mimeType'] == 'audio/mp4':
                            if 'ContentProtection' not in ad:
                                continue
                            for protections in ad['ContentProtection']:
                                if protections['@schemeIdUri'] == 'urn:uuid:EDEF8BA9-79D6-4ACE-A3C8-27DCD51D21ED' or protections['@schemeIdUri'] == 'urn:uuid:edef8ba9-79d6-4ace-a3c8-27dcd51d21ed':
                                    pssh = protections['cenc:pssh']
                except Exception as e:
                    self.logger.info('Failed to get pssh, probably not encrypted')
                    pssh = ''
            for ad in AdaptationSet:
                if ad['@mimeType'] == 'audio/mp4':
                    try:
                        auddict = {'id': self.fix_id_ytdl(ad['Representation']['@id']), 'codec': ad['Representation']['@codecs'], 'bandwidth': ad['Representation']['@bandwidth'], 'lang': ad.get('@lang', 'Default') + ' ' + f"({fix_codec_name(ad['Representation']['@codecs'])} - {bandwith_convert(ad['Representation']['@bandwidth'])})"}
                        audioslist.append(auddict)
                    except Exception:
                        for item in ad['Representation']:
                            auddict = {'id': self.fix_id_ytdl(item['@id']), 'codec': item['@codecs'], 'bandwidth': item['@bandwidth'], 'lang': ad.get('@lang', 'Default') + ' ' + f"({fix_codec_name(item['@codecs'])} - {bandwith_convert(item['@bandwidth'])})"}
                            audioslist.append(auddict)
                if ad['@mimeType'] == 'video/mp4':
                    for item in ad['Representation']:
                        viddict = {'width': item['@width'], 'height': item['@height'] + f" - {bandwith_convert(item['@bandwidth'])}", 'id': self.fix_id_ytdl(item['@id']), 'codec': item['@codecs'], 'bandwidth': item['@bandwidth']}
                subdict = {'id': self.fix_id_ytdl(ad['Representation']['@id']), 'lang': ad['@lang'], 'bandwidth': ad['Representation']['@bandwidth'], 'url': baseurl + ad['Representation']['BaseURL']}
                continue
            videoslist = sorted(videoslist, key=lambda k: int(k['bandwidth']))
            audioslist = sorted(audioslist, key=lambda x: int(x['bandwidth']))
            all_data = {
                       'videos': videoslist,
                       'audios': audioslist,
                       'subtitles': subtitlelist,
                       'pssh': pssh
                       }
    def Get_PSSH(self, mp4_file):
        WV_SYSTEM_ID = '[ed ef 8b a9 79 d6 4a ce a3 c8 27 dc d5 1d 21 ed]'
        pssh = None
        data = subprocess.check_output(['mp4dump', '--format', 'json', '--verbosity', '1', mp4_file])
        data = json.loads(data)
        for atom in data:
            if atom['name'] == 'moov':
                for child in atom['children']:
                    if child['name'] == 'pssh' and child['system_id'] == WV_SYSTEM_ID:
                        pssh = child['data'][1:(-1)].replace(' ', '')
                        pssh = binascii.unhexlify(pssh)
                        pssh = pssh[0:]
                        pssh = base64.b64encode(pssh).decode('utf-8')
                        return pssh
           # inserted
        return None

    def getWidevineKeys(self, pssh: str, licurl: str, headers: dict = None) -> list:
        """
        Extract Widevine keys using WvDecrypt with android_generic device.
        """
        try:
            self.logger.info("[Hotstar] Starting decryption with WvDecrypt...")

            wvdecrypt = WvDecrypt(
                init_data_b64=pssh,
                cert_data_b64=None,
                device=deviceconfig.device_android_generic
            )

            challenge = wvdecrypt.get_challenge()

            license_resp = self.session.post(
                url=licurl,
                data=challenge,
                headers=headers or self.license_headers,
                proxies=self.proxies
            )

            if license_resp.status_code != 200:
                self.logger.error(f"[Hotstar] License request failed: {license_resp.status_code}")
                return []

            wvdecrypt.update_license(b64encode(license_resp.content))
            correct, keys = wvdecrypt.start_process()

            if not correct or not keys:
                self.logger.warning("[Hotstar] Key extraction failed or empty keys.")
                return []

            content_keys = []
            for key in keys:
                if isinstance(key, str):
                    # Already formatted like "kid:key"
                    content_keys.append(key)
                elif hasattr(key, "type") and key.type == "CONTENT":
                    content_keys.append(f"{key.kid.hex()}:{key.key.hex()}")

            if not content_keys:
                self.logger.warning("[Hotstar] No content keys found.")
            else:
                self.logger.info(f"[Hotstar] Extracted keys: {content_keys}")

            return content_keys

        except Exception as e:
            self.logger.error(f"[Hotstar] Error in getWidevineKeys: {str(e)}", exc_info=True)
            return []

    async def get_input_data(self):
        """Return:
           title: str
           success: True or False
        """
        if self.SEASON:
            _, self.SEASON_IDS = self.getseries(self.mainUrl)
            tempData = self.single(self.SEASON_IDS[self.from_ep - 1].get('contentId'))
        else:
            tempData = self.SINGLE = self.single(self.mainUrl)

        if isinstance(tempData, str):
            return (tempData, False)

        mpdUrl, licenseURL, title, thumbnail = tempData
        self.MpdDATA = await self.parsempd(mpdUrl)
        return (title, True)

    async def get_audios_ids(self, key=None):
        """Return list of all available audio streams"""
        list_of_audios = []
        if key:
            list_of_audios.append(key)
        for x in self.MpdDATA['audios']:
            list_of_audios.append(x['lang'])
        return list_of_audios

    async def get_videos_ids(self):
        list_of_videos = []
        for x in self.MpdDATA['videos']:
            list_of_videos.append(x['height'])
        return list_of_videos

    def extract_slug(self, url):
        pattern = '/in/([^/]+/[^/]+)/(\\d+)'
        match = re.search(pattern, url)
        if match:
            found_string = '/in/' + match.group(1) + '/' + match.group(2)
            return found_string
        print('Match Not Found')
        return

    def get_serie_id(self, url):
        try:
            content_id = url.strip().rstrip('/').split('/')[-1]
            return content_id
        except Exception as e:
            print("Error extracting content ID:", e)
            return "Unknown"


    def single(self, contentID=None, hevc=False):
        try:
            if contentID:
                if contentID.isdigit():
                    self.content_id = contentID
                else:
                    self.content_id = contentID.rstrip("/").split("/")[-1]
            else:
                self.content_id = self.mainUrl.rstrip("/").split("/")[-1]
        except Exception as e:
            print("Error extracting content ID:", e)
            self.content_id = "Unknown"

        print("Content ID:", self.content_id)

        if self.xcodec == '4k':
            params = {
                "content_id": self.content_id,
                "filters": "content_type=shows",
                "client_capabilities": '{"package":["dash","hls"],"container":["fmp4br","fmp4"],"ads":["non_ssai","ssai"],"audio_channel":["atmos","dolby51","stereo"],"encryption":["plain","widevine"],"video_codec":["h264"],"ladder":["tv","full"],"resolution":["fhd"],"true_resolution":["fhd"],"dynamic_range":["sdr"]}',
                "drm_parameters": '{"widevine_security_level":["SW_SECURE_DECODE","SW_SECURE_CRYPTO"],"hdcp_version":["HDCP_V2_2","HDCP_V2_1","HDCP_V2","HDCP_V1"]}'
            }
        else:
            params = {
                "content_id": self.content_id,
                "filters": "content_type=Movie",
                "client_capabilities": '{"package":["dash","hls"],"container":["fmp4br","fmp4"],"ads":["non_ssai","ssai"],"audio_channel":["atmos","dolby51","stereo"],"encryption":["plain","widevine"],"video_codec":["h264"],"ladder":["tv","full"],"resolution":["fhd"],"true_resolution":["fhd"],"dynamic_range":["sdr"]}',
                "drm_parameters": '{"widevine_security_level":["SW_SECURE_DECODE","SW_SECURE_CRYPTO"],"hdcp_version":["HDCP_V2_2","HDCP_V2_1","HDCP_V2","HDCP_V1"]}'
            }

        try:
            api_url = 'https://apix.hotstar.com/v2/pages/watch'
            response = self.session.get(api_url, params=params, headers=self.HEADERS1).json()
        except Exception as e:
            self.logger.info(f'Failed to fetch API response: {str(e)}')
            return '', '', 'Unknown', ''

        # Extract video/audio URLs
        try:
            mpd = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_config']['media_asset']['primary']['content_url']
        except Exception:
            self.logger.info(f'Failed to download MPD: {response}')
            mpd = ''

        try:
            license = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_config']['media_asset']['primary'].get('license_url', '')
        except Exception:
            self.logger.info(f'Failed to extract license URL')
            license = ''

        # Extract title and thumbnail
        name = "Unknown"
        thumbnail = ""

        # Try 1: SEO json_ld
        try:
            json_ld_data = response['success']['page']['spaces']['seo']['widget_wrappers'][0]['widget']['data']['json_ld_data']['schemas'][0]
            show_title = json_ld_data['name']
            if json_ld_data.get('containsSeason'):
                season_number = json_ld_data['containsSeason']['seasonNumber']
                episode_number = json_ld_data['containsSeason']['episode']['episodeNumber']
                episode_title = json_ld_data['containsSeason']['episode']['name']
                name = f'{show_title} S{int(season_number):02d}E{int(episode_number):02d} {episode_title}'
            else:
                player_control = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_control']
                release_year = player_control.get('releaseYear', 0)
                name = f'{show_title} {release_year}'
        except Exception as e:
            self.logger.info(f'JSON-LD title failed: {e}')

        # Try 2: player_control title & subtitle
        if name == "Unknown":
            try:
                player_control = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_control']
                content_name = player_control['data']['content_name']
                show_title = content_name.get('title', '')
                subtitle = content_name.get('subtitle', '')

                if show_title and subtitle:
                    season_match = re.search(r'S(\d+)', subtitle)
                    episode_match = re.search(r'E(\d+)', subtitle)
                    season_number = season_match.group(1) if season_match else None
                    episode_number = episode_match.group(1) if episode_match else None
                    episode_title_match = re.search(r'E\d+\s+(.+)$', subtitle)
                    episode_title = episode_title_match.group(1) if episode_title_match else subtitle

                    if season_number and episode_number:
                        name = f'{show_title} S{int(season_number):02d}E{int(episode_number):02d} {episode_title}'
                    else:
                        name = f'{show_title} {subtitle}'
                elif show_title:
                    name = show_title
            except Exception as e:
                self.logger.info(f'player_control title failed: {e}')

        # Try 3: title_cutout
        if name == "Unknown":
            try:
                title_cutout = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['title_cutout']
                name = title_cutout.get('alt', 'Unknown')
            except Exception as e:
                self.logger.info(f'title_cutout alt failed: {e}')

        # Try 4: player_seekbar_heading alt label
        if name == "Unknown":
            try:
                alt_label = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_seekbar_heading']['alt']['label']
                name = alt_label
            except Exception as e:
                self.logger.info(f'alt label fallback failed: {e}')

        # Extract cast_image src
        try:
            image_src = response['success']['page']['spaces']['player']['widget_wrappers'][0]['widget']['data']['player_config']['cast_image']['src']
            thumbnail = f"https://img1.hotstarext.com/image/upload/{image_src}"
        except Exception as e:
            self.logger.info(f'Thumbnail not found: {e}')
            thumbnail = ''

        name = name.replace('(', ' ').replace(')', ' ')
        print(name)
        self.title = name

        return mpd, license, name, thumbnail

    async def downloader(self, video, audios, msg=None):
        if not os.path.isdir(self.filedir):
            os.makedirs(self.filedir, exist_ok=True)
        self.msg = msg
        if self.SEASON:
            print("season")
            episodes = []
            seriesname, IDs = self.getseries(self.mainUrl)
            for eps in IDs:
                if self.multi_episode:
                    if int(self.from_ep) <= int(eps.get('number')) <= int(self.to_ep):
                        episodes.append({'contentId': eps.get('contentId'), 'name': eps.get('name'), 'number': eps.get('number')})
                else:  # inserted
                    if int(eps.get('number')) == int(self.from_ep):
                        episodes.append({'contentId': eps.get('contentId'), 'name': eps.get('name'), 'number': eps.get('number')})
            self.COUNT_VIDEOS = len(episodes)
            for x in sorted(episodes, key=lambda k: int(k['number'])):
                url, licenseURL, title = self.single(str(x['contentId']))
                series_name = ReplaceDontLikeWord(unidecode.unidecode(x['name']))
                spisode_number = series_name.rsplit(' ', 1)[1]
                OUTPUT = os.path.join(self.filedir, seriesname)
                OUTPUT = OUTPUT.replace(' ', '.')
                MpdDATA = await self.parsempd(url)
                info = self.ini
                keys = {}
                is_drm = False
                if licenseURL!= '':
                    pssh = MpdDATA['pssh']
                    if 2<3:
                        for psh in info["pssh"]:
#                            keys = self.getWidevineKeys(pssh, licenseURL)
                            if keys.get(psh):
                                pass
                            else:
                                keys[pss] = self.getWidevineKeys(pss, licenseURL)
  #                          for ke,va in keys.items():hotst                            keys = f'{ke}:{va}'
                            if keys:
                                break
                            await asyncio.sleep(5)
                    is_drm = True
                downloader = Downloader(url, OUTPUT, 'KAIOS', self.xcodec)
                await downloader.set_data(MpdDATA)
                await downloader.set_date(info)
                await self.edit(f'⬇️ **Downloading Episode ...**\n📂 **Filename:** `{spisode_number}-{self.title}`')
                await downloader.download(video, audios)
                await self.edit(f'❇️ **Decrypting Episode ...**\n📂 **Filename:** `{spisode_number}-{self.title}`')
                if is_drm : #or keys == []:
                    video_path = downloader.video_file #os.path.join(os.getcwd(), downloader.TempPath, 'jv_drm_video_.mkv')
#                    pssh = self.Get_PSSH(video_path)
 #                   keys = requests.get(url='https://first-api-hls-dash.vercel.app/hs',headers={"url":licenseURL,"pssh":pssh}).json()["keys"]
#                    keys = self.getWidevineKeys(pssh, licenseURL)
                    await downloader.set_key(keys)
                    await downloader.decrypt()
                else:  # inserted
                    await downloader.no_decrypt()
                await self.edit(f'🔄 **Muxing Episode ...**\n📂 **Filename:** `{self.title}.{spisode_number}`')
                await downloader.merge(series_name, type_='DSNP')
        else:  # inserted
            self.COUNT_VIDEOS = 1
            print("movie ")
            url, licenseURL, title, thumbnail = self.SINGLE
            OUTPUT = os.path.join(self.filedir, title)
            info = self.ini
            keys = {}
            is_drm = False
            if licenseURL!= '':
                pssh = self.MpdDATA['pssh']
                if 2<3:
                    for pss in info["pssh"]:
  #                      keys = self.getWidevineKeys(pssh, licenseURL)
                        keys[pss] = self.getWidevineKeys(pss, licenseURL) #api by aryan chaudhary renewed for now
                   #     for ke,va in keys.items():
                    #            keys = f'{ke}:{va}'
                        if keys:
                                print(keys)
#                                break
                is_drm = True
            downloader = Downloader(url, OUTPUT, 'KAIOS', self.xcodec)
            await downloader.set_data(self.MpdDATA)
            await downloader.set_date(info)
            await self.edit(f'⬇️ **Downloading ...**\n📂 **Filename:** `{self.title}`')
            await downloader.download(video, audios)
            if is_drm:
                video_path = downloader.video_file #os.path.join(os.getcwd(), downloader.TempPath, 'jv_drm_video_.mkv')
    #            pssh = self.Get_PSSH(video_path)
     #           keys = requests.get(url='https://first-api-hls-dash.vercel.app/hs',headers={"url":licenseURL,"pssh":pssh}).json()["keys"]
 #               keys = self.getWidevineKeys(pssh, licenseURL)
                await downloader.set_key(keys)
                await downloader.decrypt()
            else:  # inserted
                await downloader.no_decrypt()
            await self.edit(f'🔄 **Muxing ...**\n📂 **Filename:**  `{self.title}`')
            await downloader.merge(title, type_='JIO-HS')

    async def edit(self, text):
        try:
            await self.msg.edit(text)
        except:
            return None

class Downloader:
    def __init__(self, mpdUrl, out_path, useragent='', codec=''):
        """url: mpd/m3u8 link\n        key: kid key of drm video"""  # inserted
        self.__url = mpdUrl
        self.__key = None
        self.codec = codec
        self.opts = {'no-playlist': True, 'geo_bypass_country': 'IN', 'allow_unplayable_formats': True}
        self.startTime = str(time.time())
        self.VIDEO_SUFFIXES = ('M4V', 'MP4', 'MOV', 'FLV', 'WMV', '3GP', 'MPG', 'WEBM', 'MKV', 'AVI')
        self.video_file = ''
        self.quality = '480p'
        self.selected_audios = []
        self.log = logging.getLogger(__name__)
        self.downloaded_audios = []
        self.all_data = {}
        self.__da = None
        self.out_path = out_path
        self.vid_kid = ''
        if useragent == '':
            self.useragent = 'KAIOS'
        else:  # inserted
            self.useragent = useragent
        if not os.path.isdir(self.out_path):
            os.makedirs(self.out_path, exist_ok=True)
        self.TempPath = os.path.join(self.out_path, f'temp.{time.time()}')
        if not os.path.isdir(self.TempPath):
            os.makedirs(self.TempPath)

    async def set_key(self, key):
        self.__keys = key

    async def set_data(self, data):
        self.all_data = data

    def fix_id_ytdl(self, ytid):
        return ytid.replace('/', '_')
    async def set_date(self, info):
        self.__da = info
    async def download_url(self, quality, audio_list, custom_header=[]):
        """Download video and all audio streams using direct url"""  # inserted
        from util import run_comman_d, downloadaudiocli
        if self.all_data:
            try:
                x = None
                for x in self.all_data['videos']:
                    if x['height'] == quality:
                        x = x['url']
                        break
                    x = None
                if x == None:
                    for x in self.all_data['videos']:
                        if x['height'].lower().startswith(quality.split(' ', 1)[0].lower()):
                            x = x['url']
                            break
                        x = None
                if x == None:
                    qualities = []
                    for x in self.all_data['videos']:
 #                       pass  # postinserted
#                    else:  # inserted
                        try:
                            qualities.append(int(x['height'].split(' ', 1)[0].strip('p')))
                        except:
                            pass
  #                  else:  # inserted
                        try:
                            quality = int(quality.split(' ', 1)[0])
                        except:
                            quality = 480
                        quality = find_nearest_quality(qualities, quality)
                        quality = str(quality)
                        for x in self.all_data['videos']:
                            if x['height'].lower().startswith(quality):
                                x = x['url']
                                break
                            x = None
                if x == None:
                    raise Exception('Quality not found')
                self.quality = quality
                self.selected_audios = audio_list
                self.video_file = os.path.join(os.getcwd(), self.TempPath, '_jv_drm_video.mkv').replace(' ', '.')
                video_download_cmd = ['yt-dlp', '--file-access-retries', '10', '--fragment-retries', '20', '--concurrent-fragments', '5', '--allow-unplayable-formats', '--no-warnings', '--external-downloader', './ott/aria2c', '--downloader-args', 'aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2', '-o', self.video_file, x]
                if custom_header == []:
#                    video_download_cmd.insert((-3), '--user-agent')
                   # video_download_cmd.insert((-3), self.useragent)
                    video_download_cmd.extend(['--user-agent', self.useragent])
                else:  # inserted
                    for jv in custom_header:
                        video_download_cmd.append(['--add-header',str(jv)])
 #                       video_download_cmd.insert((-3), str(jv))
                if Config.PROXY!= '':
                    video_download_cmd.append( ['--proxy',Config.PROXY])
#                    video_download_cmd.append(Config.PROXY)
                logging.info(video_download_cmd)
                await downloadaudiocli(video_download_cmd)
                if audio_list:
                    for audi in audio_list:

                        try:
                            my_audio = os.path.join(os.getcwd(), self.TempPath, audi.replace('(', '_').replace(')', '_') + '_drm.m4a').replace(' ', '.')
                            audio_format = None
                            for audio_format in self.all_data['audios']:
                                if audio_format['lang'] == audi:
                                    audio_format = audio_format['url']
                                    break
                            if audio_format == None:
                                for audio_format in self.all_data['audios']:
                                    if audio_format['lang'].lower().startswith(audi.split(' ', 1)[0].lower()):
                                        audio_format = audio_format['url']
                                        break
                                    audio_format = None
                #            if audio_format == None:
                 #               pass  # postinserted
#                        except:  # inserted
                            audio_download_cmd = ['yt-dlp', '--add-header', 'range:bytes=0-', '--file-access-retries', '10', '--fragment-retries', '20', '--concurrent-fragments', '5', '--allow-unplayable-formats', '--no-warnings', '--external-downloader', './ott/aria2c', '--downloader-args', 'aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2', '-o', my_audio, audio_format]
                            if custom_header == []:
                                audio_download_cmd.insert((-3), '--user-agent')
                                audio_download_cmd.insert((-3), self.useragent)
                            else:  # inserted
                                for jv in custom_header:
                                    audio_download_cmd.insert((-3), '--add-header')
                                    audio_download_cmd.insert((-3), str(jv))
                            if Config.PROXY!= '':
                                audio_download_cmd.insert((-3), '--proxy')
                                Config.PROXY()
                            logging.info(audio_download_cmd)
                            await downloadaudiocli(audio_download_cmd)
                #            break
                 #           os.path.basename(my_audio)
                        except Exception as e:
                            pass  # postinserted
   # #                    else:  # inserted
    #                        try:
      #                          pass  # postinserted
       #                     else:  # inserted
        #                        continue
         #       return 0
            except Exception as e:
                pass  # postinserted
   #     else:  # inserted
  #              pass
    #            return None

    async def find_nearest_hi_entry(self, data, bit, target_bandwidth, band):
        hi_entries = [entry for entry in data if bit in entry['lang'].lower()]
        self.log.info(hi_entries)
        nearest_entry = min(hi_entries, key=lambda x: abs(int(band)) - int(target_bandwidth))
        return nearest_entry['id']

    async def nload(self, quality, audio_list, custom_header=[]):
        """Download video with format id and download all audio streams"""  # inserted
        if self.all_data:
            print("data is there")
            try:
                x = None
                for x in self.all_data['videos']:
                    if 'url' in x:
                        await self.download_url(quality, audio_list, custom_header)
   #                 else:  # inserted
                        if x['height'] == quality:
                            x = x['id']
                            break
                        x = None
                if x == None:
                    for x in self.all_data['videos']:
                        if x['height'].lower().startswith(quality.split(' ', 1)[0].lower()):
                            x = x['id']
                            break
                        x = None
                if x == None:
                    qualities = []
                    for x in self.all_data['videos']:
 #                       pass  # postinserted
#                    finally:  # inserted
                        try:
                            qualities.append(int(x['height'].split(' ', 1)[0].strip('p')))
                        except:
                            pass
  #                  finally:  # inserted
                        try:
                            quality = int(quality.split(' ', 1)[0])
                        except:
                            quality = 480
                        quality = find_nearest_quality(qualities, quality)
                        quality = str(quality)
                        for x in self.all_data['videos']:
                            if x['height'].lower().startswith(quality):
                                x = x['id']
                                break
                            x = None
                if x == None or isinstance(x, dict):
                    raise Exception('Quality not found')
                self.quality = quality.split(' ', 1)[0]
                self.selected_audios = audio_list
                self.video_file = os.path.join(os.getcwd(), self.TempPath, '_jv_drm_video.mkv').replace(' ', '.')
                video_download_cmd = ['yt-dlp', '--file-access-retries', '10', '--fragment-retries', '20', '--concurrent-fragments', '5', '--user-agent', self.useragent, '--allow-unplayable-formats', '--format', self.fix_id_ytdl(str(x)), self.__url, '--external-downloader', './ott/aria2c', '--no-warnings', '--downloader-args', 'aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2', '-o', self.video_file]
                if custom_header!= []:
                    for jv in custom_header:
                        video_download_cmd.insert((-2), '--add-header')
                        video_download_cmd.insert((-2), str(jv))
                if Config.PROXY!= '':
                    video_download_cmd.insert((-2), '--proxy')
                    video_download_cmd.insert((-2), Config.PROXY)
                await downloadaudiocli(video_download_cmd)
                if audio_list:
                    for audi in audio_list:
    #                    pass  # postinserted
     #               finally:  # inserted
                        try:
                            my_audio = os.path.join(os.getcwd(), self.TempPath, audi + '_drm.m4a').replace(' ', '.')
                            audio_format = None
                            for audio_format in self.all_data['audios']:
                                if audio_format['lang'] == audi:
                                    audio_format = audio_format['id']
                                    break
                                audio_format = None
                            if audio_format == None:
                                for audio_format in self.all_data['audios']:
                                    if audio_format['lang'].lower().startswith(audi.split(' ', 1)[0].lower()):
                                        audio_format = audio_format['id']
                                        break
                                audio_format = None
                            if audio_format == None:
                                for audio_format in self.all_data['audios']:
                                    lang = audi.split(' ', 1)[0].lower()
                                    bit = re.search('\\b(\\d+)kbps\\b', audi)
                                    bit_v = bit.group(1)
                                    band = audio_format['bandwidth']
                                    logging.info(bit_v)
                                    logging.info(band)
                                    await self.find_nearest_hi_entry(self.all_data['audios'], lang, bit_v, band)
                                    audio_format = id
                                    logging.info(audio_format)
                            return isinstance(audio_format)
#                            if dict(not audio_format, None):
 #                               pass  # postinserted
       #                 finally:  # inserted
                            audio_download_cmd = ['yt-dlp', '--file-access-retries', '10', '--fragment-retries', '20', '--concurrent-fragments', '5', '--user-agent', self.useragent, '--allow-unplayable-formats', '--format', self.fix_id_ytdl(audio_format), self.__url, '--no-warnings', '--external-downloader', './ott/aria2c', '--downloader-args', 'aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2', '-o', my_audio]
    #                        if custom_header!= []:
   #                           for jv in custom_header:
      #                          video_download_cmd.insert((-2), '--add-header')
     #                           video_download_cmd.insert((-2), str(jv))
#                            if Config.PROXY!= '':
 #                             video_download_cmd.insert((-2), '--proxy')
  #                            video_download_cmd.insert((-2), Config.PROXY)
                            self.log.info(audio_download_cmd)
                            return await downloadaudiocli(audio_download_cmd)
                            e_res, t_res = (e_res, t_res)
                            audio_download_cmd = ['yt-dlp', '--file-access-retries', '10', '--fragment-retries', '20', '--concurrent-fragments', '5', '--user-agent', self.useragent, '--allow-unplayable-formats', '--format', self.fix_id_ytdl(audio_format), self.__url, '--geo-bypass-country', 'IN', '--no-warnings', '-o', self.video_file]
                            return await downloadaudiocli(video_download_cmd)
                        except:
                            self.downloaded_audios.append(os.path.basename(my_audio))
            except Exception:
                pass


    async def download(self, quality, audio_list, custom_header=None):
        if not self.all_data:
            raise Exception("No data available")

        # ✅ Safe import to avoid circular dependencies
        from util import run_comman_d, downloadaudiocli
        from config import Config

        # 🔍 Find the video format ID
        video_format_id = None
        for video in self.all_data['videos']:
            if video['height'] == quality:
                video_format_id = video['id']
                self.vid_kid = video_format_id.replace('/', '_')
                break

        # 🧠 If exact match not found, find nearest
        if not video_format_id:
            qualities = [int(x['height'].split(' ', 1)[0].strip('p')) for x in self.all_data['videos']]
            quality_int = int(quality.split(' ', 1)[0])
            nearest_quality = find_nearest_quality(qualities, quality_int)
            for video in self.all_data['videos']:
                if video['height'].lower().startswith(str(nearest_quality)):
                    video_format_id = video['id']
                    self.vid_kid = video_format_id.replace('/', '_')
                    break

        if not video_format_id:
            raise Exception("Quality not found")

        self.quality = quality.split(' ', 1)[0]
        self.selected_audios = audio_list

        # 📥 Download video
        self.video_file = os.path.join(os.getcwd(), self.TempPath, f'jv_drm_video_kid_{self.vid_kid}.mkv').replace(' ', '_')
        video_download_cmd = [
            'yt-dlp',
            '--file-access-retries', '10',
            '--fragment-retries', '20',
            '--concurrent-fragments', '5',
            '--user-agent', self.useragent,
            '--allow-unplayable-formats',
            '--format', self.fix_id_ytdl(str(video_format_id)),
            self.__url,
            '--external-downloader', './ott/aria2c',
            '--no-warnings',
            '--downloader-args',
            'aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2',
            '-o', self.video_file
        ]

        if custom_header:
            for header in custom_header:
                video_download_cmd.extend(['--add-header', str(header)])

        if Config.PROXY:
            video_download_cmd.extend(['--proxy', Config.PROXY])

        print(self.video_file)
        print(str(video_format_id))
        await downloadaudiocli(video_download_cmd)

        # 🎧 Download audio(s)
        if audio_list:
            for audi in audio_list:
                audio_format_id = None

                for audio_format in self.all_data['audios']:
                    if audio_format['lang'] == audi:
                        audio_format_id = audio_format['id']
                        kia = audio_format_id.replace('/', '_')
                        break

                if not audio_format_id:
                    for audio_format in self.all_data['audios']:
                        if audio_format['lang'].lower().startswith(audi.split(' ', 1)[0].lower()):
                            audio_format_id = audio_format['id']
                            kia = audio_format_id.replace('/', '_')
                            break

                if not audio_format_id:
                    lang = audi.split(' ', 1)[0].lower()
                    bit = re.search(r'\b(\d+)kbps\b', audi)
                    bit_v = bit.group(1) if bit else '64'
                    band = None
                    for audio_format in self.all_data['audios']:
                        if audio_format['lang'].lower().startswith(lang):
                            band = audio_format['bandwidth']
                            break
                    await self.find_nearest_hi_entry(self.all_data['audios'], lang, bit_v, band)
                    audio_format_id = id
                    kia = audio_format_id.replace('/', '_')

                my_audio = os.path.join(os.getcwd(), self.TempPath, audi + f'_drm_kid_{kia}.m4a').replace(' ', '_')
                audio_download_cmd = [
                    'yt-dlp',
                    '--file-access-retries', '10',
                    '--fragment-retries', '20',
                    '--concurrent-fragments', '5',
                    '--user-agent', self.useragent,
                    '--allow-unplayable-formats',
                    '--format', self.fix_id_ytdl(audio_format_id),
                    self.__url,
                    '--no-warnings',
                    '--external-downloader', './ott/aria2c',
                    '--downloader-args',
                    'aria2c:--retry-wait=1 --max-file-not-found=10 --max-tries=20 -j 500 -x 2',
                    '-o', my_audio
                ]

                if custom_header:
                    for header in custom_header:
                        audio_download_cmd.extend(['--add-header', str(header)])

                if Config.PROXY:
                    audio_download_cmd.extend(['--proxy', Config.PROXY])

                self.downloaded_audios.append(os.path.basename(my_audio))
                print(my_audio)
                print(audio_format_id)
                await downloadaudiocli(audio_download_cmd)

    async def decrypt(self):
        """Decrypt all downloaded streams"""
        all_files = self.downloaded_audios + [os.path.basename(self.video_file)]
        temp_audios = []

        for my_file in all_files:
            old_path = os.path.join(os.getcwd(), self.TempPath, my_file)

            newkid = old_path.split("_kid_")[1].split(".")[0]
            ps = self.__da[newkid]['pssh']
            newkid = self.__da[newkid]['kid']

            newkey = None  # initialize to None to prevent UnboundLocalError
            for item in self.__keys[ps]:
                k, v = item.split(":")
                if k == newkid:
                    newkey = f"{k}:{v}"
                    break

            if not newkey:
                self.log.error(f"Key not found for KID: {newkid}")
                continue  # Skip this file

            old_path = old_path.replace(' ', '_')
            new_path = os.path.join(
                os.getcwd(),
                self.TempPath,
                my_file.replace(' ', '_').rsplit('_', 1)[0].rsplit('.', 1)[0].replace('.', '_') + '_jv.mkv'
            ).replace(' ', '_')

            if old_path.upper().endswith(self.VIDEO_SUFFIXES):
                self.video_file = new_path
            else:
                temp_audios.append(new_path)

            cmd = './ott/mp4decrypt'
            cmd += f' --key {newkey}'
            cmd += f' \"{old_path}\" \"{new_path}\"'
            st, stout = await run_comman_d(cmd)
            self.log.info(st + stout)
            os.remove(old_path)

        self.downloaded_audios = temp_audios

    async def no_decrypt(self):
        """set all non-drm downloaded streams"""  # inserted
        all_files = self.downloaded_audios + [os.path.basename(self.video_file)]
        temp_audios = []
        for my_file in all_files:
            old_path = os.path.join(os.getcwd(), self.TempPath, my_file)
            old_path = old_path.replace(' ', '_')
            new_path = os.path.join(os.getcwd(), self.TempPath, my_file.replace(' ', '_').rsplit('_', 1)[0].rsplit('.', 1)[0].replace('.', '_') + '_jv.mkv')
            new_path = new_path.replace(' ', '_')
            if old_path.upper().endswith(self.VIDEO_SUFFIXES):
                self.video_file = new_path
            else:  # inserted
                temp_audios.append(new_path)
            os.rename(old_path, new_path)
        self.downloaded_audios = temp_audios

    async def get_info(self, file):
        mediainfo_output = subprocess.Popen(['mediainfo', '--Output=JSON', '-f', file], stdout=subprocess.PIPE)
        return json.load(mediainfo_output.stdout)

    async def merge(self, output_filename, type_='ZEE5'):
        """Merge all downloaded stream"""

        # ✅ Safe local import to avoid circular import issues
        from util import run_comman_d, downloadaudiocli, LANGUAGE_FULL_FORM, LANGUAGE_SHORT_FORM  # inserted
        if len(self.selected_audios) > 8:
            FORM_DICT = LANGUAGE_FULL_FORM
        else:  # inserted
            FORM_DICT = LANGUAGE_SHORT_FORM
        output_string = [re.sub('\\([^)]*\\)', '', string) for string in self.selected_audios]
        full_forms = {'ta ': 'Tam', 'te ': 'Tel', 'en ': 'Eng', 'hi ': 'Hin', 'bn ': 'Ben', 'kn ': 'Kan', 'mr ': 'Mar', 'ml ': 'Mal', 'Ta ': 'tam', 'Te ': 'Tel', 'En ': 'Eng', 'Be ': 'Ben', 'Kn ': 'Kan', 'Mr ': 'Mar', 'Ml ': 'Mal'}
        match = None
        ad = 'Unknown'
        if len(self.selected_audios) >= 1:
            match = re.search('\\((.*?)\\)', self.selected_audios[0])
        if match:
            ad = match.group(0)
            ad = ad.split(' - ')[(-1)]
        self.quality = self.quality.split(' ', 1)[0]
        full_forms_list = [full_forms.get(abbr, abbr) for abbr in output_string]
        out_file = f'{output_filename}.{self.quality}p.{type_}.WEB-DL.{Config.END_NAME}.mkv'
        if len(self.selected_audios) == 1:
            FORM_DICT = LANGUAGE_FULL_FORM
            out_file = f"{output_filename}.{self.quality}p {type_}-WEB-DL.{Config.END_NAME}.mkv"
        else:  # inserted
            if len(self.selected_audios) >= 2:
                out_file = f"{output_filename}.{self.quality}p.{type_}-WEB-DL.{Config.END_NAME}.mkv"
        out_file = out_file.replace(' ', '.')
        out_path = os.path.join(self.out_path, out_file)
        video_path = self.video_file
        cmd = f'./ott/ffmpeg -y -i \"{video_path}\" '
        audios = self.downloaded_audios
        for audio in audios:
            cmd += f'-i \"{audio}\" '
        if len(self.downloaded_audios) == 0:
            cmd += '-map 0 '
        else:  # inserted
            cmd += '-map 0:v '
        for i in range(1, len(audios) + 1):
            cmd += f'-map {i}:a? '
        step = 0
        for audio in audios:
            cmd += f'-metadata:s:a:{step} title=\"{Config.METADATA_NAME} - [ - {ad}]\" '
            step += 1
        cmd += f'-c:v copy -c:a copy \"{out_path}\"\n        '
        print(out_path)
        st, stout = await run_comman_d(cmd)
        for aud_file in self.downloaded_audios:
            if 2<3:
                os.remove(aud_file)
        if 2<3:
            os.remove(self.video_file)

        return 
        data = await self.get_info(out_path)
        print(json.dumps(data))
        audio_track = [x for x in data['media']['track'] if x['@type'] == 'Audio']
        audio_track = audio_track[0]
        if audio_track['Format'] == 'E-AC-3':
            codec = 'DD+'
        else:  # inserted
            codec = 'DD'
            if audio_track['Format'] == 'AAC':
                codec = 'AAC'
            else:  # inserted
                if audio_track['Format'] == 'DTS':
                    codec = 'DTS'
                else:  # inserted
                    codec = 'DD+'
        ch = '7.1'
        ch = '5.1'
        v_codec = 'x265'
        ch = '2.0'
        ch = '1.0'
        ch = '5.1'
        ac = '{} {} {}'.format(codec, ch, 'Atmos')
        ac = '{} {}'.format(codec, ch)
        X = [x for x in data['media']['track'] if x['@type'] == 'Video']
        abb = "hi" #ad(video_track, video_track[0])
        cdec = "hello" #video_track[0]['Format'].lower()
        if 'hev' in cdec or 'hvc' in cdec:
            v_codec = 'x265'
        cmd += f'{Config.METADATA_NAME} - [{codec} {ch}- {abb}]\" '
        await run_comman_d(cmd)
        for aud_file in self.downloaded_audios:
            if 2<3:
                os.remove(aud_file)
        if 2<3:
            os.remove(self.video_file)
        return None
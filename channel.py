# -*- coding: utf-8 -*-
#------------------------------------------------------------
# RadioReference.com
#------------------------------------------------------------
# Based on code from pelisalacarta
# License: GPL (http://www.gnu.org/licenses/gpl-3.0.html)
#------------------------------------------------------------

#Code Upated by: Blazetamer 2014

import urlparse,urllib2,urllib,re
import os, sys

from core import logger
from core import config
from core import scrapertools
from core.item import Item

DEBUG = config.get_setting("debug")
URL = "http://www.earthcam.com/network/"
IMAGES = os.path.join(config.get_runtime_path(),"resources")

def isGeneric():
    return True

def mainlist(item):
    logger.info("[channel.py] mainlist")
    itemlist=[]
    itemlist.append( Item(action="cams",      title="Featured Cams" , url=URL ) )
    itemlist.append( Item(action="usa",       title="USA" , url=URL ) )
    itemlist.append( Item(action="worldwide", title="Worldwide" , url=URL ) )
    return itemlist

def worldwide(item):
    logger.info("[channel.py] worldwide")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron  = ';" href="(.+?)" class="locationLink">(.+?)</a>'
    #patron  = '<p class="location"><a\s+onclick="[^"]+" href="(/network/index.php\?page\=world\&country\=[^"]+)" class="[^"]+">([^<]+)</a></p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        url = url.replace('[','').replace(']','')
        print'WORLDWIDE PARSED IS ' +url
        title = scrapedtitle.strip()
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        if 'page=world' in url:
            itemlist.append( Item(action="cams", title=title , url=url, fanart=os.path.join(IMAGES,"fanart.jpg") ) )
    
    return itemlist

def usa(item):
    logger.info("[channel.py] usa")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    patron  = ';" href="(.+?)" class="locationLink">(.+?)</a>'
    #patron  = '<p class="location"><a  onclick="[^"]+" href="(index.php?country=us&[^"]+)" class="[^"]+">([^<]+)</a>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    #match=re.compile(';" href="(.+?)" class="locationLink">(.+?)</a>').findall(link)
    if DEBUG: scrapertools.printMatches(matches)

    for scrapedurl,scrapedtitle in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        print'USA PARSED IS ' +url
        title = scrapedtitle.strip()
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        if 'country=us'in url:
         itemlist.append( Item(action="cams", title=title , url=url, fanart=os.path.join(IMAGES,"fanart.jpg") ) )
    
    return itemlist

def cams(item):
    logger.info("[channel.py] cams")
    itemlist = []

    data = scrapertools.cache_page(item.url)
    #logger.info("data="+data)
    
    patron  = '<div[^<]+'
    patron += '<div[^<]+<a[^<]+<div[^<]+<img\s+class="[^"]*"\s+src="([^"]+)"[^<]+</div>[^<]+'
    patron += '</a></div>[^<]+'
    patron += '<div[^<]+'
    patron += '<p[^<]+<img[^<]+<a href="([^"]+)" class="featuredTitleLink"><span class="featuredTitle">([^<]+)</span></a></p>[^<]+'
    patron += '<p style="[^"]+" class="featuredCity">([^<]+)</p>[^<]+'
    patron += '<p style="[^"]+" class="featuredDescription">([^<]+)</p>'
    matches = re.compile(patron,re.DOTALL).findall(data)
    if DEBUG: scrapertools.printMatches(matches)

    if len(matches)==0:
        patron  = '<div[^<]+'
        patron += '<div[^<]+<a[^<]+<div[^<]+<img\s+class="[^"]*"\s+src="([^"]+)"[^<]+</div>[^<]+'
        patron += '</a></div>[^<]+'
        patron += '<div[^<]+'
        patron += '<p[^<]+<a href="([^"]+)"[^<]+<span[^>]+>([^<]+)</span></a></p>[^<]+'
        patron += '<p style="[^"]+"[^>]+>([^<]+)</p>[^<]+'
        patron += '<p style="[^"]+"[^>]+>([^<]+)</p>'
        matches = re.compile(patron,re.DOTALL).findall(data)
        if DEBUG: scrapertools.printMatches(matches)

    for scrapedthumbnail,scrapedurl,scrapedtitle,location,scrapedplot in matches:
        url = urlparse.urljoin(item.url,scrapedurl)
        thumbnail = urlparse.urljoin(item.url,scrapedthumbnail)
        title = scrapedtitle.strip()+" ("+location+")"
        plot = scrapedplot.strip()
        if (DEBUG): logger.info("title=["+title+"], url=["+url+"]")
        if url.startswith("http://www.earthcam.com") and not url.startswith("http://www.earthcam.com/client/"):
            itemlist.append( Item(action="play", title=title , url=url, thumbnail=thumbnail, fanart=thumbnail, plot=plot, folder=False ) )
    
    return itemlist

def play(item):
    itemlist = []

    data = scrapertools.cache_page(item.url)
    
    # Extracts json info
    json_text = scrapertools.get_match(data,'flashvars.json\s+\=\s*"([^"]+)"')
    logger.info("json_text="+json_text)
    json_decoded = urllib.unquote(json_text)
    logger.info("json_decoded="+json_decoded)
    json_object = load_json(json_decoded)
    logger.info("json_object="+str(json_object))
    
    #http://www.earthcam.com/usa/newyork/timessquare/?cam=tsstreet
    #if "?cam=" in item.url:
    video_url=""
    try:
        # Extract cam_id
        cam_id = item.url.split("?")[1].split("=")[1]
        logger.info("cam_id="+cam_id)
        cam_data=json_object["cam"][cam_id]
        logger.info("cam_data="+str(cam_data))

        offline = cam_data["showOfflineMessage"]
        logger.info("offline="+offline)
        liveon = cam_data["liveon"]
        logger.info("liveon="+liveon)
    
        video_url = cam_data["worldtour_path"]
        logger.info("video_url="+video_url)
    except:
        logger.info("NO cam_id")
        cam_data=json_object["cam"]
        logger.info("cam_data="+str(cam_data))
        logger.info("len(cam_data)=%d" % len(cam_data))
        for cam_id in cam_data:
            logger.info("cam_id="+str(cam_id))
            liveon = cam_data[cam_id]["liveon"]
            logger.info("liveon="+liveon)
            if liveon!="disabled":
                video_url = cam_data[cam_id]["worldtour_path"]
                logger.info("video_url="+video_url)
                break
    
    #video_url2 = scrapertools.get_match(json_decoded,'"worldtour_path"\:"([^"]+)"')
    #logger.info("video_url2="+video_url2)
    
    #video_url = "rtmp://video2.earthcam.com/fecnetwork/hdtimes11.flv"
    #./rtmpdump-2.4 -r "rtmp://video2.earthcam.com/fecnetwork/4828.flv" --swfVfy "http://www.earthcam.com/swf/cam_player_v2/ecnPlayer.swf?20121010" --pageUrl "http://www.earthcam.com/world/turkey/istanbul/" --tcUrl "rtmp://video2.earthcam.com/fecnetwork" --app fecnetwork --live --playpath "4828.flv" -o out.flv
    
    # Taken from http://forum.xbmc.org/archive/index.php/thread-120418-20.html
    # rtmp://video2.earthcam.com/ app=fecnetwork swfUrl=http://www.earthcam.com/swf/cam_player_v2/ecnPlayer.swf playpath=fridaysHD1.flv live=true timeout=180
    
    if video_url.lower().endswith(".jpg") or video_url.lower().endswith(".png"):
        url = video_url
    else:
        rtmp_url = scrapertools.get_match(video_url,"(rtmp\://[^\/]+/)")
        app = scrapertools.get_match(video_url,"rtmp\://[^\/]+/([a-z]+)/")
        playpath = scrapertools.get_match(video_url,"rtmp\://[^\/]+/[a-z]+/([a-zA-Z0-9]+\.flv)")
        swfurl = "http://www.earthcam.com/swf/cam_player_v2/ecnPlayer.swf"
        pageurl = item.url
        
        url=rtmp_url + " app=" + app + " swfUrl=" + swfurl + " playpath=" + playpath + " live=true timeout=180"
        logger.info("url="+url)

    itemlist.append( Item(action="play", title=item.title , server="directo", url=url, fanart=item.thumbnail, thumbnail=item.thumbnail, folder=False) )
    
    return itemlist

def load_json(data):
    # callback to transform json string values to utf8
    def to_utf8(dct):
        rdct = {}
        for k, v in dct.items() :
            if isinstance(v, (str, unicode)) :
                rdct[k] = v.encode('utf8', 'ignore')
            else :
                rdct[k] = v
        return rdct
    try :        
        import json
        json_data = json.loads(data, object_hook=to_utf8)
        return json_data
    except:
        import sys
        for line in sys.exc_info():
            logger.error( "%s" % line ) 

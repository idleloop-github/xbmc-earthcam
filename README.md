# plugin.video.earthcam add-on for Kodi / XBMC

This add-on version will show you more webcams than any other version on internet!

EarthCam.com is the premiere network of scenic webcams and offers a complete database of interesting places and views from around the world. EarthCam.com is the worlds favorite webcam network and the EarthCam Network cameras have been seen on top news shows, including CNN Headline News.

### Installation

* [download released zip](https://github.com/idleloop-github/xbmc-earthcam/releases/download/v1.2.0/plugin.video.earthcam-1.3.0.zip)
* Kodi/XBMC: System / Add-ons / Install from zip file / 
* or Kodi 17: Add-ons / Download / ".." / Install from zip file /
* select [earthcam's zip file](https://github.com/idleloop-github/xbmc-earthcam/releases/download/v1.2.0/plugin.video.earthcam-1.3.0.zip)   
* Note that Kodi will complain about installing from "Unknown sources": in this case, activate this option, and repeat the installation steps.

From version 1.2.0 on, this add-on can play [HLS streams](https://en.wikipedia.org/wiki/HTTP_Live_Streaming), and this mode is more stable than [RTMP](https://en.wikipedia.org/wiki/Real-Time_Messaging_Protocol).   
Please follow **Enable HLS playing** instructions to try it.   

##### Enable HLS playing
From version 1.2.0 on, this add-on can play [HLS streams](https://en.wikipedia.org/wiki/HTTP_Live_Streaming).   
From version 1.3.0 on, HLS is activated by default.   
In order to activate this functionality you have to both activate it in this add-on's configuration,   
and also install (if necessary) and enable the add-on **InputStream Adaptative** (or another add-on capable of playing HLS - for example [awaiters1 releases](https://github.com/awaters1/inputstream.hls/releases)).

* Configure earthcam add-on: Add-ons / Video add-ons / Earthcam / right click / Settings / Enable HLS instead of RMP : activate
* activate "InputStream Adaptative": Add-ons / My Add-ons / VideoPlayer InputStream / InputStream Adaptative / Enable
* Also, configure it to be able to open HD streams: Add-ons / My Add-ons / VideoPlayer InputStream / InputStream Adaptative / Configure / Max. Resolution general decoder: Max [Ok]

* Now check that you can open some cams. If that is not the case, simply deactivate HLS again: Add-ons / Video add-ons / Earthcam / right click / Settings / Enable HLS instead of RMP : deactivate

### Changes

See [changelog.txt](https://github.com/idleloop-github/xbmc-earthcam/blob/master/changelog.txt)

### License

Distributed [under GPL 3](http://www.gnu.org/licenses/gpl-3.0.html)

### Contact

[idleloop](http://www.angelfire.com/ego2/idleloop/) -at- yahoo.com   
BTC: 1GX726he5TNgnDuG4qG9zrM6CSN7uyga6F

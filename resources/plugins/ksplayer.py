'''
    resolveurl XBMC Addon
    Copyright (C) 2018 Whitecream

This program is free software: you can redistribute it and/or modify
it under the terms of the GNU General Public License as published by
the Free Software Foundation, either version 3 of the License, or
(at your option) any later version.

This program is distributed in the hope that it will be useful,
but WITHOUT ANY WARRANTY; without even the implied warranty of
MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
GNU General Public License for more details.

You should have received a copy of the GNU General Public License
along with this program. If not, see <http://www.gnu.org/licenses/>.
'''

from resolveurl.plugins.lib import helpers
from resolveurl import common
from resolveurl.resolver import ResolveUrl, ResolverError

class KSplayerResolver(ResolveUrl):
    name = 'ksplayer'
    domains = ['ksplayer.com']
    pattern = '(?://|\.)(ksplayer\.com)/(?:plugins/mediaplayer/site/_embed\.php\?u=|player/)([A-Za-z0-9]+)'

    def __init__(self):
        self.net = common.Net()

    def get_media_url(self, host, media_id):
        web_url = self.get_url(host, media_id)
        headers = {'User-Agent': common.FF_USER_AGENT,
                   'Referer': web_url}
        response = self.net.http_GET(web_url, headers=headers)
        html = response.content
        sources = helpers.scrape_sources(html)
        return helpers.pick_source(sources) + helpers.append_headers(headers)

    def get_url(self, host, media_id):
        return self._default_get_url(host, media_id, template='https://{host}/player/{media_id}/')

    @classmethod
    def _is_enabled(cls):
        return True
    

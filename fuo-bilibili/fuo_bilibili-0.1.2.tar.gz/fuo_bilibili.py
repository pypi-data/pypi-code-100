import asyncio
import logging
import sys
import threading

import aiohttp

from feeluown.app import App
from feeluown.library import (
    ProviderV2, ProviderFlags as PF, AbstractProvider,
    ModelType, VideoModel, BriefArtistModel,
)
from feeluown.media import Quality, Media, MediaType, VideoAudioManifest
from feeluown.utils.sync import AsyncToSync


__alias__ = 'bilibili'
__version__ = '0.1.2'
__desc__ = 'Bilibili'

local = threading.local()
logger = logging.getLogger('feeluown.fuo_provider_bilibili')

# Global varaiables
SOURCE = 'bilibili'


def enable(app: App):
    provider = BilibiliProvider()
    app.library.register(provider)


def disable(app: App):
    provider = app.library.get(SOURCE)
    if provider is not None:
        app.library.deregister(provider)


class BilibiliApiPatcher:
    """
    Try to workaround https://github.com/MoyuScript/bilibili-api/issues/245
    """
    def patch(self):
        from bilibili_api.utils import network

        def fixed_get_session():
            session = getattr(local, 'session', None)
            if session is None:
                session = aiohttp.ClientSession(loop=asyncio.get_event_loop())
                local.session = session
            return session

        network.get_session = fixed_get_session

        # Delete bilibili_api.*.** modules except bilibili_api.network,
        # so that them can be reloaded and use the `fixed_get_session` implementation.
        mod_to_delete = []
        for mod in sys.modules:
            if mod.startswith('bilibili_api') and 'network' not in mod:
                mod_to_delete.append(mod)
        for mod in mod_to_delete:
            del sys.modules[mod]

    def sync(self, coro):
        """
        Since we create a aiohttp.ClientSession in threads, ensure aiohttp session
        is closed before loop is closed.
        """
        async def wrap_coro(*args, **kwargs):
            try:
                return await coro(*args, **kwargs)
            finally:
                await local.session.close()
        return AsyncToSync(wrap_coro)


# Reimport bilibili_api modules
from bilibili_api.video import Video  # noqa


patcher = BilibiliApiPatcher()
patcher.patch()
Sync = patcher.sync


def create_video(identifier):
    if identifier.isdigit():
        v = Video(aid=int(identifier))
    else:
        # Old bilibili video model trimed the BV prefix.
        if not identifier.startswith('BV'):
            identifier = f'BV{identifier}'
        v = Video(bvid=identifier)
    return v


class BilibiliProvider(AbstractProvider, ProviderV2):
    class meta:
        identifier = 'bilibili'
        name = 'Bilibili'
        flags = {
            ModelType.video: (PF.get | PF.multi_quality | PF.model_v2),
        }

    @property
    def identifier(self):
        return self.meta.identifier

    @property
    def name(self):
        return self.meta.name

    def video_get(self, vid: str):
        v = create_video(vid)
        info = patcher.sync(v.get_info)()
        artists = [BriefArtistModel(source=self.meta.identifier,
                                    identifier=info['owner']['mid'],
                                    name=info['owner']['name'])]
        video = VideoModel(source=self.meta.identifier,
                           identifier=vid,
                           title=info['title'],
                           artists=artists,
                           duration=info['duration'],
                           cover=info['pic'])
        # `pages` means how much parts a video have.
        # TODO: each part should be a video model and have its own identifier
        video.cache_set('pages', [{'cid': page['cid']} for page in info['pages']])
        return video

    def video_get_media(self, video, quality):
        q_media_mapping = self._get_or_fetch_q_media_mapping(video)
        return q_media_mapping.get(quality)

    def video_list_quality(self, video):
        q_media_mapping = self._get_or_fetch_q_media_mapping(video)
        return list(q_media_mapping.keys())

    def _get_or_fetch_q_media_mapping(self, video):
        v = create_video(video.identifier)
        pages = self._model_cache_get_or_fetch(video, 'pages')
        assert pages, 'this should not happend, a video has no part'
        url_info = Sync(v.get_download_url)(cid=pages[0]['cid'])
        q_media_mapping = self._parse_media_info(url_info)
        video.cache_set('q_media_mapping', q_media_mapping)
        return q_media_mapping

    def _parse_media_info(self, url_info):
        q_media_mapping = {}
        dash_info = url_info['dash']
        # Not sure if the `audio` always exists.
        audio_url = dash_info['audio'][0]['base_url']
        for q in sorted(url_info['accept_quality'], reverse=True)[:4]:
            for video in dash_info['video']:
                if video['id'] == q:
                    video_url = video['base_url']
                    if audio_url:
                        obj = VideoAudioManifest(video_url, audio_url)
                    else:
                        obj = video_url
                    media = Media(obj,
                                  type_=MediaType.video,
                                  http_headers={'Referer': 'https://www.bilibili.com/'})
                    # TODO: handle more qualities
                    if q >= 64:
                        q_media_mapping[Quality.Video.fhd] = media
                    elif q >= 32:
                        q_media_mapping[Quality.Video.hd] = media
                    else:
                        q_media_mapping[Quality.Video.sd] = media
        return q_media_mapping

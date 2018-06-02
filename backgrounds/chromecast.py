import json
import logging
import re
from pathlib import Path
from urllib.error import HTTPError
from urllib.request import Request, urlopen

logger = logging.getLogger('backgrounds.chromecast')


class Background:
    __slots__ = ('_href', '_author', '_title')

    def __init__(self, href: str, author: str, title: str):
        """
        :param href: Image source URL
        :param author: Image author, please utilize to provide proper
                       attribution of work.
        :param title: Image title, something repeatable so it can be checked
                      against for future runs.
        """
        self._href = href
        self._author = author
        self._title = title

    @property
    def href(self) -> str:
        return self._href

    @property
    def author(self) -> str:
        return self._author

    @property
    def title(self) -> str:
        return self._title

    def download(self, to: Path) -> None:
        """Download the background to the specified output directory
        :param to: Target directory, the author/title will be appended.
        """
        if not to.exists():
            logger.debug('The author directory does not exist, creating...')
            to.mkdir(parents=True)

        dl_to = to / f'{self.author}-{self.title}'
        if dl_to.exists():
            logger.debug('File %s already exists, skipping.', dl_to.absolute())
            return

        with urlopen(self.href) as resp:
            if resp.getcode() != 200:
                logger.info('Skipping download href %s due to status %d',
                            self.href, resp.getcode())
                return

            logger.debug('Downloading new background: %s', dl_to.absolute())
            with open(dl_to, 'wb') as f:
                f.write(resp.read())


class Chromecast:
    """Discover the backgrounds as provided by Chromecast"""

    TITLE_RE = re.compile(r'"([^"]+)"')
    URL = 'https://clients3.google.com/cast/chromecast/home/v/c9541b08'

    def __call__(self):
        match = re.search(r'JSON\.parse\(([^\)]+)', self.load_page())
        if not match:
            raise ValueError('No match found in the response body, '
                             'the page format may have changed.')

        raw_text = (match.group(1).encode('UTF-8').decode('unicode_escape')
                    .replace('\\u003d', '=')
                    .replace('\\', '')
                    .replace("'", '')
                    .replace('s1280-w1280-h720', 's1920-w1920-h1200')
                    .replace('\n', ''))
        js = json.loads(raw_text)
        for background in js[0]:
            href, author = background[:2]

            # either not a background or we cannot provide proper attribution.
            if any(x is None for x in [href, author]):
                logger.debug('Found image is not likely a background, it '
                             'is missing either the href or author')
                continue

            try:
                yield Background(href, author, self._determine_title(href))
            except HTTPError as e:
                logger.debug('Received an HTTPError, attempting to continue: %s',  # noqa
                             e)
                continue  # ignore any we can't get, whatever.

    def load_page(self) -> str:
        """Load the page source"""
        with urlopen(self.URL) as res:
            assert res.getcode() == 200, (
                'There was an error requesting the data from the server :('
            )
            return res.read().decode()

    def _determine_title(self, href: str) -> str:
        """Attempt to determine a title of the image at the href.

        :param href: Location of the image binary"""
        request = Request(href, method='HEAD')
        with urlopen(request) as res:
            return self.TITLE_RE.search(
                res.getheader('content-disposition')
            ).group(1)


chromecast = Chromecast()

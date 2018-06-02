import logging
from argparse import (
    ArgumentParser,
    ArgumentDefaultsHelpFormatter,
)
from pathlib import Path

from .chromecast import chromecast

logging.basicConfig(level=logging.INFO)


def main():
    parser = ArgumentParser(prog='backgrounds',
                            formatter_class=ArgumentDefaultsHelpFormatter)

    parser.add_argument('-v', '--verbose', help='Increase logging verbosity',
                        action='store_true')

    parser.add_argument('target_dir', type=str,
                        help='Target directory to save downloaded backgrounds')

    args = parser.parse_args()

    logger = logging.getLogger('backgrounds')

    if args.verbose:
        logger.setLevel(logging.DEBUG)

    target = Path(args.target_dir)
    try:
        logger.info('Discovering and downloading chromecast backgrounds...')
        for bg in chromecast():
            bg.download(target)
        logger.info('Finished! Check %s for images.', target.absolute())
    except KeyboardInterrupt:
        pass


if __name__ == '__main__':
    main()

import logging

from .config import BRANCH_OVERRIDES, TRY_BRANCH_OVERRIDE
from .exceptions import CallError
from .utils.git_utils import branch_exists_in_repository, retrieve_git_remote_and_sha, update_git_manifest
from .utils.package import get_packages


logger = logging.getLogger(__name__)


def checkout_sources():
    info = retrieve_git_remote_and_sha('.')
    update_git_manifest(info['url'], info['sha'], 'w')
    logger.info('Starting checkout of source')

    for package in get_packages():
        gh_override = BRANCH_OVERRIDES.get(package.name)

        # TRY_BRANCH_OVERRIDE is a special use-case. It allows setting a branch name to be used
        # during the checkout phase, only if it exists on the remote.
        #
        # This is useful for PR builds and testing where you want to use defaults for most repos
        # but need to test building of a series of repos with the same experimental branch
        #
        if TRY_BRANCH_OVERRIDE:
            retries = 3
            while retries:
                try:
                    if branch_exists_in_repository(package.origin, TRY_BRANCH_OVERRIDE):
                        gh_override = TRY_BRANCH_OVERRIDE
                except CallError:
                    retries -= 1
                    logger.debug(
                        'Failed to determine if %r branch exists for %r. Trying again',
                        TRY_BRANCH_OVERRIDE, package.origin
                    )
                    if not retries:
                        logger.debug('Unable to determine if %r branch exists in 3 attempts.', TRY_BRANCH_OVERRIDE)
                else:
                    break

        package.checkout(gh_override)

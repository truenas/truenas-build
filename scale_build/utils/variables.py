import os


BUILDER_DIR = './'
TMPFS = './tmp/tmpfs'
CACHE_DIR = './tmp/cache'
CD_DIR = './tmp/cdrom'
CHROOT_BASEDIR = os.path.join(TMPFS, 'chroot')
CHROOT_OVERLAY = os.path.join(TMPFS, 'chroot-overlay')
CONF_SOURCES = os.path.join(BUILDER_DIR, 'conf/sources.list')
CONF_GRUB = os.path.join(BUILDER_DIR, 'scripts/grub.cfg')
DPKG_OVERLAY = './tmp/dpkg-overlay'
GIT_MANIFEST_PATH = './logs/GITMANIFEST'
GIT_LOG_PATH = './logs/git-checkout.log'
HASH_DIR = './tmp/pkghashes'
LOG_DIR = './logs'
MANIFEST = './conf/build.manifest'
PARALLEL_BUILDS = int(os.environ.get('PARALLEL_BUILDS') or 4)
PKG_DEBUG = bool(os.environ.get('PKG_DEBUG'))
PKG_DIR = './tmp/pkgdir'
PKG_LOG_DIR = os.path.join(LOG_DIR, 'packages')
RELEASE_DIR = './tmp/release'
REQUIRED_RAM = 16  # GB
SOURCES_DIR = './sources'
TMP_DIR = './tmp'
UPDATE_DIR = os.path.join(TMP_DIR, 'update')
WORKDIR_OVERLAY = os.path.join(TMPFS, 'workdir-overlay')


if PKG_DEBUG:
    PARALLEL_BUILDS = 1

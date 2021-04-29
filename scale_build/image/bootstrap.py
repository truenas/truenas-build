import os
import shutil

from scale_build.utils.run import run
from scale_build.utils.paths import CHROOT_BASEDIR, PKG_DIR, TMPFS

from .utils import PACKAGE_PATH


def setup_chroot_basedir(bootstrapdir_obj, logger):
    if os.path.exists(CHROOT_BASEDIR):
        shutil.rmtree(CHROOT_BASEDIR)
    os.makedirs(TMPFS, exist_ok=True)
    run(
        ['mount', '-t', 'tmpfs', '-o', 'size=12G', 'tmpfs', TMPFS],
        logger=logger
    )
    bootstrapdir_obj.restore_cache(CHROOT_BASEDIR)
    run(['mount', 'proc', os.path.join(CHROOT_BASEDIR, 'proc'), '-t', 'proc'], logger=logger)
    run(['mount', 'sysfs', os.path.join(CHROOT_BASEDIR, 'sys'), '-t', 'sysfs'], logger=logger)
    os.makedirs(PACKAGE_PATH, exist_ok=True)
    run(['mount', '--bind', PKG_DIR, PACKAGE_PATH], logger=logger)


def umount_tmpfs_and_clean_chroot_dir():
    if os.path.exists(CHROOT_BASEDIR):
        shutil.rmtree(CHROOT_BASEDIR)
    run(['umount', '-f', TMPFS], check=False)


def umount_chroot_basedir():
    for command in (
        ['umount', '-f', PACKAGE_PATH],
        ['umount', '-f', os.path.join(CHROOT_BASEDIR, 'proc')],
        ['umount', '-f', os.path.join(CHROOT_BASEDIR, 'sys')],
    ):
        run(command, check=False)


def clean_mounts():
    umount_chroot_basedir()
    umount_tmpfs_and_clean_chroot_dir()
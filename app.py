#!/usr/bin/env python3
# project template
# Copyright(C) 2010 Red Hat, Inc.
#
# This program is free software: you can redistribute it and / or modify
# it under the terms of the GNU General Public License as published by
# the Free Software Foundation, either version 3 of the License, or
# (at your option) any later version.
#
# This program is distributed in the hope that it will be useful,
# but WITHOUT ANY WARRANTY without even the implied warranty of
# MERCHANTABILITY or FITNESS FOR A PARTICULAR PURPOSE. See the
# GNU General Public License for more details.
#
# You should have received a copy of the GNU General Public License
# along with this program. If not, see <http://www.gnu.org/licenses/>.

import os
import logging

import click

from thoth.common import init_logging
from thoth.analyzer import run_command

init_logging()

_LOGGER = logging.getLogger("image_pusher")

_HERE_DIR = os.path.dirname(os.path.abspath(__file__))
_SKOPEO_EXEC_PATH = os.getenv("SKOPEO_EXEC_PATH", os.path.join(_HERE_DIR, "bin", "skopeo"))


@click.group()
@click.option(
    "--verbose", "-v", is_flag=True, envvar="THOTH_VERBOSE_IMAGE_PUSHER", help="Be verbose about what is going on."
)
def cli(verbose):
    if verbose:
        _LOGGER.setLevel(logging.DEBUG)


@cli.command(name='push')
@click.argument('src', nargs=1)
@click.option(
    "--user-src",
    "-us",
    type=str,
    envvar="THOTH_SRC_REGISTRY_USER",
    help="Username used in the source registry.",
)
@click.option(
    "--pass-src",
    "-ps",
    type=str,
    envvar="THOTH_SRC_REGISTRY_PASSWORD",
    help="Password for the source registry.",
)
@click.argument('dst', nargs=1)
@click.option(
    "--user-dst",
    "-ud",
    type=str,
    envvar="THOTH_DST_REGISTRY_USER",
    help="Username used in the target registry.",
)
@click.option(
    "--pass-dst",
    "-pd",
    type=str,
    envvar="THOTH_DST_REGISTRY_PASSWORD",
    help="Password for the target registry.",
)
def push(src, dst, user_src=None, pass_src=None, user_dst=None, pass_dst=None):
    '''
        [SRC] [DST]
        Push a container image from a source to an external registry
    '''
    _LOGGER.debug(user_src)
    _LOGGER.debug(pass_src)
    _LOGGER.debug(user_dst)
    _LOGGER.debug(pass_dst)

    cmd = f"{_SKOPEO_EXEC_PATH} copy {src} {dst}"

    if user_src:
        cmd += f"--src-creds={user_src}"

        if pass_src:
            cmd += f":{pass_src}"

        cmd += " "

    if user_dst:
        cmd += f"--dest-creds={user_dst}"

        if pass_dst:
            cmd += f":{pass_dst}"

        cmd += " "
    
    image_name = src.rsplit("/", maxsplit=1)[1]
    if "quay.io" in dst:
        image_name = image_name.replace("@sha256", "")
        output = f"{dst}:{image_name.replace(':','-')}"
    else:
        output = f"{dst}/{image_name}"

    _LOGGER.debug("Pushing image %r from %r to registry %r, output is %r", image_name, src, dst, output)
    cmd += f"docker://{src} docker://{output}"

    _LOGGER.debug("Running: %s", cmd)
    try:
        command = run_command(cmd)
        _LOGGER.debug("%s stdout:\n%s\n%s", _SKOPEO_EXEC_PATH, command.stdout, command.stderr)
    except CommandError as exc:
        if "Error determining manifest MIME type" in exc.stderr:
            # Manifest MIME type error is caused by the way image is build. we have no control over it.
            _LOGGER.warning("Ignoring error caused by invalid manifest MIME type during push: %s", str(exc))
            return
        else:
            _LOGGER.exception("Failed to push image %r to external registry: %s", image_name, str(exc))
    
    return output



if __name__ == '__main__':
    cli()
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

"""This is the main script of the template project."""
import click
import logging

from thoth.common import init_logging
from thoth.analyzer import run_command



init_logging()

_LOGGER = logging.getLogger('image_pusher')



@click.group()
def cli():
    pass


@cli.command(name='push')
@click.argument('src', nargs=1)
@click.argument('dst', nargs=1)
def push(src, dst):
    '''
        [SRC] [DST]
        Push a container image from a source to an external registry
    '''
    skopeo_cmd = f'skopeo copy {src} {dst}'
    run_command(skopeo_cmd)



if __name__ == '__main__':
    cli()
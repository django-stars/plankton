import asyncio
import sys
import shlex

from asyncio.subprocess import PIPE, STDOUT


import settings
import logging

logger = logging.getLogger('plankton.wkhtmltopdf.utils.exec_wkhtmltopdf')


async def exec_wkhtmltopdf(data):
    # Prepare inline options parameters for command

    command_args = [settings.WKHTMLTOPDF_CMD]
    command_args.extend(_options_to_args(data.get('options', settings.WKHTMLTOPDF_DEFAULT_OPTIONS)))
    # Output to STDOUT
    command_args.extend([data['page'], '-'])

    command_out = await _get_lines(' '.join(command_args))

    if b'%PDF-' in command_out:
        debug_info, pdf_content = command_out.split(b'%PDF-', 1)
    else:
        raise Exception('{}\n{}'.format(command_args, command_out))

    pdf_content = b'%PDF-' + pdf_content

    logger.info(debug_info)

    return pdf_content


def _options_to_args(options):
    flags = []

    for k, v in options.items():
        if v in [False, None]:
            continue

        if isinstance(v, list):
            # wkhtmltopdf can accept many parameters like --cookie
            for item in v:
                flags.extend(_options_to_args({k: item}))
        else:
            flags.append('--{}'.format(k))

            if v is not True:
                flags.append(shlex.quote(v))

    return flags


async def _get_lines(shell_command):
    proc = await asyncio.create_subprocess_shell(
        shell_command,
        stdin=PIPE, stdout=PIPE, stderr=STDOUT
    )

    out, errs = await proc.communicate()

    return out

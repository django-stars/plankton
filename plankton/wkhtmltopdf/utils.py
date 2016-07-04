import asyncio
import sys
import shlex

from asyncio.subprocess import PIPE, STDOUT


import settings
import logging

logger = logging.getLogger('plankton.wkhtmltopdf.utils.exec_wkhtmltopdf')


class WkhtmlToPdfFailure(Exception):
    pass


async def exec_wkhtmltopdf(data):
    # Prepare inline options parameters for command

    command_args = [settings.WKHTMLTOPDF_CMD]
    command_args.extend(_options_to_args(data.get('options', settings.WKHTMLTOPDF_DEFAULT_OPTIONS)))
    # Output to STDOUT
    command_args.extend([data['page'], '-'])

    proc = await asyncio.create_subprocess_shell(
        ' '.join(command_args),
        stdin=PIPE, stdout=PIPE, stderr=STDOUT
    )

    command_out, errs = await proc.communicate()

    if b'%PDF-' in command_out:
        debug_info, pdf_content = command_out.split(b'%PDF-', 1)
    else:
        error_msg = command_out.decode('utf-8').replace('\n', ' ')
        raise WkhtmlToPdfFailure(error_msg)

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


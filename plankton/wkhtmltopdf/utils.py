import asyncio
import sys
import shlex

from asyncio.subprocess import PIPE, STDOUT


from plankton import settings
import logging

logger = logging.getLogger('plankton.wkhtmltopdf.utils.exec_wkhtmltopdf')


class WkhtmlToPdfFailure(Exception):
    pass


def wkhtmltopdf_args_mapping(data):
    """
    fix our names to wkhtmltopdf's args
    """
    mapping = {
        'cookies': 'cookie',
        'custom-headers': 'custom-header',
        'run-scripts': 'run-script'
    }

    return {mapping.get(k, k): v for k, v in data.items()}


async def exec_wkhtmltopdf(data):
    data = wkhtmltopdf_args_mapping(data)
    # security things
    data['disable-local-file-access'] = True

    # Prepare inline options parameters for command

    command_args = [settings.WKHTMLTOPDF_CMD]
    command_args.extend(_options_to_args(data.get('options', settings.WKHTMLTOPDF_DEFAULT_OPTIONS)))
    # Output to STDOUT
    command_args.extend([shlex.quote(data['page']), '-'])

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

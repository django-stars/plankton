import json
from aiohttp import web
from aiohttp.web_exceptions import  HTTPBadRequest
from aiohttp.web_reqrep import Response

from .utils import exec_wkhtmltopdf, WkhtmlToPdfFailure
from .validators import WkhtmlToPdfParamsValidator


def alive(request):
    return Response(
        body=bytes(
            json.dumps({'isAlive': True}),
            'utf-8'
        ),
        status=200,
        content_type='application/json')


class HtmlToPdfView(web.View):
    async def post(self):
        try:
            data = await self.request.json()
        except ValueError:
            raise HTTPBadRequest(reason='You should provide valid json body.')

        validator = WkhtmlToPdfParamsValidator()

        if not validator.validate(data):
            raise HTTPBadRequest(
                reason='Invalid input params',
                body=bytes(json.dumps(validator.errors), 'utf-8'),
                content_type='application/json')

        try:
            pdf_output = await exec_wkhtmltopdf(data)
        except WkhtmlToPdfFailure as e:
            raise HTTPBadRequest(
                reason=e
            )


        return Response(body=pdf_output, status=200, content_type='application/pdf')

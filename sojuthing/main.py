from urllib.parse import urlparse

import aiohttp
from quart import Quart, request, Response
from quart.datastructures import FileStorage

app = Quart(__name__)


def get_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(headers={'User-Agent': 'soju-nil/0.1'}, raise_for_status=True)


@app.route('/', methods=['GET'])
async def index() -> str:
    return 'sojuthing is running'


@app.route('/', methods=['OPTIONS'])
async def options() -> Response:
    return Response(
        status=204,
        headers={
            'Accept-Post': '*',
        },
    )


@app.route('/', methods=['POST'])
async def upload() -> Response:
    files = await request.files
    file = files.get('data')

    if not isinstance(file, FileStorage):
        return Response('missing bad part', status=400)

    form_data = aiohttp.FormData()
    form_data.add_field(
        'file', file.stream, filename=file.filename, content_type='application/octet-stream'
    )

    async with get_session() as session:
        try:
            async with session.post(
                'https://0x0.st',
                data=form_data,
            ) as result:
                body = await result.text()
                # rewrite to https as 0x0.st returns insecure http links
                upload_url = urlparse(body)._replace(scheme='https').geturl()
                return Response(upload_url, status=201, headers={'Location': upload_url})

        except aiohttp.ClientError as e:
            return Response(f'upload failed: {e}', status=500)

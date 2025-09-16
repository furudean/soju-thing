from urllib.parse import urlparse

import aiohttp
from quart import Quart, request, Response
from quart.datastructures import FileStorage

app = Quart(__name__, static_url_path='', static_folder='static')


def get_session() -> aiohttp.ClientSession:
    return aiohttp.ClientSession(headers={'User-Agent': 'soju-nil/0.1'}, raise_for_status=True)


@app.route('/upload', methods=['POST'])
@app.route('/uploads', methods=['POST'])
async def upload() -> Response:
    files = await request.files
    file: FileStorage = files.get('data')  # type: ignore

    if file is None:
        return Response('missing data part', status=400)

    async with get_session() as session:
        form_data = aiohttp.FormData()
        form_data.add_field(
            'file', file.stream, filename=file.filename, content_type='application/octet-stream'
        )

        try:
            async with session.post(
                'https://0x0.st',
                data=form_data,
            ) as result:
                body = await result.text()
                # rewrite to https as 0x0.st returns insecure http links
                upload_url = urlparse(body)._replace(scheme='https')
                return Response(upload_url, status=201, headers={'Location': upload_url.geturl()})

        except aiohttp.ClientError as e:
            return Response(f'upload failed: {e}', status=500)

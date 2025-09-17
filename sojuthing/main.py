from urllib.parse import urlparse
import mimetypes

import aiohttp
from quart import Quart, request, Response

app = Quart(__name__)


def extract_filename_from_content_disposition(content_disposition: str) -> str | None:
    """Extract filename from Content-Disposition header."""
    if not content_disposition:
        return 'file'

    for part in content_disposition.split(';'):
        part = part.strip()
        if part.startswith('filename='):
            filename = part[9:].strip('"\'')
            return filename if filename else 'file'

    return 'file'


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
    file_data = await request.get_data()

    if file_data is None or len(file_data) == 0:
        return Response('missing file data', status=400)

    content_disposition = request.headers.get('content-disposition', '')
    filename = extract_filename_from_content_disposition(content_disposition)

    if filename is not None:
        content_type = mimetypes.guess_type(filename)[0]

    form_data = aiohttp.FormData()
    form_data.add_field(
        name='file',
        value=file_data,
        filename=filename,
        content_type=content_type or 'application/octet-stream',
    )

    async with aiohttp.ClientSession(headers={'User-Agent': 'soju-nil/0.1'}) as session:
        try:
            async with session.post(
                'https://0x0.st',
                data=form_data,
            ) as result:
                body = await result.text()
                # rewrite to https as 0x0.st returns insecure http links
                try:
                    upload_url = urlparse(body.strip())._replace(scheme='https').geturl()
                    return Response(upload_url, status=201, headers={'Location': upload_url})
                except Exception:
                    return Response('invalid response from upload service', status=500)

        except aiohttp.ClientError as e:
            return Response(f'upload failed: {e}', status=500)

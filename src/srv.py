from aiohttp import web

async def handle_post(request):
    data = await request.post()
    print(data)
    name = data.get('name', 'Anonymous')
    return web.Response(text=f'Hello, {name}')

async def handle_post1(request):
    try:
        data = await request.json()
        name = data.get('name', 'Anonymous')
        age = data.get('age', 'Unknown')
        return web.Response(text=f'Hello, {name}! Age: {age}')
    except Exception as e:
        return web.Response(text=f'Error: {str(e)}', status=400)

app = web.Application()
app.router.add_post('/post-example', handle_post)

if __name__ == '__main__':
    web.run_app(app)

import aiohttp
from web_math.errors import BadArgument

async def calculate(expr, precision = None):
    expr = expr.replace("**", "^")
    expr = expr.replace("+", "%2B")
    async with aiohttp.ClientSession() as session:
        async with session.get(f"http://api.mathjs.org/v4/?expr={expr}&precision={precision}") as r:
            result = await r.text()
    if result.startswith("Error:"):
        raise BadArgument("An Invalid argument was passed.")
    return result

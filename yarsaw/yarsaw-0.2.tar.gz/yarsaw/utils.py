class Utils:
    def __init__(self):
        pass

    async def format_joke(self, joke : dict, joined_by : str = '\n') -> dict:
        if joke.get('type') == 'twopart':
            return f"{joke.get('setup')}{joined_by}{joke.get('delivery')}"
        else:
            return joke.get("joke")

PLANS = {
    'free' : '',
    'pro' : 'premium/pro',
    'ultra' : 'premium/ultra',
    'biz' : 'premium/biz',
    'mega' : 'premium/mega'
}

class InvalidPlanError(Exception):
    pass
    
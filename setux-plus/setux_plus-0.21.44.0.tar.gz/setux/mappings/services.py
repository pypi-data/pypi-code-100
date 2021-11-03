from setux.core.mapping import Services


class Artix(Services):
    mapping = dict(
        cron = 'cronie',
    )

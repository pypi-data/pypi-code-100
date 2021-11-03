from aleksis.core.util.apps import AppConfig


class ResintConfig(AppConfig):
    name = "aleksis.apps.resint"
    verbose_name = "AlekSIS – Resint (Public poster)"

    urls = {
        "Repository": "https://edugit.org/AlekSIS/official/AlekSIS-App-Resint/",
    }
    licence = "EUPL-1.2+"
    copyright_info = (
        ([2018, 2019, 2020, 2021], "Jonathan Weth", "dev@jonathanweth.de"),
        ([2020, 2021], "Frank Poetzsch-Heffter", "p-h@katharineum.de"),
        ([2019], "Julian Leucker", "leuckeju@katharineum.de"),
    )

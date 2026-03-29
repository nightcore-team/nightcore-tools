"""Constants for forms feature."""

from typing import Final

from .types import OrganizationInfo

FORM_TEXT: Final[str] = """
Организация / Причина постановки на должность:
Игровой ник:
Игровой уровень:

Имя:
Возраст:
Город проживания:
Онлайн в день:
Ссылка форума:
Ссылка вк (Cтрого ID):
Привязка по почте в игре ( скриншот + /time):
Привязка вконтакте в игре (скриншот + /time):
ID аккаунта:
Дискорд:
IP-адреса: R-IP [***] - IP [***]
"""

BUSINESS_TEXT: Final[str] = """
Ваш ник:
Ваша мафия:
От какой мафии должны выдать бизнесов:
Сколько бизнесов вам должны выдать:
Доказательство для выдачи:
Результат стрелы, по которой вам выдают биз:
Причина выдачи бизнеса:
"""

TERRITORY_TEXT: Final[str] = """
Игровой никнейм:
Ваша банда:
От какой банды должны выдать территории?:
Количество территорий, которые вам должны выдать:
Доказательство для выдачи:
"""

TEXT_DICTIONARY: Final[dict[str, str]] = {
    "mafia": FORM_TEXT,
    "ghetto": FORM_TEXT,
    "business": BUSINESS_TEXT,
    "territory": TERRITORY_TEXT,
}

TITLE_DICTIONARY: Final[dict[str, str]] = {
    "mafia": "Анкета на пост заместителя (Мафия)",
    "ghetto": "Анкета на пост заместителя (Гетто)",
    "business": "Заявка на выдачу бизнеса",
    "territory": "Заявка на выдачу территории",
}

GLOBAL_DEPUTY_ILLEGAL_ROLE_ID: Final[int] = 1184189905644032070

ORGANIZATIONS_DICTIONARY: Final[dict[str, list[OrganizationInfo]]] = {
    "ghetto": [
        OrganizationInfo(name="Grove Street", deputy_role_id=""),
    ],
    "mafia": [
        OrganizationInfo(name="La Cosa Nostra", deputy_role_id=""),
        OrganizationInfo(name="Yakuza", deputy_role_id="456456"),
        OrganizationInfo(name="Russian Mafia", deputy_role_id="456456"),
    ],
}

MAFIA_ACCESS_ROLES: Final[list[int]] = [
    693824998208569377,
    693824997520572456,
    693824979657293905,
]
GHETTO_ACCESS_ROLES: Final[list[int]] = [
    693825000393801752,
    693825000066777178,
    693824979657293905,
]

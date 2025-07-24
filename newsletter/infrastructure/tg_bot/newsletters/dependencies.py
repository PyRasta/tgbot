from typing import Annotated

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession
from newsletter.application.users.ports import UsersStoragePort
from newsletter.application.newsletters.ports import (
    NewslettersStoragePort,
    SentNewslettersStoragePort,
    NewslettersSenderPort,
)
from newsletter.infrastructure.tg_bot.dependencies import use_db_session
from newsletter.infrastructure.tg_bot.users.dependencies import use_users_storage
from newsletter.infrastructure.db.storages.newsletters import (
    AlchemyNewslettersStorage,
    AlchemySentNewslettersStorage,
)
from newsletter.application.newsletters.controllers import (
    CreateNewsletterController,
    CreateSentNewsletterController,
    GetNewsletterController,
)


def use_newsletters_storage(
    session: Annotated[AsyncSession, Depends(use_db_session)],
) -> NewslettersStoragePort:
    return AlchemyNewslettersStorage(session)


def use_sent_newsletters_storage(
    session: Annotated[AsyncSession, Depends(use_db_session)],
) -> SentNewslettersStoragePort:
    return AlchemySentNewslettersStorage(session)


def use_get_newsletter_controller(
    newsletter_storage: Annotated[
        NewslettersStoragePort, Depends(use_newsletters_storage)
    ],
) -> GetNewsletterController:
    return GetNewsletterController(newsletter_storage)


def use_create_sent_newsletter_controller(
    sent_newsletter_storage: Annotated[
        SentNewslettersStoragePort, Depends(use_sent_newsletters_storage)
    ],
) -> CreateSentNewsletterController:
    return CreateSentNewsletterController(sent_newsletter_storage)

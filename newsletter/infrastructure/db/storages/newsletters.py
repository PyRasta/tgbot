from pydantic import TypeAdapter
from sqlalchemy import insert, select, update
from sqlalchemy.orm import selectinload
from sqlalchemy.ext.asyncio import AsyncSession

from newsletter.application.newsletters.ports import (
    NewslettersStoragePort,
    SentNewslettersStoragePort,
)
from newsletter.domain.newsletters.exceptions import NewsletterNotFoundError
from newsletter.domain.newsletters.models import Newsletter, SentNewsletter
from newsletter.infrastructure.db.models.newsletters import (
    DatabaseNewsletter,
    DatabaseSentNewsletter,
)


class AlchemyNewslettersStorage(NewslettersStoragePort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, newsletter: Newsletter) -> Newsletter:
        query = (
            insert(DatabaseNewsletter)
            .values(
                **newsletter.model_dump(mode="json", exclude={"id", "created_by"}),
                created_by_id=newsletter.created_by.id,
            )
            .returning(DatabaseNewsletter.id)
        )
        result = await self._session.execute(query)
        newsletter_id = result.scalar_one()
        newsletter.id = newsletter_id
        return newsletter

    async def get_by_id(self, newsletter_id: int) -> Newsletter:
        query = (
            select(DatabaseNewsletter)
            .options(selectinload(DatabaseNewsletter.created_by))
            .where(DatabaseNewsletter.id == newsletter_id)
        )
        result = await self._session.execute(query)
        db_message = result.scalar_one_or_none()
        if db_message is None:
            raise NewsletterNotFoundError(f"Не найдена рассылка с id={newsletter_id}")

        return Newsletter.model_validate(db_message)


class AlchemySentNewslettersStorage(SentNewslettersStoragePort):
    def __init__(self, session: AsyncSession):
        self._session = session

    async def create(self, sent_newsletter: SentNewsletter) -> SentNewsletter:
        query = (
            insert(DatabaseSentNewsletter)
            .values(
                **sent_newsletter.model_dump(
                    mode="json", exclude={"id", "newsletter", "target"}
                ),
                newsletter_id=sent_newsletter.newsletter.id,
                target_id=sent_newsletter.target.id,
            )
            .returning(DatabaseSentNewsletter.id)
        )
        result = await self._session.execute(query)
        sent_message_id = result.scalar_one()
        sent_newsletter.id = sent_message_id
        return sent_newsletter

    async def get_all(self) -> list[SentNewsletter]:
        query = select(DatabaseSentNewsletter).options(
            selectinload(DatabaseSentNewsletter.newsletter).selectinload(
                DatabaseNewsletter.created_by
            )
        )
        result = await self._session.execute(query)
        return TypeAdapter(list[SentNewsletter]).validate_python(result.scalars())

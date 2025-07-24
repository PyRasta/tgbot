from newsletter.application.newsletters.ports import (
    NewslettersSenderPort,
    NewslettersStoragePort,
    SentNewslettersStoragePort,
)
from newsletter.application.users.ports import UsersStoragePort
from newsletter.domain.newsletters.models import Newsletter, SentNewsletter


class CreateNewsletterController:
    def __init__(self, newsletters_storage: NewslettersStoragePort):
        self._newsletters_storage = newsletters_storage

    async def execute(self, newsletter: Newsletter) -> Newsletter:
        return await self._newsletters_storage.create(newsletter)


class GetNewsletterController:
    def __init__(self, newsletters_storage: NewslettersStoragePort):
        self._newsletters_storage = newsletters_storage

    async def execute(self, newsletter_id: int) -> Newsletter:
        return await self._newsletters_storage.get_by_id(newsletter_id)


class CreateSentNewsletterController:
    def __init__(self, sent_newsletter_storage: SentNewslettersStoragePort):
        self._sent_newsletter_storage = sent_newsletter_storage

    async def execute(self, sent_newsletter: SentNewsletter) -> SentNewsletter:
        return await self._sent_newsletter_storage.create(sent_newsletter)


class SendNewsletterController:
    def __init__(
        self,
        sent_newsletters_storage: SentNewslettersStoragePort,
        newsletter_storage: NewslettersStoragePort,
        users_storage: UsersStoragePort,
        newsletters_sender: NewslettersSenderPort,
    ):
        self._sent_newsletters_storage = sent_newsletters_storage
        self._newsletter_storage = newsletter_storage
        self._users_storage = users_storage
        self._newsletters_sender = newsletters_sender

    async def execute(self, newsletter: Newsletter) -> None:
        users = await self._users_storage.get_all()
        self._newsletters_sender.send(newsletter, users)

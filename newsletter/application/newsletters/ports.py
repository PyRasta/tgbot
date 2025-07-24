from abc import ABC, abstractmethod

from newsletter.domain.newsletters.models import Newsletter, SentNewsletter
from newsletter.domain.users.models import User


class NewslettersStoragePort(ABC):
    @abstractmethod
    async def create(self, newsletter: Newsletter) -> Newsletter: ...

    @abstractmethod
    async def get_by_id(self, newsletter_id: int) -> Newsletter: ...


class SentNewslettersStoragePort(ABC):
    @abstractmethod
    async def create(self, sent_newsletter: SentNewsletter) -> SentNewsletter: ...

    @abstractmethod
    async def get_all(self) -> list[SentNewsletter]: ...


class NewslettersSenderPort(ABC):
    @abstractmethod
    def send(self, newsletter: Newsletter, users: list[User]) -> None: ...

from abc import ABC, abstractmethod

from app.services import (
    ReviewsModerationService,
    ReviewsService,
    ReviewsStatisticsService,
)


class ServicesFactory(ABC):
    @abstractmethod
    def get_reviews_moderation_service(self) -> ReviewsModerationService: ...

    @abstractmethod
    def get_reviews_service(self) -> ReviewsService: ...

    @abstractmethod
    def get_reviews_statistics_service(self) -> ReviewsStatisticsService: ...

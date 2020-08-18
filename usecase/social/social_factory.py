from abc import ABC, abstractmethod
from core.social import AbsSocial
from typing import Optional


class SocialFactory(ABC):

    @abstractmethod
    def create_social(self, social_param: str) -> Optional[AbsSocial]:
        pass

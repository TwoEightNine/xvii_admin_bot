from core import AbsSocial
from usecase.social import SocialFactory
from .vk_social import VkSocial
from typing import Optional

from secret import access_token


class SocialFactoryImpl(SocialFactory):
    supported_values = ['vk']

    def create_social(self, social_param: str) -> Optional[AbsSocial]:
        social = self.__create(social_param)
        if social:
            social.set_api_keys(access_token)
        return social

    def __create(self, social_param: str) -> Optional[AbsSocial]:
        if social_param == 'vk':
            return VkSocial()
        else:
            return None

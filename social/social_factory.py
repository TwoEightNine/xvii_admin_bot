from typing import Optional

from social import AbsSocial, VkSocial

supported_socials = ['vk']


def create_social(social: str) -> Optional[AbsSocial]:
    if social == 'vk':
        return VkSocial()

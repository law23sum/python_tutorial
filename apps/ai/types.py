from dataclasses import dataclass

from apps.users.models import CustomUser


@dataclass
class UserDependencies:
    user: CustomUser

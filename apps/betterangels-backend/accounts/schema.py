from typing import cast

import strawberry
import strawberry_django
from accounts.groups import GroupTemplateNames
from accounts.models import User
from common.graphql.types import DeletedObjectType
from common.permissions.utils import IsAuthenticated
from django.db import transaction
from django.db.models import QuerySet
from notes.permissions import NotePermissions
from organizations.models import Organization
from strawberry.types import Info
from strawberry_django import auth
from strawberry_django.auth.utils import get_current_user
from strawberry_django.mutations import resolvers
from strawberry_django.pagination import OffsetPaginated
from strawberry_django.permissions import HasPerm

from .types import (
    AuthInput,
    AuthResponse,
    LoginInput,
    OrganizationType,
    UpdateUserInput,
    UserType,
)


@strawberry.type
class Query:
    current_user: UserType = auth.current_user()  # type: ignore

    @strawberry_django.offset_paginated(OffsetPaginated[OrganizationType], extensions=[HasPerm(NotePermissions.ADD)])
    def caseworker_organizations(self) -> QuerySet[Organization]:
        queryset: QuerySet[Organization] = Organization.objects.filter(
            permission_groups__name__icontains=GroupTemplateNames.CASEWORKER
        )
        return queryset


@strawberry.type
class Mutation:
    logout = auth.logout()

    @strawberry.mutation
    def login(self, input: LoginInput) -> AuthResponse:
        # The is a stub and logic is handled client-side by Apollo
        return AuthResponse(status_code="")

    @strawberry.mutation
    def google_auth(self, input: AuthInput) -> AuthResponse:
        # The is a stub and logic is handled client-side by Apollo
        return AuthResponse(status_code="")

    @strawberry.mutation
    def apple_auth(self, input: AuthInput) -> AuthResponse:
        # The is a stub and logic is handled client-side by Apollo
        return AuthResponse(status_code="")

    @strawberry_django.mutation(permission_classes=[IsAuthenticated])
    def update_current_user(self, info: Info, data: UpdateUserInput) -> UserType:
        user = cast(User, get_current_user(info))
        if str(user.pk) != str(data.id):
            raise PermissionError("You do not have permission to modify this user.")

        user_data: dict = strawberry.asdict(data)

        user = resolvers.update(
            info,
            user,
            {
                **user_data,
                "id": user.pk,
            },
        )

        return cast(UserType, user)

    @strawberry_django.mutation(permission_classes=[IsAuthenticated])
    def delete_current_user(self, info: Info) -> DeletedObjectType:
        user = get_current_user(info)
        if user.pk is None:
            raise RuntimeError("Cannot delete user.")

        user_id = user.pk

        with transaction.atomic():
            user.delete()

        return DeletedObjectType(id=user_id)

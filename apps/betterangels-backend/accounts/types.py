from typing import List, Optional, Tuple

import strawberry
import strawberry_django
from common.graphql.types import NonBlankString
from django.db.models import Q, QuerySet
from organizations.models import Organization
from strawberry import ID, Info, auto

from .models import User


@strawberry.input
class AuthInput:
    code: Optional[str] = strawberry.field(name="code")
    code_verifier: Optional[str] = strawberry.field(name="code_verifier")
    id_token: Optional[str] = strawberry.field(name="id_token")
    redirect_uri: Optional[str] = strawberry.field(name="redirect_uri")


@strawberry.type
class AuthResponse:
    status_code: str = strawberry.field(name="status_code")


@strawberry.input
class LoginInput:
    username: str
    password: str


@strawberry_django.ordering.order(Organization)
class OrganizationOrder:
    name: auto
    id: auto


@strawberry_django.filters.filter(Organization)
class OrganizationFilter:
    @strawberry_django.filter_field
    def search(
        self, queryset: QuerySet, info: Info, value: Optional[str], prefix: str
    ) -> Tuple[QuerySet[Organization], Q]:
        if value is None:
            return queryset, Q()

        search_terms = value.split()
        query = Q()

        for term in search_terms:
            q_search = Q(name__icontains=term)

            query &= q_search

        return (queryset.filter(query), Q())


@strawberry_django.type(Organization, order=OrganizationOrder, filters=OrganizationFilter)  # type: ignore[literal-required]
class OrganizationType:
    id: ID
    name: auto


@strawberry_django.type(User)
class UserBaseType:
    first_name: Optional[NonBlankString]
    last_name: Optional[NonBlankString]
    middle_name: Optional[NonBlankString]
    email: Optional[NonBlankString]


@strawberry_django.type(User)
class UserType(UserBaseType):
    # TODO: has_accepted_tos, has_accepted_privacy_policy, is_outreach_authorized shouldn't be optional.
    # Temporary fix while we figure out type generation
    id: ID
    has_accepted_tos: Optional[bool]
    has_accepted_privacy_policy: Optional[bool]
    is_outreach_authorized: Optional[bool]
    organizations_organization: Optional[List[OrganizationType]]
    username: auto


@strawberry_django.input(User, partial=True)
class CreateUserInput(UserBaseType):
    "See parent"


@strawberry_django.input(User, partial=True)
class UpdateUserInput(UserBaseType):
    id: ID
    has_accepted_tos: auto
    has_accepted_privacy_policy: auto

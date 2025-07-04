from typing import Any, Optional
from unittest import skip

import time_machine
from accounts.models import User
from accounts.tests.baker_recipes import permission_group_recipe
from deepdiff import DeepDiff
from django.test import ignore_warnings
from django.utils import timezone
from model_bakery import baker
from notes.enums import (
    DueByGroupEnum,
    SelahTeamEnum,
    ServiceEnum,
    ServiceRequestStatusEnum,
)
from notes.models import Note
from notes.tests.utils import (
    NoteGraphQLBaseTestCase,
    ServiceRequestGraphQLBaseTestCase,
    TaskGraphQLBaseTestCase,
)
from unittest_parametrize import parametrize


@ignore_warnings(category=UserWarning)
@time_machine.travel("2024-03-11T10:11:12+00:00", tick=False)
class NoteQueryTestCase(NoteGraphQLBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.graphql_client.force_login(self.org_1_case_manager_1)

    def test_note_query(self) -> None:
        note_id = self.note["id"]
        # Update fields available on the note input
        self._update_note_fixture(
            {
                "id": note_id,
                "interactedAt": "2024-03-12T11:12:13+00:00",
                "isSubmitted": False,
                "location": self.location.pk,
                "privateDetails": "Updated private details",
                "publicDetails": "Updated public details",
                "purpose": "Updated Note",
                "team": SelahTeamEnum.WDI_ON_SITE.name,
            }
        )
        # Add moods
        self._create_note_mood_fixture(
            {"descriptor": "ANXIOUS", "noteId": note_id},
        )
        self._create_note_mood_fixture(
            {"descriptor": "EUTHYMIC", "noteId": note_id},
        )
        # Add purposes and next steps
        note = Note.objects.get(pk=note_id)
        note.purposes.set([self.purpose_1["id"], self.purpose_2["id"]])
        note.next_steps.set([self.next_step_1["id"], self.next_step_2["id"]])
        note.provided_services.set(self.provided_services)
        note.requested_services.set(self.requested_services)

        query = f"""
            query ($id: ID!) {{
                note(pk: $id) {{
                    {self.note_fields}
                }}
            }}
        """

        variables = {"id": note_id}
        expected_query_count = 8

        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables)

        note = response["data"]["note"]
        expected_note = {
            "id": note_id,
            "clientProfile": {"id": str(self.client_profile_1.pk)},
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "interactedAt": "2024-03-12T11:12:13+00:00",
            "isSubmitted": False,
            "privateDetails": "Updated private details",
            "publicDetails": "Updated public details",
            "purpose": "Updated Note",
            "team": SelahTeamEnum.WDI_ON_SITE.name,
            "location": {
                "id": str(self.location.pk),
                "address": {
                    "street": self.address.street,
                    "city": self.address.city,
                    "state": self.address.state,
                    "zipCode": self.address.zip_code,
                },
                "point": self.point,
                "pointOfInterest": self.point_of_interest,
            },
            "moods": [{"descriptor": "ANXIOUS"}, {"descriptor": "EUTHYMIC"}],
            "purposes": [
                {"id": self.purpose_1["id"], "title": self.purpose_1["title"]},
                {"id": self.purpose_2["id"], "title": self.purpose_2["title"]},
            ],
            "nextSteps": [
                {"id": self.next_step_1["id"], "title": self.next_step_1["title"], "location": None},
                {"id": self.next_step_2["id"], "title": self.next_step_2["title"], "location": None},
            ],
            "providedServices": [
                {
                    "id": str(self.provided_services[0].id),
                    "service": ServiceEnum(self.provided_services[0].service).name,
                    "serviceOther": self.provided_services[0].service_other,
                    "dueBy": self.provided_services[0].due_by,
                    "status": ServiceRequestStatusEnum(self.provided_services[0].status).name,
                },
                {
                    "id": str(self.provided_services[1].id),
                    "service": ServiceEnum(self.provided_services[1].service).name,
                    "serviceOther": self.provided_services[1].service_other,
                    "dueBy": self.provided_services[1].due_by,
                    "status": ServiceRequestStatusEnum(self.provided_services[1].status).name,
                },
            ],
            "requestedServices": [
                {
                    "id": str(self.requested_services[0].id),
                    "service": ServiceEnum(self.requested_services[0].service).name,
                    "serviceOther": self.requested_services[0].service_other,
                    "dueBy": self.requested_services[0].due_by,
                    "status": ServiceRequestStatusEnum(self.requested_services[0].status).name,
                },
                {
                    "id": str(self.requested_services[1].id),
                    "service": ServiceEnum(self.requested_services[1].service).name,
                    "serviceOther": self.requested_services[1].service_other,
                    "dueBy": self.requested_services[1].due_by,
                    "status": ServiceRequestStatusEnum(self.requested_services[1].status).name,
                },
            ],
        }
        note_differences = DeepDiff(expected_note, note, ignore_order=True)
        self.assertFalse(note_differences)

    def test_notes_query(self) -> None:
        query = f"""
            query ($offset: Int, $limit: Int) {{
                notes(pagination: {{offset: $offset, limit: $limit}}) {{
                    totalCount
                    pageInfo {{
                        limit
                        offset
                    }}
                    results {{
                        {self.note_fields}
                    }}
                }}
            }}
        """
        expected_query_count = 9
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables={"offset": 0, "limit": 10})

        self.assertEqual(response["data"]["notes"]["totalCount"], 1)
        self.assertEqual(response["data"]["notes"]["pageInfo"], {"limit": 10, "offset": 0})

        notes = response["data"]["notes"]["results"]
        # TODO: Add more validations once sort is implemented
        note_differences = DeepDiff(self.note, notes[0], ignore_order=True)
        self.assertFalse(note_differences)

    def test_interaction_authors(self) -> None:
        query = """
            query ViewInteractionAuthors {
                interactionAuthors {
                    totalCount
                    results {
                        id
                        firstName
                        lastName
                        middleName
                    }
                }
            }
        """

        interaction_author = baker.make(
            User,
            first_name="Wanda",
            last_name="Maximoff",
            middle_name="J.",
        )

        perm_group = permission_group_recipe.make()
        perm_group.organization.add_user(interaction_author)

        response = self.execute_graphql(query)

        results = response["data"]["interactionAuthors"]["results"]
        returned_author: dict = next((u for u in results if u["id"] == str(interaction_author.pk)))
        self.assertEqual(returned_author["firstName"], "Wanda")
        self.assertEqual(returned_author["lastName"], "Maximoff")
        self.assertEqual(returned_author["middleName"], "J.")

    @parametrize(
        ("case_manager_labels, client_label, org_labels, is_submitted, expected_results_count, returned_note_labels"),
        [
            # Filter by:
            # created by, client_label, and/or is_submitted
            (
                ["org_1_case_manager_1", "org_1_case_manager_2"],
                None,
                None,
                None,
                2,
                ["note", "note_2"],
            ),  # CM 1 created one note
            (["org_2_case_manager_1"], None, None, True, 1, ["note_3"]),  # Org 2 CM 1 submitted 1 note
            (["org_1_case_manager_2"], None, None, False, 1, ["note_2"]),  # CM 2 has one unsubmitted note
            (["org_1_case_manager_1"], "client_profile_2", None, None, 0, []),  # CM 1 has no notes for client 2
            # CM 1 has one unsubmitted note for client 1
            (["org_1_case_manager_1"], "client_profile_1", [], False, 1, ["note"]),
            ([], None, ["org_2"], True, 1, ["note_3"]),  # There is one submitted note from org 2
            (
                None,
                None,
                ["org_1", "org_2"],
                None,
                3,
                ["note", "note_2", "note_3"],
            ),  # Orgs 1 and 2 have authored three notes
        ],
    )
    def test_notes_query_filter(
        self,
        case_manager_labels: Optional[list[str]],
        client_label: Optional[str],
        org_labels: Optional[str],
        is_submitted: Optional[bool],
        expected_results_count: int,
        returned_note_labels: list[str],
    ) -> None:
        self.graphql_client.force_login(self.org_1_case_manager_2)
        # self.note is created in the setup block by self.org_1_case_manager_1 for self.client_profile_1
        self.note_2 = self._create_note_fixture(
            {"purpose": "Client 1's Note", "clientProfile": self.client_profile_1.pk}
        )["data"]["createNote"]
        self.graphql_client.logout()
        self.graphql_client.force_login(self.org_2_case_manager_1)
        self.note_3 = self._create_note_fixture(
            {"purpose": "Client 2's Note", "clientProfile": self.client_profile_2.pk}
        )["data"]["createNote"]
        self._update_note_fixture(
            {
                "id": self.note_3["id"],
                "isSubmitted": True,
            }
        )

        query = """
            query Notes($filters: NoteFilter) {
                notes(filters: $filters) {
                    totalCount
                    results{
                        id
                    }
                }
            }
        """

        filters: dict[str, Any] = {}

        if case_manager_labels is not None:
            filters["authors"] = [self.user_map[label].pk for label in case_manager_labels]

        if client_label:
            filters["clientProfile"] = getattr(self, client_label).pk

        if org_labels:
            filters["organizations"] = [getattr(self, org_label).pk for org_label in org_labels]

        if isinstance(is_submitted, bool):
            filters["isSubmitted"] = is_submitted

        expected_query_count = 4
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables={"filters": filters})

        self.assertEqual(response["data"]["notes"]["totalCount"], expected_results_count)
        notes = response["data"]["notes"]["results"]

        for idx, note_label in enumerate(returned_note_labels):
            self.assertEqual(notes[idx]["id"], getattr(self, note_label)["id"])

    @parametrize(
        ("authors, expected_results_count, returned_note_labels, expected_query_count"),
        [
            ([], 3, ["note", "note_2", "note_3"], 4),
            (["org_1_case_manager_1"], 1, ["note"], 4),
            (["org_1_case_manager_2"], 2, ["note_2", "note_3"], 4),
            (["org_2_case_manager_1"], 0, [], 4),
            (["org_1_case_manager_2", "org_2_case_manager_1"], 2, ["note_2", "note_3"], 4),
        ],
    )
    def test_notes_query_filter_by_authors(
        self,
        authors: list[SelahTeamEnum],
        expected_results_count: int,
        returned_note_labels: list[str],
        expected_query_count: int,
    ) -> None:
        self.graphql_client.force_login(self.org_1_case_manager_2)
        # self.note is created in the setup block by self.org_1_case_manager_1 for self.client_profile_1
        self.note_2 = self._create_note_fixture(
            {
                "purpose": "Client 1's Note",
                "clientProfile": self.client_profile_1.pk,
            }
        )["data"]["createNote"]
        self.note_3 = self._create_note_fixture(
            {
                "purpose": "Client 2's Note",
                "clientProfile": self.client_profile_2.pk,
            }
        )["data"]["createNote"]

        filters = {"authors": [self.user_map[author].pk for author in authors]}

        query = """
            query ($filters: NoteFilter) {
                notes(filters: $filters) {
                    totalCount
                    results{
                        id
                    }
                }
            }
        """

        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables={"filters": filters})

        self.assertEqual(response["data"]["notes"]["totalCount"], expected_results_count)
        notes = response["data"]["notes"]["results"]

        for idx, note_label in enumerate(returned_note_labels):
            self.assertEqual(notes[idx]["id"], getattr(self, note_label)["id"])

    @parametrize(
        ("teams, expected_results_count, returned_note_labels, expected_query_count"),
        [
            ([], 3, ["note", "note_2", "note_3"], 4),
            ([SelahTeamEnum.WDI_ON_SITE.name, SelahTeamEnum.SLCC_ON_SITE.name], 2, ["note_2", "note_3"], 4),
            ([SelahTeamEnum.SLCC_ON_SITE.name], 1, ["note_3"], 4),
            ([SelahTeamEnum.WDI_ON_SITE.name, "invalid team"], 0, [], 1),
        ],
    )
    def test_notes_query_filter_by_teams(
        self,
        teams: list[SelahTeamEnum],
        expected_results_count: int,
        returned_note_labels: list[str],
        expected_query_count: int,
    ) -> None:
        self.graphql_client.force_login(self.org_1_case_manager_2)
        # self.note is created in the setup block by self.org_1_case_manager_1 for self.client_profile_1
        self.note_2 = self._create_note_fixture(
            {
                "purpose": "Client 1's Note",
                "clientProfile": self.client_profile_1.pk,
            }
        )["data"]["createNote"]
        self.note_3 = self._create_note_fixture(
            {
                "purpose": "Client 2's Note",
                "clientProfile": self.client_profile_2.pk,
            }
        )["data"]["createNote"]
        self._update_note_fixture(
            {
                "id": self.note_2["id"],
                "team": SelahTeamEnum.WDI_ON_SITE.name,
            }
        )
        self._update_note_fixture(
            {
                "id": self.note_3["id"],
                "team": SelahTeamEnum.SLCC_ON_SITE.name,
            }
        )

        filters = {"teams": teams}

        query = """
            query Notes($filters: NoteFilter) {
                notes(filters: $filters) {
                    totalCount
                    results{
                        id
                    }
                }
            }
        """

        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables={"filters": filters})

        if "invalid team" in teams:
            self.assertIsNone(response["data"])
            self.assertEqual(len(response["errors"]), 1)
            self.assertIn("does not exist in 'SelahTeamEnum'", response["errors"][0]["message"])

        else:
            self.assertEqual(response["data"]["notes"]["totalCount"], expected_results_count)
            notes = response["data"]["notes"]["results"]

            for idx, note_label in enumerate(returned_note_labels):
                self.assertEqual(notes[idx]["id"], getattr(self, note_label)["id"])

    @parametrize(
        ("name_search, expected_results_count, expected_authors"),
        [
            ("Maximoff", 1, ["interaction_author_2"]),
            ("Pietro Maximoff", 0, None),
            ("Alex", 2, ["interaction_author", "interaction_author_3"]),
        ],
    )
    def test_interaction_authors_filter(
        self,
        name_search: Optional[str],
        expected_results_count: int,
        expected_authors: Optional[list[str]],
    ) -> None:
        self.graphql_client.force_login(self.org_1_case_manager_2)

        baker.make(User, first_name="Alex", last_name="Johnson")

        test_user_map = {
            "interaction_author": baker.make(User, first_name="Alexa", last_name="Danvers", middle_name="J."),
            "interaction_author_2": baker.make(User, first_name="Wanda", last_name="Maximoff", middle_name="A."),
            "interaction_author_3": baker.make(User, first_name="Alexandria", last_name="Daniels", middle_name="M."),
        }

        interaction_author = test_user_map["interaction_author"]
        interaction_author_2 = test_user_map["interaction_author_2"]
        interaction_author_3 = test_user_map["interaction_author_3"]

        perm_group = permission_group_recipe.make()
        perm_group.organization.add_user(interaction_author)
        perm_group.organization.add_user(interaction_author_2)
        perm_group.organization.add_user(interaction_author_3)

        query = """
            query InteractionAuthors($filters: InteractionAuthorFilter) {
                interactionAuthors(filters: $filters) {
                    totalCount
                    results {
                        id
                    }
                }
            }
        """

        filters: dict[str, Any] = {"search": name_search}

        response = self.execute_graphql(query, variables={"filters": filters})

        self.assertEqual(response["data"]["interactionAuthors"]["totalCount"], expected_results_count)
        authors = response["data"]["interactionAuthors"]["results"]

        if expected_authors:
            author_ids = set([int(u["id"]) for u in authors])
            expected_authors_ids = set([test_user_map[u].pk for u in expected_authors])
            self.assertEqual(author_ids, expected_authors_ids, f"Not equal, {author_ids, expected_authors_ids}")

    @parametrize(
        ("search_terms, expected_results_count, returned_note_labels"),
        [
            ("deets", 2, ["note_2", "note_3"]),  # Two notes have "deets" in public details
            ("deets coop", 1, ["note_2"]),  # One note has "deets" in public details and "coop" in client name
            ("more", 1, ["note_3"]),  # One note has "more" in public details
        ],
    )
    def test_notes_query_search(
        self,
        search_terms: Optional[str],
        expected_results_count: int,
        returned_note_labels: list[str],
    ) -> None:
        self.graphql_client.force_login(self.org_1_case_manager_2)
        # self.note is created in the setup block by self.org_1_case_manager_1 for self.client_profile_1
        self.note_2 = self._create_note_fixture(
            {
                "purpose": "Client 1's Note",
                "publicDetails": "deets",
                "clientProfile": self.client_profile_1.pk,
            }
        )["data"]["createNote"]
        self.note_3 = self._create_note_fixture(
            {
                "purpose": "Client 2's Note",
                "publicDetails": "more deets",
                "clientProfile": self.client_profile_2.pk,
            }
        )["data"]["createNote"]

        query = """
            query Notes($filters: NoteFilter) {
                notes(filters: $filters) {
                    totalCount
                    results{
                        id
                    }
                }
            }
        """

        filters: dict[str, Any] = {"search": search_terms}

        expected_query_count = 4
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables={"filters": filters})

        self.assertEqual(response["data"]["notes"]["totalCount"], expected_results_count)
        notes = response["data"]["notes"]["results"]

        for idx, note_label in enumerate(returned_note_labels):
            self.assertEqual(notes[idx]["id"], getattr(self, note_label)["id"])

    def test_notes_query_order(self) -> None:
        """
        Assert that notes are returned in order of interacted_at timestamp, regardless of client
        """
        self.graphql_client.force_login(self.org_1_case_manager_2)

        older_note = self._create_note_fixture(
            {
                "purpose": "Client 1's Note",
                "clientProfile": self.client_profile_1.pk,
            }
        )["data"]["createNote"]
        self._update_note_fixture({"id": older_note["id"], "interactedAt": "2024-03-10T10:11:12+00:00"})

        oldest_note = self._create_note_fixture(
            {
                "purpose": "Client 2's Note",
                "clientProfile": self.client_profile_2.pk,
            }
        )["data"]["createNote"]
        self._update_note_fixture({"id": oldest_note["id"], "interactedAt": "2024-01-10T10:11:12+00:00"})

        query = """
            query Notes($order: NoteOrder) {
                notes(order: $order) {
                    results{
                        id
                    }
                }
            }
        """

        # Test descending order
        expected_query_count = 3
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables={"order": {"interactedAt": "DESC"}})

        self.assertEqual(
            [n["id"] for n in response["data"]["notes"]["results"]],
            [self.note["id"], older_note["id"], oldest_note["id"]],
        )

        # Test ascending order
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables={"order": {"interactedAt": "ASC"}})

        self.assertEqual(
            [n["id"] for n in response["data"]["notes"]["results"]],
            [oldest_note["id"], older_note["id"], self.note["id"]],
        )


@skip("Service Requests are not currently implemented")
@ignore_warnings(category=UserWarning)
@time_machine.travel("2024-03-11T10:11:12+00:00", tick=False)
class ServiceRequestQueryTestCase(ServiceRequestGraphQLBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.graphql_client.force_login(self.org_1_case_manager_1)

    def test_service_request_query(self) -> None:
        service_request_id = self.service_request["id"]
        self._update_service_request_fixture(
            {
                "id": service_request_id,
                "status": "COMPLETED",
            }
        )

        query = """
            query ($id: ID!) {
                serviceRequest(pk: $id) {
                    id
                    service
                    serviceOther
                    status
                    dueBy
                    completedOn
                    clientProfile {
                        id
                    }
                    createdBy {
                        id
                    }
                    createdAt
                }
            }
        """
        variables = {"id": service_request_id}

        expected_query_count = 3
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables)

        service_request = response["data"]["serviceRequest"]
        expected_service_request = {
            "id": service_request_id,
            "service": self.service_request["service"],
            "serviceOther": None,
            "status": "COMPLETED",
            "dueBy": None,
            "completedOn": "2024-03-11T10:11:12+00:00",
            "clientProfile": None,
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": "2024-03-11T10:11:12+00:00",
        }

        self.assertEqual(service_request, expected_service_request)

    def test_service_requests_query(self) -> None:
        query = """
            {
                serviceRequests {
                    id
                    service
                    serviceOther
                    status
                    dueBy
                    completedOn
                    clientProfile {
                        id
                    }
                    createdBy {
                        id
                    }
                    createdAt
                }
            }
        """
        expected_query_count = 3
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query)

        service_requests = response["data"]["serviceRequests"]
        self.assertEqual(len(service_requests), 1)
        self.assertEqual(service_requests[0], self.service_request)


@skip("Tasks are not currently implemented")
@ignore_warnings(category=UserWarning)
@time_machine.travel("2024-03-11T10:11:12+00:00", tick=False)
class TaskQueryTestCase(TaskGraphQLBaseTestCase):
    def setUp(self) -> None:
        super().setUp()
        self.graphql_client.force_login(self.org_1_case_manager_1)

    def test_task_query(self) -> None:
        task_id = self.task["id"]
        # Update fields available on the task input
        self._update_task_fixture(
            {
                "id": task_id,
                "title": "Updated task title",
                "location": self.location.pk,
                "status": "COMPLETED",
                "dueBy": timezone.now(),
            }
        )

        query = f"""
            query ($id: ID!) {{
                task(pk: $id) {{
                    {self.task_fields}
                }}
            }}
        """
        variables = {"id": task_id}

        expected_query_count = 3
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query, variables)

        task = response["data"]["task"]
        expected_task = {
            "id": task_id,
            "title": "Updated task title",
            "location": {
                "id": str(self.location.pk),
                "address": {
                    "street": self.address.street,
                    "city": self.address.city,
                    "state": self.address.state,
                    "zipCode": self.address.zip_code,
                },
                "point": self.point,
                "pointOfInterest": self.point_of_interest,
            },
            "status": "COMPLETED",
            "dueBy": "2024-03-11T10:11:12+00:00",
            "dueByGroup": DueByGroupEnum.TODAY.name,
            "clientProfile": None,
            "createdBy": {"id": str(self.org_1_case_manager_1.pk)},
            "createdAt": "2024-03-11T10:11:12+00:00",
        }

        self.assertEqual(task, expected_task)

    def test_tasks_query(self) -> None:
        query = f"""
            tasks {{
                {self.task_fields}
            }}
        """
        expected_query_count = 1
        with self.assertNumQueriesWithoutCache(expected_query_count):
            response = self.execute_graphql(query)

        tasks = response["data"]["tasks"]
        self.assertEqual(len(tasks), 1)
        self.assertEqual(tasks[0], self.task)

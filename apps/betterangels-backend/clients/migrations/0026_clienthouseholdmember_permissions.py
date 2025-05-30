# Generated by Django 5.1.7 on 2025-03-28 15:32

from clients.permissions import ClientHouseholdMemberPermissions
from django.db import migrations


def create_permissions_if_not_exist(apps, schema_editor):
    ClientHouseholdMember = apps.get_model("clients", "ClientHouseholdMember")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    ClientHouseholdMemberContentType = ContentType.objects.get_for_model(ClientHouseholdMember)
    db_alias = schema_editor.connection.alias

    # Generate readable names based on the enum
    PERM_MAP = {perm.split(".")[1]: perm.label for perm in ClientHouseholdMemberPermissions}
    for codename, name in PERM_MAP.items():
        Permission.objects.using(db_alias).get_or_create(
            codename=codename,
            content_type=ClientHouseholdMemberContentType,
            defaults={"name": name, "content_type": ClientHouseholdMemberContentType},
        )


def update_caseworker_permission_template(apps, schema_editor):
    PermissionGroupTemplate = apps.get_model("accounts", "PermissionGroupTemplate")
    Permission = apps.get_model("auth", "Permission")
    ContentType = apps.get_model("contenttypes", "ContentType")
    ClientHouseholdMember = apps.get_model("clients", "ClientHouseholdMember")
    ClientHouseholdMemberContentType = ContentType.objects.get_for_model(ClientHouseholdMember)
    caseworker_template = PermissionGroupTemplate.objects.get(name="Caseworker")

    perm_map = [
        perm.split(".")[1]
        for perm in [
            "clients.add_clienthouseholdmember",
            "clients.view_clienthouseholdmember",
            "clients.change_clienthouseholdmember",
            "clients.delete_clienthouseholdmember",
        ]
    ]

    permissions = Permission.objects.filter(codename__in=perm_map, content_type=ClientHouseholdMemberContentType)
    caseworker_template.permissions.add(*permissions)


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0025_alter_clientprofile_user_and_more"),
    ]

    operations = [
        migrations.RunPython(create_permissions_if_not_exist),
        migrations.RunPython(update_caseworker_permission_template),
    ]

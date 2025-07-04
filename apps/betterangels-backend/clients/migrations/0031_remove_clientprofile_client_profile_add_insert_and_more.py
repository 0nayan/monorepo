# Generated by Django 5.2.3 on 2025-06-24 19:20

import pgtrigger.compiler
import pgtrigger.migrations
from django.db import migrations


class Migration(migrations.Migration):

    dependencies = [
        ("clients", "0030_remove_clientprofile_client_profile_add_insert_and_more"),
        ("notes", "0016_note_client_profile_data"),
    ]

    operations = [
        pgtrigger.migrations.RemoveTrigger(
            model_name="clientprofile",
            name="client_profile_add_insert",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="clientprofile",
            name="client_profile_update_update",
        ),
        pgtrigger.migrations.RemoveTrigger(
            model_name="clientprofile",
            name="client_profile_remove_delete",
        ),
        migrations.RemoveField(
            model_name="clientprofile",
            name="user",
        ),
        migrations.RemoveField(
            model_name="clientprofileevent",
            name="user",
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="clientprofile",
            trigger=pgtrigger.compiler.Trigger(
                name="client_profile_add_insert",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "clients_clientprofileevent" ("ada_accommodation", "address", "california_id", "created_at", "date_of_birth", "email", "eye_color", "first_name", "gender", "gender_other", "hair_color", "height_in_inches", "id", "important_notes", "last_name", "living_situation", "mailing_address", "marital_status", "middle_name", "nickname", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "phone_number", "physical_description", "place_of_birth", "preferred_communication", "preferred_language", "profile_photo", "pronouns", "pronouns_other", "race", "residence_address", "residence_geolocation", "spoken_languages", "updated_at", "veteran_status") VALUES (NEW."ada_accommodation", NEW."address", NEW."california_id", NEW."created_at", NEW."date_of_birth", NEW."email", NEW."eye_color", NEW."first_name", NEW."gender", NEW."gender_other", NEW."hair_color", NEW."height_in_inches", NEW."id", NEW."important_notes", NEW."last_name", NEW."living_situation", NEW."mailing_address", NEW."marital_status", NEW."middle_name", NEW."nickname", _pgh_attach_context(), NOW(), \'client_profile.add\', NEW."id", NEW."phone_number", NEW."physical_description", NEW."place_of_birth", NEW."preferred_communication", NEW."preferred_language", NEW."profile_photo", NEW."pronouns", NEW."pronouns_other", NEW."race", NEW."residence_address", NEW."residence_geolocation", NEW."spoken_languages", NEW."updated_at", NEW."veteran_status"); RETURN NULL;',
                    hash="ba4b7e0a04fe0a2cabc3c0f83f6069ca499db57d",
                    operation="INSERT",
                    pgid="pgtrigger_client_profile_add_insert_4c2ed",
                    table="clients_clientprofile",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="clientprofile",
            trigger=pgtrigger.compiler.Trigger(
                name="client_profile_update_update",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    condition="WHEN (OLD.* IS DISTINCT FROM NEW.*)",
                    func='INSERT INTO "clients_clientprofileevent" ("ada_accommodation", "address", "california_id", "created_at", "date_of_birth", "email", "eye_color", "first_name", "gender", "gender_other", "hair_color", "height_in_inches", "id", "important_notes", "last_name", "living_situation", "mailing_address", "marital_status", "middle_name", "nickname", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "phone_number", "physical_description", "place_of_birth", "preferred_communication", "preferred_language", "profile_photo", "pronouns", "pronouns_other", "race", "residence_address", "residence_geolocation", "spoken_languages", "updated_at", "veteran_status") VALUES (NEW."ada_accommodation", NEW."address", NEW."california_id", NEW."created_at", NEW."date_of_birth", NEW."email", NEW."eye_color", NEW."first_name", NEW."gender", NEW."gender_other", NEW."hair_color", NEW."height_in_inches", NEW."id", NEW."important_notes", NEW."last_name", NEW."living_situation", NEW."mailing_address", NEW."marital_status", NEW."middle_name", NEW."nickname", _pgh_attach_context(), NOW(), \'client_profile.update\', NEW."id", NEW."phone_number", NEW."physical_description", NEW."place_of_birth", NEW."preferred_communication", NEW."preferred_language", NEW."profile_photo", NEW."pronouns", NEW."pronouns_other", NEW."race", NEW."residence_address", NEW."residence_geolocation", NEW."spoken_languages", NEW."updated_at", NEW."veteran_status"); RETURN NULL;',
                    hash="f88a26e1379be4523d9b8ac8319b8c53a336af73",
                    operation="UPDATE",
                    pgid="pgtrigger_client_profile_update_update_858fb",
                    table="clients_clientprofile",
                    when="AFTER",
                ),
            ),
        ),
        pgtrigger.migrations.AddTrigger(
            model_name="clientprofile",
            trigger=pgtrigger.compiler.Trigger(
                name="client_profile_remove_delete",
                sql=pgtrigger.compiler.UpsertTriggerSql(
                    func='INSERT INTO "clients_clientprofileevent" ("ada_accommodation", "address", "california_id", "created_at", "date_of_birth", "email", "eye_color", "first_name", "gender", "gender_other", "hair_color", "height_in_inches", "id", "important_notes", "last_name", "living_situation", "mailing_address", "marital_status", "middle_name", "nickname", "pgh_context_id", "pgh_created_at", "pgh_label", "pgh_obj_id", "phone_number", "physical_description", "place_of_birth", "preferred_communication", "preferred_language", "profile_photo", "pronouns", "pronouns_other", "race", "residence_address", "residence_geolocation", "spoken_languages", "updated_at", "veteran_status") VALUES (OLD."ada_accommodation", OLD."address", OLD."california_id", OLD."created_at", OLD."date_of_birth", OLD."email", OLD."eye_color", OLD."first_name", OLD."gender", OLD."gender_other", OLD."hair_color", OLD."height_in_inches", OLD."id", OLD."important_notes", OLD."last_name", OLD."living_situation", OLD."mailing_address", OLD."marital_status", OLD."middle_name", OLD."nickname", _pgh_attach_context(), NOW(), \'client_profile.remove\', OLD."id", OLD."phone_number", OLD."physical_description", OLD."place_of_birth", OLD."preferred_communication", OLD."preferred_language", OLD."profile_photo", OLD."pronouns", OLD."pronouns_other", OLD."race", OLD."residence_address", OLD."residence_geolocation", OLD."spoken_languages", OLD."updated_at", OLD."veteran_status"); RETURN NULL;',
                    hash="8687d7c87da92660251e9f467a0cec853f8a53c2",
                    operation="DELETE",
                    pgid="pgtrigger_client_profile_remove_delete_ade5a",
                    table="clients_clientprofile",
                    when="AFTER",
                ),
            ),
        ),
    ]

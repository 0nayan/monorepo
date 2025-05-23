import strawberry
from django.db import models
from django.utils.translation import gettext_lazy as _


class MoodEnum(models.TextChoices):
    AGITATED = "agitated", _("Agitated")
    AGREEABLE = "agreeable", _("Agreeable")
    ANXIOUS = "anxious", _("Anxious")
    DEPRESSED = "depressed", _("Depressed")
    DETACHED = "detached", _("Detached")
    DISORGANIZED_THOUGHT = "disorganized_thought", _("Disorganized Thought")
    DISORIENTED = "disoriented", _("Disoriented")
    ESCALATED = "escalated", _("Escalated")
    EUTHYMIC = "euthymic", _("Euthymic")
    FLAT_BLUNTED = "flat_blunted", _("Flat/blunted")
    HAPPY = "happy", _("Happy")
    HOPELESS = "hopeless", _("Hopeless")
    INDIFFERENT = "indifferent", _("Indifferent")
    MANIC = "manic", _("Manic")
    MOTIVATED = "motivated", _("Motivated")
    OPTIMISTIC = "optimistic", _("Optimistic")
    PERSONABLE = "personable", _("Personable")
    PLEASANT = "pleasant", _("Pleasant")
    RESTLESS = "restless", _("Restless")
    SUICIDAL = "suicidal", _("Suicidal")


class ServiceEnum(models.TextChoices):
    BAG = "bag", _("Bag(s)")
    BATTERIES = "batteries", _("Batteries")
    BICYCLE = "bicycle", _("Bicycle")
    BICYCLE_REPAIR = "bicycle_repair", _("Bicycle Repair")
    BIRTH_CERTIFICATE = "birth_certificate", _("Birth Certificate")
    BLANKET = "blanket", _("Blanket")
    BOOK = "book", _("Book")
    CALIFORNIA_LIFELINE_PHONE = "california_lifeline_phone", _("California Lifeline Phone")
    CLOTHES = "clothes", _("Clothes")
    CONSENT_TO_CONNECT = "consent_to_connect", _("Consent to Connect (CM or Council District)")
    CONTACT_DPSS = "contact_dpss", _("Contact DPSS")
    CONTACT_FRIEND = "contact_friend", _("Contact Friend")
    DENTAL = "dental", _("Dental")
    DISCOUNT_SCOOTER_RIDES = "discount_scooter_rides", _("Discount Scooter Rides")
    DMH_EVALUATION = "dmh_evaluation", _("DMH Evaluation")
    DMV_NO_FEE_ID_FORM = "dmv_no_fee_id_form", _("DMV No Fee ID Form")
    EBT = "ebt", _("EBT")
    FAMILY_REUNIFICATION = "family_reunification", _("Family Reunification")
    FEMININE_HYGIENE = "feminine_hygiene", _("Feminine Hygiene")
    FIRST_AID = "first_aid", _("First Aid")
    FOOD = "food", _("Food")
    HARM_REDUCTION = "harm_reduction", _("Harm Reduction")
    HMIS_CONSENT = "hmis_consent", _("HMIS Consent")
    HYGIENE_KIT = "hygiene_kit", _("Hygiene Kit")
    INTERNET_ACCESS = "internet_access", _("Internet Access")
    LAHOP = "lahop", _("LAHOP")
    LEGAL_COUNSEL = "legal_counsel", _("Legal Counsel")
    MAIL_PICK_UP = "mail_pick_up", _("Mail Pick Up")
    MEDICAL = "medical", _("Medical")
    MEDI_CAL = "medi_cal", _("Medi-Cal")
    METRO_LIFE_TAP = "metro_life_tap", _("Metro LIFE Tap")
    NOTARY = "notary", _("Notary")
    OTHER = "other", _("Other")
    PET_CARE = "pet_care", _("Pet Care")
    PET_FOOD = "pet_food", _("Pet Food")
    PUBLIC_BENEFITS_PROGRAMS = "public_benefits_programs", _("Public Benefits Programs")
    RIDE = "ride", _("Ride")
    SAFE_PARKING = "safe_parking", _("Safe Parking")
    SHELTER = "shelter", _("Shelter")
    SHOES = "shoes", _("Shoes")
    SHOWER = "shower", _("Shower")
    SLEEPING_BAG = "sleeping_bag", _("Sleeping Bag")
    SOCIAL_SECURITY_CARD_REPLACEMENT = "social_security_card_replacement", _("Social Security Card Replacement")
    SSI_SSDI = "ssi_ssdi", _("SSI/SSDI")
    STABILIZE = "stabilize", _("Stabilize")  # TODO: remove once fe has been updated
    STIMULUS_ASSISTANCE = "stimulus_assistance", _("Stimulus Assistance")
    STORAGE = "storage", _("Storage")  # TODO: remove once fe has been updated
    STORAGE_BELONGINGS = "storage_belongings", _("Storage - Belongings")
    STORAGE_DOCUMENTS = "storage_documents", _("Storage - Documents")
    TARP = "tarp", _("Tarp")
    TENT = "tent", _("Tent")
    THERAPIST_APPOINTMENT = "therapist_appointment", _("Therapist Appointment")
    TRANSPORT = "transport", _("Transport")  # TODO: remove once fe has been updated
    UNEMPLOYMENT_CERTIFICATION = "unemployment_certification", _("Unemployment Certification")
    VACCINE_PASSPORT = "vaccine_passport", _("Vaccine Passport")
    WATER = "water", _("Water")


class TaskStatusEnum(models.TextChoices):
    COMPLETED = "completed", _("Completed")
    TO_DO = "to_do", _("To Do")


class ServiceRequestStatusEnum(models.TextChoices):
    COMPLETED = "completed", _("Completed")
    TO_DO = "to_do", _("To Do")


@strawberry.enum
class TaskTypeEnum(models.TextChoices):
    PURPOSE = "purpose", "Purpose"
    NEXT_STEP = "next_step", "Next Step"


@strawberry.enum
class ServiceRequestTypeEnum(models.TextChoices):
    PROVIDED = "provided", "Provided"
    REQUESTED = "requested", "Requested"


@strawberry.enum
class DueByGroupEnum(models.TextChoices):
    OVERDUE = "overdue", _("Overdue")
    TODAY = "today", _("Today")
    TOMORROW = "tomorrow", _("Tomorrow")
    IN_THE_NEXT_WEEK = "in_the_next_week", _("In the next week")
    FUTURE_TASKS = "future_tasks", _("Future tasks")
    NO_DUE_DATE = "no_due_date", _("No due date")


@strawberry.enum
class SelahTeamEnum(models.TextChoices):
    BOWTIE_RIVERSIDE_OUTREACH = "bowtie_riverside_outreach", _("Bowtie & Riverside Outreach")
    ECHO_PARK_ON_SITE = "echo_park_on_site", _("Echo Park On-site")
    ECHO_PARK_OUTREACH = "echo_park_outreach", _("Echo Park Outreach")
    HOLLYWOOD_ON_SITE = "hollywood_on_site", _("Hollywood On-site")
    HOLLYWOOD_OUTREACH = "hollywood_outreach", _("Hollywood Outreach")
    LA_RIVER_OUTREACH = "la_river_outreach", _("LA River Outreach")
    LOS_FELIZ_OUTREACH = "los_feliz_outreach", _("Los Feliz Outreach")
    NORTHEAST_HOLLYWOOD_OUTREACH = "northeast_hollywood_outreach", _("Northeast Hollywood Outreach")
    SILVER_LAKE_OUTREACH = "silver_lake_outreach", _("Silver Lake Outreach")
    SLCC_ON_SITE = "slcc_on_site", _("SLCC On-site")
    SUNDAY_SOCIAL_ATWATER_ON_SITE = "sunday_social_atwater_on_site", _("Sunday Social / Atwater On-site")
    SUNDAY_SOCIAL_ATWATER_OUTREACH = "sunday_social_atwater_outreach", _("Sunday Social / Atwater Outreach")
    WDI_ON_SITE = "wdi_on_site", _("WDI On-site")
    WDI_OUTREACH = "wdi_outreach", _("WDI Outreach")

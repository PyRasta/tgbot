from enum import Enum


class CallbackDataEnum(Enum):
    CREATE_NEWSLETTER = "create_newsletter"
    VIEW_USERS = "view_users"
    VIEW_PLAIN_NEWSLETTERS = "view_plain_newsletters"
    SAVE_AND_SEND_NEWSLETTER = "save_and_send_newsletter"
    SETUP_DATETIME_FOR_NEWSLETTER = "setup_datetime_for_newsletter"
    CHANGE_ROLE = "change_role"

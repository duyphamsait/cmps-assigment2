from utils.data_services import DataServices
from models.role import role_features, Role
import random

MAX_SEND_ATTEMPTS = 3

# Colors
GREEN = "\033[92m"
RED = "\033[91m"
YELLOW = "\033[93m"
BLUE = "\033[96m"
RESET = "\033[0m"

# add color to text
def color_text(text, color):
    return color + text + RESET

# get role name (handle enum or string)
def get_role_name(role):
    if isinstance(role, Role):
        return role.value
    return str(role)

# get permissions based on role
def get_permissions(role):
    role_name = get_role_name(role)

    if role_name == "admin":
        return [f.value for f in role_features.get(Role.ADMIN, [])]

    if role_name == "editor":
        return [f.value for f in role_features.get(Role.EDITOR, [])]

    if role_name == "viewer":
        return [f.value for f in role_features.get(Role.VIEWER, [])]

    return []

# create notification message
# def generate_notification(user_dict):

#     # get role and subscription
#     role = user_dict["role"].capitalize()
#     subscription = user_dict["subscription"]

#     if subscription == "premium":
#         tier = color_text("Premium", BLUE)
#     else:
#         tier = color_text("Free", GREEN)

#     return tier + " " + role + " notification was sent"

def generate_notification(user_dict):

    # get role and subscription
    role = user_dict.get("role")
    subscription = user_dict.get("subscription")

    # check missing data
    if role is None or subscription is None:
        return "Invalid notification data"

    # check if user is active
    if not user_dict.get("active"):
        return "User is not active"

    # check if user is logged in
    if not user_dict.get("logged_in"):
        return "User must be logged in"

    # check subscription is valid
    if subscription not in ["free", "premium"]:
        return "Invalid subscription"

    # format role name
    role = str(role).capitalize()

    # choose message based on subscription
    if subscription == "premium":
        tier = color_text("Premium", BLUE)
    else:
        tier = color_text("Free", GREEN)

    # return final message
    return tier + " " + role + " notification was sent"


# check if user can receive notification
def is_user_eligible(user_dict):
    # check active
    if user_dict["active"] == False:
        return False, color_text("Skipped", YELLOW) + ": inactive user"

    # check login
    if user_dict["logged_in"] == False:
        return False, color_text("Skipped", YELLOW) + ": not logged in"

    # check role
    if user_dict["role"] not in ["admin", "editor", "viewer"]:
        return False, color_text("Skipped", YELLOW) + ": invalid role"

    # check subscription
    if user_dict["subscription"] not in ["free", "premium"]:
        return False, color_text("Skipped", YELLOW) + ": invalid subscription"

    # check permissions
    if len(user_dict["permissions"]) == 0:
        return False, color_text("Skipped", YELLOW) + ": no permissions"

    return True, "Eligible"


# try sending notification
def send_notification(message):

    attempts = ["-", "-", "-"]

    for i in range(MAX_SEND_ATTEMPTS):
        # Simulate random success or failure for sent attempts.
        success = random.choice([True, False])

        if success:
            attempts[i] = "OK"
            return attempts, message
        else:
            attempts[i] = "Error"

    return attempts, "Failed after 3 attempts"


def color_attempt(value):

    if value == "OK":
        return color_text("OK", GREEN)

    if value == "Error":
        return color_text("Error", RED)

    return color_text("-", YELLOW)


def color_bool(value):

    if str(value) == "True":
        return color_text("True", GREEN)

    return color_text("False", RED)


def color_result(message):

    if message.startswith("Failed"):
        return color_text(message, RED)

    if "Skipped" in message:
        return color_text(message, RED)

    return message


def main():

    data_service = DataServices()
    results = []

    # loop through users
    for user in data_service.users:

        role = get_role_name(user.role)

        # build user data dictionary
        user_dict = {
            "username": user.username,
            "active": user.active,
            "logged_in": user.logged_in,
            "role": role,            
            "subscription": getattr(user, "subscription", "free"),
            "permissions": get_permissions(user.role)
        }

        # check if user can receive notification
        eligible, status = is_user_eligible(user_dict)

        if eligible == False:

            result = {
                "username": user_dict["username"],
                "active": user_dict["active"],
                "logged_in": user_dict["logged_in"],
                "role": user_dict["role"],
                "subscription": user_dict["subscription"],
                "attempt1": "-",
                "attempt2": "-",
                "attempt3": "-",
                "result": status
            }

        else:
            # generate and send notification
            message = generate_notification(user_dict)
            attempts, final_message = send_notification(message)

            result = {
                "username": user_dict["username"],
                "active": user_dict["active"],
                "logged_in": user_dict["logged_in"],
                "role": user_dict["role"],
                "subscription": user_dict["subscription"],
                "attempt1": attempts[0],
                "attempt2": attempts[1],
                "attempt3": attempts[2],
                "result": final_message
            }

        results.append(result)

    print("\n" + "=" * 140)
    print("SMART NOTIFICATION SYSTEM".center(140))
    print("=" * 140)
    # print table header
    print(
        f"{'Username':<15}"
        f"{'Active':<10}"
        f"{'Logged In':<12}"
        f"{'Role':<12}"
        f"{'Subscription':<15}"
        f"{'Attempt 1':<12}"
        f"{'Attempt 2':<12}"
        f"{'Attempt 3':<12}"
        f"{'Result'}"
    )

    print("-" * 140)
    # print each row
    for row in results:
        print(
            f"{row['username']:<15}"
            f"{color_bool(row['active']):<19}"
            f"{color_bool(row['logged_in']):<21}"
            f"{row['role']:<12}"
            f"{row['subscription']:<15}"
            f"{color_attempt(row['attempt1']):<21}"
            f"{color_attempt(row['attempt2']):<21}"
            f"{color_attempt(row['attempt3']):<21}"
            f"{color_result(row['result'])}"
        )

    print("=" * 140)
    print(color_text("\nSystem finished.", BLUE))

    # generate_notification({
    #     "role": "admin",
    #     "subscription": "free1"
    # })

    # print(generate_notification({
    #     "role": "admin",
    #     "subscription": "premium",
    #     "active": False,
    #     "logged_in": False
    # }))
        
if __name__ == "__main__":
    main()
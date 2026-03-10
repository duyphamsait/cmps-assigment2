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

def color_text(text, color):
    return color + text + RESET

def get_role_name(role):
    if isinstance(role, Role):
        return role.value
    return str(role)

def generate_notification(user_dict):

    role = user_dict["role"].capitalize()
    subscription = user_dict["subscription"]

    if subscription == "premium":
        tier = color_text("Premium", BLUE)
    else:
        tier = color_text("Free", GREEN)

    return tier + " " + role + " notification was sent"


def is_user_eligible(user_dict):

    if user_dict["active"] == False:
        return False, color_text("Skipped", YELLOW) + ": inactive user"

    if user_dict["logged_in"] == False:
        return False, color_text("Skipped", YELLOW) + ": not logged in"

    if user_dict["role"] not in ["admin", "editor", "viewer"]:
        return False, color_text("Skipped", YELLOW) + ": invalid role"

    if user_dict["subscription"] not in ["free", "premium"]:
        return False, color_text("Skipped", YELLOW) + ": invalid subscription"

    # if len(user_dict["permissions"]) == 0:
    #     return False, color_text("Skipped", YELLOW) + ": no permissions"

    return True, "Eligible"


def send_notification(message):

    attempts = ["-", "-", "-"]

    for i in range(MAX_SEND_ATTEMPTS):

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

    for user in data_service.users:

        role = get_role_name(user.role)

        user_dict = {
            "username": user.username,
            "active": user.active,
            "logged_in": user.logged_in,
            "role": role,
            "subscription": getattr(user, "subscription", "free")
        }

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


if __name__ == "__main__":
    main()
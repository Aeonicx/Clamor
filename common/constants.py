# OTP verification time for phone
DEFAULT_OTP_TIME = 600  # 10 minute

# Define a regular expression pattern to match phone numbers
PHONE_VALIDATE_REGEX = r"^\+?[1-9]\d{1,14}$"


AVAILABILITY_STATUS_CHOICES = [
    (1, "Close"),
    (2, "Open"),
]

DEFAULT_STATUS_CHOICES = [
    (1, "Not Available"),
    (2, "Available"),
]


DAY_CHOICES = [
    (1, "Sunday"),
    (2, "Monday"),
    (3, "Tuesday"),
    (4, "Wednesday"),
    (5, "Thursday"),
    (6, "Friday"),
    (7, "Saturday"),
]

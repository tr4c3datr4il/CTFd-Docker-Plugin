from CTFd.models import Users, Teams
from CTFd.models import Challenges
import requests


WEBHOOK_URL = "https://discord.com/api/webhooks/your_webhook_url_here"
CTFD_BASE_URL = "http://0.0.0.0:8000/containers/admin/cheat"
IS_RUN = True  # Set to False to disable webhook alerts

def get_username(user_id, is_team_mode):
    if is_team_mode:
        team = Teams.query.filter_by(id=user_id).first()
        return team.name if team else "Unknown Team"
    else:
        user = Users.query.filter_by(id=user_id).first()
        return user.name if user else "Unknown User"
    
def get_challenge_name(challenge_id):
    challenge = Challenges.query.filter_by(id=challenge_id).first()
    return challenge.name if challenge else "Unknown Challenge"

def send_alert(challenge_id, original_team_id, original_user_id, second_team_id, second_user_id, is_team_mode):
    data = {
        "embeds": [
            {
                "description" : "Found cheaters in challenge {}: Owner: {} | Submitter: {}".format(
                    get_challenge_name(challenge_id), 
                    get_username(original_team_id if is_team_mode else original_user_id, is_team_mode),
                    get_username(second_team_id if is_team_mode else second_user_id, is_team_mode), 
                ),
                "title" : "ALERT: Cheating Detected!!! ⚠️⚠️⚠️",
                "color" : 16711680,
                "url" : CTFD_BASE_URL
            }
        ]
    }

    response = requests.post(WEBHOOK_URL, json=data)
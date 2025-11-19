import os
import json
import requests
from datetime import datetime

# Pobranie zmiennych środowiskowych GitHub Actions
WEBHOOK_URL = os.getenv('DISCORD_WEBHOOK_URL')  # Secret w GitHub Actions
REPOSITORY = os.getenv('GITHUB_REPOSITORY')  # np. "owner/repo-name"
BRANCH = os.getenv('GITHUB_REF_NAME')  # nazwa brancha
COMMIT_SHA = os.getenv('GITHUB_SHA')  # pełny SHA commita
COMMIT_SHORT_SHA = os.getenv('GITHUB_SHA')[:7] if os.getenv('GITHUB_SHA') else 'unknown'
ACTOR = os.getenv('GITHUB_ACTOR')  # użytkownik, który uruchomił workflow
WORKFLOW = os.getenv('GITHUB_WORKFLOW')  # nazwa workflow
RUN_NUMBER = os.getenv('GITHUB_RUN_NUMBER')  # numer uruchomienia
SERVER_NAME = os.getenv('SERVER_NAME', 'vps')  # własna zmienna
REPO_URL = f"https://github.com/{REPOSITORY}" if REPOSITORY else None
COMMIT_URL = f"{REPO_URL}/commit/{COMMIT_SHA}" if REPO_URL and COMMIT_SHA else None
ACTION_URL = f"{REPO_URL}/actions/runs/{os.getenv('GITHUB_RUN_ID')}" if REPO_URL else None

def send_discord_notification(status="in_progress", error_msg=None):
    """
    Wysyła powiadomienie do Discord webhook
    
    Args:
        status: "in_progress", "success", lub "failure"
        error_msg: opcjonalny komunikat błędu
    """
    
    # Ustawienie koloru w zależności od statusu
    colors = {
        "in_progress": 3447003,  # niebieski
        "success": 5814783,       # zielony
        "failure": 16711680       # czerwony
    }
    
    # Emoji dla statusu
    status_emoji = {
        "in_progress": "🔄",
        "success": "✅",
        "failure": "❌"
    }
    
    # Tytuły dla statusu
    status_titles = {
        "in_progress": "Odświeżanie repozytorium w trakcie",
        "success": "Repozytorium odświeżone pomyślnie",
        "failure": "Błąd podczas odświeżania repozytorium"
    }
    
    color = colors.get(status, 3447003)
    emoji = status_emoji.get(status, "🔄")
    title = f"{emoji} {status_titles.get(status, 'Status nieznany')}"
    
    # Przygotowanie pól embedu
    fields = [
        {
            "name": "📦 Repozytorium",
            "value": REPOSITORY or "Nieznane",
            "inline": True
        },
        {
            "name": "🌿 Branch",
            "value": BRANCH or "Nieznany",
            "inline": True
        },
        {
            "name": "🖥️ Serwer",
            "value": SERVER_NAME,
            "inline": True
        },
        {
            "name": "👤 Uruchomione przez",
            "value": ACTOR or "Nieznany",
            "inline": True
        },
        {
            "name": "🔢 Run #",
            "value": RUN_NUMBER or "N/A",
            "inline": True
        },
        {
            "name": "📝 Commit",
            "value": f"[`{COMMIT_SHORT_SHA}`]({COMMIT_URL})" if COMMIT_URL else COMMIT_SHORT_SHA,
            "inline": True
        }
    ]
    
    # Dodanie informacji o błędzie jeśli wystąpił
    if error_msg and status == "failure":
        fields.append({
            "name": "⚠️ Błąd",
            "value": f"``````",  # limit 1024 znaki
            "inline": False
        })
    
    # Przygotowanie payloadu
    payload = {
        "username": "GitHub Deploy Bot",
        "avatar_url": "https://github.githubassets.com/images/modules/logos_page/GitHub-Mark.png",
        "embeds": [{
            "title": title,
            "description": f"Workflow: **{WORKFLOW}**",
            "color": color,
            "fields": fields,
            "timestamp": datetime.utcnow().isoformat(),
            "footer": {
                "text": "GitHub Actions Deployment"
            },
            "url": ACTION_URL  # link do workflow run
        }]
    }
    
    # Wysłanie webhooka
    try:
        response = requests.post(
            WEBHOOK_URL,
            data=json.dumps(payload),
            headers={"Content-Type": "application/json"}
        )
        response.raise_for_status()
        print(f"✅ Powiadomienie Discord wysłane pomyślnie (status: {status})")
        return True
    except requests.exceptions.RequestException as e:
        print(f"❌ Błąd podczas wysyłania powiadomienia Discord: {e}")
        return False

if __name__ == "__main__":
    # Przykład użycia - start procesu
    send_discord_notification(status="in_progress")

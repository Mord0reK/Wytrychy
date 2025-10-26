import os
import requests
import sys

def send_webhook_request():
    """
    Wysyła zapytanie HTTP do serwera wykorzystując dane ze zmiennych środowiskowych.
    """
    try:
        # Pobranie zmiennych środowiskowych
        auth_header_name = os.getenv('AUTH_HEADER_NAME')
        auth_header_value = os.getenv('AUTH_HEADER_VALUE')
        cf_aci = os.getenv('CF_ACI')
        cf_acs = os.getenv('CF_ACS')
        webhook_url = os.getenv('WEBHOOK_URL')
        webhook_method = os.getenv('WEBHOOK_METHOD')
        
        # Walidacja wymaganych zmiennych
        required_vars = {
            'AUTH-HEADER-NAME': auth_header_name,
            'AUTH-HEADER-VALUE': auth_header_value,
            'CF-ACI': cf_aci,
            'CF-ACS': cf_acs,
            'WEBHOOK-URL': webhook_url
        }
        
        missing_vars = [var_name for var_name, var_value in required_vars.items() if not var_value]
        
        if missing_vars:
            print(f"Błąd: Brakujące zmienne środowiskowe: {', '.join(missing_vars)}")
            sys.exit(1)
        
        # Przygotowanie headerów
        headers = {
            auth_header_name: auth_header_value,
            'CF-Access-Client-ID': cf_aci,
            'CF-Access-Client-Secret': cf_acs
        }
        
        # Wykonanie zapytania
        response = requests.request(
            method=webhook_method,
            url=webhook_url,
            headers=headers,
            timeout=30
        )
        
        # Wyświetlenie wyniku
        print(f"\nStatus Code: {response.status_code}")
        print(f"Response Headers: {dict(response.headers)}")
        print(f"\nResponse Body:")
        print(response.text)
        
        # Zwrócenie kodu błędu jeśli request się nie powiódł
        if response.status_code >= 400:
            sys.exit(1)
            
        return response
        
    except requests.exceptions.RequestException as e:
        print(f"Błąd podczas wykonywania zapytania: {e}")
        sys.exit(1)
    except Exception as e:
        print(f"Nieoczekiwany błąd: {e}")
        sys.exit(1)

if __name__ == "__main__":
    send_webhook_request()

import os
import requests
from datetime import datetime, timedelta
import time

GITLAB_USER = os.environ.get("GITLAB_USER")
GITLAB_PRIVATE_TOKEN = os.environ.get("GITLAB_PRIVATE_TOKEN")
GITHUB_USER_EMAIL = os.environ.get("GITHUB_USER_EMAIL")
GITHUB_USER_NAME = os.environ.get("GITHUB_USER_NAME")
GITLAB_URL = "https://gitlab.com"
ACTIONS_TO_TRACK = ['pushed', 'commented', 'approved', 'created', 'starred']

if not all([GITLAB_USER, GITLAB_PRIVATE_TOKEN, GITHUB_USER_EMAIL, GITHUB_USER_NAME]):
    print("Erro: Variáveis de ambiente essenciais não foram definidas.")
    exit(1)

def get_gitlab_events():
    """Busca os eventos de contribuição do usuário no GitLab para múltiplas ações."""
    all_events = []
    headers = {"PRIVATE-TOKEN": GITLAB_PRIVATE_TOKEN}
    after_date = (datetime.now() - timedelta(days=365)).strftime('%Y-%m-%d')
    
    print(f"Buscando eventos após a data: {after_date}")
    
    for action in ACTIONS_TO_TRACK:
        print(f"Buscando por ação: '{action}'...")
        try:
            url = f"{GITLAB_URL}/api/v4/users/{GITLAB_USER}/events?action={action}&after={after_date}&per_page=100"
            response = requests.get(url, headers=headers)
            response.raise_for_status()
            events = response.json()
            if events:
                print(f"  -> Encontrados {len(events)} eventos para '{action}'.")
                all_events.extend(events)
            else:
                print(f"  -> Nenhum evento recente para '{action}'.")
            
            time.sleep(1)

        except requests.exceptions.RequestException as e:
            print(f"  -> Erro ao buscar eventos para '{action}': {e}")
            continue
            
    return all_events

def configure_git():
    os.system(f'git config --global user.name "{GITHUB_USER_NAME}"')
    os.system(f'git config --global user.email "{GITHUB_USER_EMAIL}"')

def create_dummy_commit(event_date):
    """Cria um commit vazio na data especificada."""
    commit_message = f"GitLab contribution on {event_date}"
    date_str = datetime.strptime(event_date, "%Y-%m-%d").strftime("%Y-%m-%dT12:00:00")
    
    command = (
        f'GIT_AUTHOR_DATE="{date_str}" GIT_COMMITTER_DATE="{date_str}" '
        f'git commit --allow-empty -m "{commit_message}"'
    )
    os.system(command)

def main():
    print("Iniciando a importação de atividades do GitLab...")
    configure_git()
    
    events = get_gitlab_events()
    if not events:
        print("Nenhum evento de contribuição encontrado no último ano.")
        return

    contribution_dates = {event['created_at'].split('T')[0] for event in events}
    
    print(f"\nTotal de dias únicos com contribuições encontradas: {len(contribution_dates)}.")
    
    existing_dates = set(os.popen('git log --pretty=format:"%as"').read().splitlines())
    print(f"Datas já existentes no log: {len(existing_dates)}")
    
    new_dates = sorted(list(contribution_dates - existing_dates))

    if not new_dates:
        print("\nNenhuma nova data de contribuição para adicionar. Repositório já está sincronizado.")
    else:
        print(f"\nNovas datas a serem adicionadas: {len(new_dates)}")
        for date in new_dates:
            print(f"  -> Criando commit para a data: {date}")
            create_dummy_commit(date)
        
        print("\nSincronizando com o repositório remoto do GitHub...")
        os.system("git push")
    
    print("\nImportação concluída com sucesso!")

if __name__ == "__main__":
    main()

from github import Github
import os
import datetime

def fetch_repos(g):
    return [r for r in g.get_user().get_repos() if not r.private]

def score_repo(repo):
    try:
        topics = repo.get_topics() or []
    except Exception:
        topics = []
    has_featured = 'featured' in topics
    pushed = repo.pushed_at or repo.updated_at or datetime.datetime(1970, 1, 1)
    stars = repo.stargazers_count or 0
    return (not has_featured, -pushed.timestamp(), -stars, repo.name.lower())

def select_top(repos, count=6):
    return sorted(repos, key=score_repo)[:count]

def build_project_line(repo):
    name = repo.name
    url = repo.html_url
    desc = (repo.description or 'No description provided.').strip().rstrip('. ')[:200]
    tags = []
    if repo.language:
        tags.append(repo.language)
    try:
        topics = repo.get_topics() or []
    except Exception:
        topics = []
    tags += [t for t in topics if t.lower() != 'featured']
    # deduplicate tags while preserving order
    seen = set()
    uniq = []
    for t in tags:
        if t and t not in seen:
            seen.add(t)
            uniq.append(t)
    tag_str = ', '.join(uniq)
    last_update = repo.pushed_at or repo.updated_at or datetime.datetime.utcnow()
    date_str = last_update.strftime("%Y\u2011%m\u2011%d")
    stars = repo.stargazers_count or 0
    stars_str = f" ({stars}\u2605)" if stars > 0 else ""
    return f"- [{name}]({url}) — {desc}. Tags: {tag_str}. Updated: {date_str}{stars_str}"

def update_readme(projects_md):
    start_marker = "<!-- PROJECTS-START -->"
    end_marker = "<!-- PROJECTS-END -->"
    with open('README.md', 'r', encoding='utf-8') as f:
        content = f.read()
    start = content.find(start_marker)
    end = content.find(end_marker, start)
    if start == -1 or end == -1:
        raise ValueError('Project markers not found')
    new_section = f"{start_marker}\n\n{projects_md}\n\n{end_marker}"
    new_content = content[:start] + new_section + content[end + len(end_marker):]
    if new_content == content:
        return False
    with open('README.md', 'w', encoding='utf-8') as f:
        f.write(new_content)
    return True

def main():
    token = os.getenv('GH_TOKEN') or os.getenv('GITHUB_TOKEN')
    if not token:
        raise EnvironmentError('GH_TOKEN or GITHUB_TOKEN environment variable is required')
    gh = Github(token)
    repos = fetch_repos(gh)
    if not repos:
        print('No repositories found.')
        return
    top = select_top(repos)
    projects_md = '\n'.join(build_project_line(r) for r in top)
    updated = update_readme(projects_md)
    if updated:
        print('README.md updated with new projects section.')
    else:
        print('README.md projects section is up to date; no changes made.')

if __name__ == '__main__':
    main()

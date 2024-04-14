class Filter:
    def __init__(self, repository_id=0, name="", is_fork=False, commits=0, branches=0, default_branch="",
                 releases=0, contributors=0, repository_license="", watchers=0, stargazers=0, forks=0,
                 size=0, created_at="", pushed_at="", updated_at="",
                 homepage="", main_language=None, total_issues=0, open_issues=0, total_pull_requests=0,
                 open_pull_requests=0, last_commit="", last_commit_sha="", has_wiki=False,
                 is_archived=False, languages=None, labels=None):
        if main_language is None:
            main_language = []
        if labels is None:
            labels = []
        if languages is None:
            languages = []
        self.__id = repository_id
        self.__name = name
        self.__is_fork = is_fork
        self.__commits = commits
        self.__branches = branches
        self.__default_branch = default_branch
        self.__releases = releases
        self.__contributors = contributors
        self.__license = repository_license
        self.__watchers = watchers
        self.__stargazers = stargazers
        self.__forks = forks
        self.__size = size
        self.__created_at = created_at
        self.__pushed_at = pushed_at
        self.__updated_at = updated_at
        self.__homepage = homepage
        self.__main_language = main_language
        self.__total_issues = total_issues
        self.__open_issues = open_issues
        self.__total_pull_requests = total_pull_requests
        self.__open_pull_requests = open_pull_requests
        self.__last_commit = last_commit
        self.__last_commit_sha = last_commit_sha
        self.__has_wiki = has_wiki
        self.__is_archived = is_archived
        self.__languages = languages
        self.__labels = labels

    def filtering(self, repositories):
        risultati = []
        for item in repositories:
            if (item['isFork'] == self.__is_fork and
                    item['commits'] is not None and
                    item['commits'] > self.__commits and
                    item['mainLanguage'] in self.__main_language and
                    item['stargazers'] is not None and
                    item['stargazers'] >= self.__stargazers and
                    item['contributors'] is not None and
                    item['contributors'] > self.__contributors):
                risultati.append((item['name'], item['mainLanguage']))
        return risultati

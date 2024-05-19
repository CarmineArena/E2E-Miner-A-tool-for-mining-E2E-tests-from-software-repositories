from sqlalchemy import create_engine, ForeignKey, String, Integer, Boolean, Column
from sqlalchemy.orm import declarative_base
from DBconnector import Base
from DBconnector import Session, engine


class Repository(Base):
    __tablename__ = "repository"
    ID = Column(Integer(), primary_key=True)
    name = Column(String())
    is_fork = Column(Boolean())
    commits = Column(Integer())
    branches = Column(Integer())
    releases = Column(Integer())
    forks = Column(Integer())
    main_language = Column(String())
    default_branch = Column(String())
    licences = Column(String())
    homepage = Column(String())
    watchers = Column(Integer())
    stargazers = Column(Integer())
    contributors = Column(Integer())
    size = Column(Integer())
    created_at = Column(String())
    pushed_at = Column(String())
    updated_at = Column(String())
    total_issues = Column(Integer())
    open_issues = Column(Integer())
    total_pull_requests = Column(Integer())
    open_pull_requests = Column(Integer())
    blank_lines = Column(Integer())
    code_lines = Column(Integer())
    comment_lines = Column(Integer())
    metrics = Column(String())
    last_commit = Column(String())
    last_commit_sha = Column(String())
    has_wiki = Column(Boolean())
    is_archived = Column(Boolean())
    is_disabled = Column(Boolean())
    is_locked = Column(Boolean())
    languages = Column(String())
    labels = Column(String())
    topics = Column(String())
    is_processed = Column(Boolean())

    def __init__(self, name, is_fork, commits, branches, releases, forks,
                 main_language, default_branch, licenses, homepage, watchers,
                 stargazers, contributors, size, created_at, pushed_at, updated_at,
                 total_issues, open_issues, total_pull_requests, open_pull_requests,
                 blank_lines, code_lines, comment_lines, metrics, last_commit,
                 last_commit_sha, has_wiki, is_archived, is_disabled, is_locked, languages, labels, topics,
                 is_processed=False):
        self.name = name
        self.is_fork = is_fork
        self.commits = commits
        self.branches = branches
        self.releases = releases
        self.forks = forks
        self.main_language = main_language
        self.default_branch = default_branch
        self.licences = licenses
        self.homepage = homepage
        self.watchers = watchers
        self.stargazers = stargazers
        self.contributors = contributors
        self.size = size
        self.created_at = created_at
        self.pushed_at = pushed_at
        self.updated_at = updated_at
        self.total_issues = total_issues
        self.open_issues = open_issues
        self.total_pull_requests = total_pull_requests
        self.open_pull_requests = open_pull_requests
        self.blank_lines = blank_lines
        self.code_lines = code_lines
        self.comment_lines = comment_lines
        self.metrics = metrics
        self.last_commit = last_commit
        self.last_commit_sha = last_commit_sha
        self.has_wiki = has_wiki
        self.is_archived = is_archived
        self.is_disabled = is_disabled
        self.is_locked = is_locked
        self.languages = languages
        self.labels = labels
        self.topics = topics
        self.is_processed = is_processed
        Base.metadata.create_all(engine)

    def connect_to_db(self):
        local_session = Session(bind=engine)
        return local_session

    def add_repository_to_db(self):
        local_session = Session(bind=engine)
        self.languages = self.convert_list_in_string(self.languages)
        self.labels = self.convert_list_in_string(self.labels)
        self.topics = self.convert_list_in_string(self.topics)
        self.metrics = self.convert_metrics_in_string(self.metrics)
        local_session.add(self)
        local_session.commit()

    def convert_metrics_in_string(self, metric):
        import json
        data = json.loads(metric)

        # Inizializza una lista per memorizzare le stringhe dei metrics
        metrics_strings = []

        # Itera su ogni elemento nella lista
        for item in data:
            # Costruisci la stringa per l'elemento corrente
            metrics_str = f"language:{item['language']}, commentLines:{item['commentLines']}, codeLines:{item['codeLines']}, blankLines:{item['blankLines']}"
            # Aggiungi la stringa alla lista
            metrics_strings.append(metrics_str)

        # Unisci tutte le stringhe dei metrics usando il punto e virgola come separatore
        output_string = "; ".join(metrics_strings)
        return output_string

    def convert_list_in_string(self, general_list):
        string = ""
        for element in general_list:
            string = string + element + "; "
        return string

    def convert_string_language_in_list(self):
        # Rimuovi lo spazio finale e poi suddividi la stringa utilizzando il separatore "; "
        elements = self.languages.rstrip("; ").split("; ")
        self.languages = elements

    def update_processed_repository(self):
        local_session = Session(bind=engine)
        # self.is_processed = True
        repository_to_update = local_session.query(Repository).filter(Repository.ID == self.ID).first()
        repository_to_update.is_processed = True
        local_session.commit()


class WebRepository:

    def __init__(self, idrepository, name):
        self.IDrepository = idrepository
        self.name = name
        self.is_web_java = False
        self.is_web_python = False
        self.is_web_javascript = False
        self.is_web_typescript = False
        self.is_selenium_tested_java = False
        self.is_selenium_tested_python = False
        self.is_selenium_tested_javascript = False
        self.is_selenium_tested_typescript = False
        # self.is_puppeteer_tested_java = False
        self.is_puppeteer_tested_python = False
        self.is_puppeteer_tested_javascript = False
        self.is_puppeteer_tested_typescript = False
        self.is_playwright_tested_java = False
        self.is_playwright_tested_python = False
        self.is_playwright_tested_javascript = False
        self.is_playwright_tested_typescript = False
        self.is_cypress_tested_javascript = False
        self.is_cypress_tested_typescript = False
        self.is_locust_tested_java = False
        self.is_locust_tested_python = False
        # self.is_locust_tested_javascript = False
        self.is_jmeter_tested = False
        self.web_dependencies = []
        self.test_path = []

    def set_is_web_java(self, value):
        self.is_web_java = value

    def set_is_web_python(self, value):
        self.is_web_python = value

    def set_is_web_javascript(self, value):
        self.is_web_javascript = value

    def set_is_web_typescript(self, value):
        self.is_web_typescript = value

    def get_is_selenium_tested_java(self):
        return self.is_selenium_tested_java

    def set_is_selenium_tested_java(self, value):
        self.is_selenium_tested_java = value

    def get_is_selenium_tested_python(self):
        return self.is_selenium_tested_python

    def set_is_selenium_tested_python(self, value):
        self.is_selenium_tested_python = value

    def get_is_selenium_tested_javascript(self):
        return self.is_selenium_tested_javascript

    def set_is_selenium_tested_javascript(self, value):
        self.is_selenium_tested_javascript = value

    def get_is_selenium_tested_typescript(self):
        return self.is_selenium_tested_typescript

    def set_is_selenium_tested_typescript(self, value):
        self.is_selenium_tested_typescript = value

    def get_is_puppeteer_tested_python(self):
        return self.is_puppeteer_tested_python

    def set_is_puppeteer_tested_python(self, value):
        self.is_puppeteer_tested_python = value

    def get_is_puppeteer_tested_javascript(self):
        return self.is_puppeteer_tested_javascript

    def set_is_puppeteer_tested_javascript(self, value):
        self.is_puppeteer_tested_javascript = value

    def get_is_puppeteer_tested_typescript(self):
        return self.is_puppeteer_tested_typescript

    def set_is_puppeteer_tested_typescript(self, value):
        self.is_puppeteer_tested_typescript = value

    def get_is_playwright_tested_java(self):
        return self.is_playwright_tested_java

    def set_is_playwright_tested_java(self, value):
        self.is_playwright_tested_java = value

    def get_is_playwright_tested_python(self):
        return self.is_playwright_tested_python

    def set_is_playwright_tested_python(self, value):
        self.is_playwright_tested_python = value

    def get_is_playwright_tested_javascript(self):
        return self.is_playwright_tested_javascript

    def set_is_playwright_tested_javascript(self, value):
        self.is_playwright_tested_javascript = value

    def get_is_playwright_tested_typescript(self):
        return self.is_playwright_tested_typescript

    def set_is_playwright_tested_typescript(self, value):
        self.is_playwright_tested_typescript = value

    def get_is_cypress_tested_javascript(self):
        return self.is_cypress_tested_javascript

    def set_is_cypress_tested_javascript(self, conditions):
        self.is_cypress_tested_javascript = conditions

    def get_is_cypress_tested_typescript(self):
        return self.is_cypress_tested_typescript

    def set_is_cypress_tested_typescript(self, conditions):
        self.is_cypress_tested_typescript = conditions

    def get_is_locust_tested_java(self):
        return self.is_locust_tested_java

    def set_is_locust_tested_java(self, value):
        self.is_locust_tested_java = value

    def get_is_locust_tested_python(self):
        return self.is_locust_tested_python

    def set_is_locust_tested_python(self, value):
        self.is_locust_tested_python = value

    def set_is_jmeter_tested(self, conditions):
        self.is_jmeter_tested = conditions

    def set_web_dependency(self, dependencies):
        self.web_dependencies = dependencies

    def set_test_path(self, path_list):
        self.test_path = path_list

    def add_path_in_list(self, list):
        self.test_path += list


class WebRepositoryDAO(Base):
    __tablename__ = "webrepository"
    IDweb = Column(Integer(), primary_key=True)
    IDrepository = Column(Integer(), ForeignKey("repository.ID"))
    name = Column(String())
    is_web_java = Column(Boolean())
    is_web_python = Column(Boolean())
    is_web_javascript = Column(Boolean())
    is_web_typescript = Column(Boolean())
    is_selenium_tested_java = Column(Boolean())
    is_selenium_tested_python = Column(Boolean())
    is_selenium_tested_javascript = Column(Boolean())
    is_selenium_tested_typescript = Column(Boolean())
    # is_puppeteer_tested_java = Column(Boolean())
    is_puppeteer_tested_python = Column(Boolean())
    is_puppeteer_tested_javascript = Column(Boolean())
    is_puppeteer_tested_typescript = Column(Boolean())
    is_playwright_tested_java = Column(Boolean())
    is_playwright_tested_python = Column(Boolean())
    is_playwright_tested_javascript = Column(Boolean())
    is_playwright_tested_typescript = Column(Boolean())
    is_cypress_tested_javascript = Column(Boolean())
    is_cypress_tested_typescript = Column(Boolean())
    is_locust_tested_java = Column(Boolean())
    is_locust_tested_python = Column(Boolean())
    # is_locust_tested_javascript = Column(Boolean())
    is_jmeter_tested = Column(Boolean())
    web_dependencies = Column(String())
    test_path = Column(String())

    def __init__(self, WebRepository):
        self.IDrepository = WebRepository.IDrepository
        self.name = WebRepository.name
        self.is_web_java = WebRepository.is_web_java
        self.is_web_python = WebRepository.is_web_python
        self.is_web_javascript = WebRepository.is_web_javascript
        self.is_web_typescript = WebRepository.is_web_typescript
        self.is_selenium_tested_java = WebRepository.is_selenium_tested_java
        self.is_selenium_tested_python = WebRepository.is_selenium_tested_python
        self.is_selenium_tested_javascript = WebRepository.is_selenium_tested_javascript
        self.is_selenium_tested_typescript = WebRepository.is_selenium_tested_typescript
        # self.is_puppeteer_tested_java = WebRepository.is_puppeteer_tested_java
        self.is_puppeteer_tested_python = WebRepository.is_puppeteer_tested_python
        self.is_puppeteer_tested_javascript = WebRepository.is_puppeteer_tested_javascript
        self.is_puppeteer_tested_typescript = WebRepository.is_puppeteer_tested_typescript
        self.is_playwright_tested_java = WebRepository.is_playwright_tested_java
        self.is_playwright_tested_python = WebRepository.is_playwright_tested_python
        self.is_playwright_tested_javascript = WebRepository.is_playwright_tested_javascript
        self.is_playwright_tested_typescript = WebRepository.is_playwright_tested_typescript
        self.is_cypress_tested_javascript = WebRepository.is_cypress_tested_javascript
        self.is_cypress_tested_typescript = WebRepository.is_cypress_tested_typescript
        self.is_locust_tested_java = WebRepository.is_locust_tested_java
        self.is_locust_tested_python = WebRepository.is_locust_tested_python
        # self.is_locust_tested_javascript = WebRepository.is_locust_tested_javascript
        self.is_jmeter_tested = WebRepository.is_jmeter_tested
        self.web_dependencies = self.convert_list_in_string(WebRepository.web_dependencies)
        self.test_path = self.convert_list_in_string(WebRepository.test_path)
        Base.metadata.create_all(engine)

    def add_web_repository_to_db(self):
        local_session = Session(bind=engine)
        local_session.add(self)
        local_session.commit()

    def convert_list_in_string(self, general_list):
        string = ""
        for element in general_list:
            string = string + element + "; "
        return string

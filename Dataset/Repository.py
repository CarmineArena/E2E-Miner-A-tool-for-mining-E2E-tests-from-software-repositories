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
    last_commit = Column(String())
    last_commit_sha = Column(String())
    has_wiki = Column(Boolean())
    is_archived = Column(Boolean())
    is_disabled = Column(Boolean())
    is_locked = Column(Boolean())
    languages = Column(String())
    labels = Column(String())
    topics = Column(String())

    def __init__(self, name, is_fork, commits, branches, releases, forks,
                 main_language, default_branch, licenses, homepage, watchers,
                 stargazers, contributors, size, created_at, pushed_at, updated_at,
                 total_issues, open_issues, total_pull_requests, open_pull_requests,
                 blank_lines, code_lines, comment_lines, last_commit,
                 last_commit_sha, has_wiki, is_archived, is_disabled, is_locked, languages, labels, topics):
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
        self.last_commit = last_commit
        self.last_commit_sha = last_commit_sha
        self.has_wiki = has_wiki
        self.is_archived = is_archived
        self.is_disabled = is_disabled
        self.is_locked = is_locked
        self.languages = languages
        self.labels = labels
        self.topics = topics
        Base.metadata.create_all(engine)

    def connect_to_db(self):
        local_session = Session(bind=engine)
        return local_session

    def add_repository_to_db(self):
        local_session = Session(bind=engine)
        self.languages = self.convert_list_in_string(self.languages)
        self.labels = self.convert_list_in_string(self.labels)
        self.topics = self.convert_list_in_string(self.topics)
        local_session.add(self)
        local_session.commit()

    def convert_list_in_string(self, general_list):
        string = ""
        for element in general_list:
            string = string + element + "; "
        return string


class WebRepository:

    def __init__(self, idrepository, name):
        self.IDrepository = idrepository
        self.name = name
        self.is_selenium_tested = False
        self.is_puppeteer_tested = False
        self.is_playwright_tested = False
        self.is_cypress_tested = False
        self.is_locust_tested = False
        self.is_jmeter_tested = False

    def set_is_selenium_tested(self, conditions):
        self.is_selenium_tested = conditions

    def set_is_puppeteer_tested(self, conditions):
        self.is_puppeteer_tested = conditions

    def set_is_playwright_tested(self, conditions):
        self.is_playwright_tested = conditions

    def set_is_cypress_tested(self, conditions):
        self.is_cypress_tested = conditions

    def set_is_locust_tested(self, conditions):
        self.is_locust_tested = conditions

    def set_is_jmeter_tested(self, conditions):
        self.is_jmeter_tested = conditions


class WebRepositoryDAO(Base):
    __tablename__ = "webrepository"
    IDweb = Column(Integer(), primary_key=True)
    IDrepository = Column(Integer(), ForeignKey("repository.ID"))
    name = Column(String())
    is_selenium_tested = Column(Boolean())
    is_puppeteer_tested = Column(Boolean())
    is_playwright_tested = Column(Boolean())
    is_cypress_tested = Column(Boolean())
    is_locust_tested = Column(Boolean())
    is_jmeter_tested = Column(Boolean())

    def __init__(self, WebRepository):
        self.IDrepository = WebRepository.IDrepository
        self.name = WebRepository.name
        self.is_selenium_tested = WebRepository.is_selenium_tested
        self.is_puppeteer_tested = WebRepository.is_puppeteer_tested
        self.is_playwright_tested = WebRepository.is_playwright_tested
        self.is_cypress_tested = WebRepository.is_cypress_tested
        self.is_locust_tested = WebRepository.is_locust_tested
        self.is_jmeter_tested = WebRepository.is_jmeter_tested
        Base.metadata.create_all(engine)

    def add_web_repository_to_db(self):
        local_session = Session(bind=engine)
        local_session.add(self)
        local_session.commit()

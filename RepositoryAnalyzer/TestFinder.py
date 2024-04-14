import os
from abc import ABC

from RepositoryAnalyzer.TestFinderInterface import TestDependencyFinderInterface


class SeleniumFinder(TestDependencyFinderInterface, ABC):

    def find_test_dependency_in_repository(self, repository, dependency_list):
        for dependency in dependency_list:
            if dependency[0] == 'org.seleniumhq.selenium' or dependency[0] == 'selenium':
                print("usa selenium")
                return True
        return False


class PlayWrightFinder(TestDependencyFinderInterface, ABC):

    def find_test_dependency_in_repository(self, repository, dependency_list):
        for dependency in dependency_list:
            if dependency[0] == 'com.microsoft.playwright' or dependency[0] == 'playwright':
                print("usa PlayWright")
                return True
        return False


class PuppeteerFinder(TestDependencyFinderInterface, ABC):

    def find_test_dependency_in_repository(self, repository, dependency_list):
        for dependency in dependency_list:
            if dependency[0] == 'puppeteer':
                print("usa Puppeteer")
                return True
            if dependency[0] == 'org.webjars.npm' and dependency[1] == 'puppeteer':
                return True
        return False


class CypressFinder(TestDependencyFinderInterface, ABC):

    def find_test_dependency_in_repository(self, repository, dependency_list):
        for dependency in dependency_list:
            if dependency[0] == 'cypress':
                print("usa cypress")
                return True
        return False


class LocustFinder(TestDependencyFinderInterface, ABC):

    def find_test_dependency_in_repository(self, repository, dependency_list):
        for dependency in dependency_list:
            if dependency[0] == 'locust' or dependency[1] == 'locust4j':
                print("usa Locust")
                return True
        return False


class JMeterFinder(TestDependencyFinderInterface, ABC):

    def find_test_dependency_in_repository(self, repository, dependency_list):
        for root, dirs, files in os.walk(repository):
            for file in files:
                if file.endswith('.jmx'):
                    print("usa Jmeter")
                    return True
        return False

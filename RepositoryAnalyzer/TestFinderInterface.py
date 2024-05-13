from abc import ABC, abstractmethod
import os


class TestDependencyFinderInterface(ABC):

    @abstractmethod
    def has_test_dependency(self, dependencies, repository, webrepository, repo_path):
        pass


class SeleniumTestDependencyFinder(TestDependencyFinderInterface, ABC):

    def has_test_dependency(self, dependencies, repository, webrepository, repo_path):
        if 'Java' in repository.languages:
            return SeleniumTestDependencyFinderJava().find_dependency(dependencies, webrepository, repo_path)
        if 'Python' in repository.languages:
            return SeleniumTestDependencyFinderPython().find_dependency(dependencies, webrepository, repo_path)
        if 'JavaScript' in repository.languages:
            return SeleniumTestDependencyFinderJavaScript().find_dependency(dependencies, webrepository, repo_path)
        if 'TypeScript' in repository.languages:
            return SeleniumTestDependencyFinderTypeScript().find_dependency(dependencies, webrepository, repo_path)


class ToolFinderForLanguage(ABC):

    @abstractmethod
    def find_dependency(self, dependency_list, webrepository, repo_path):
        pass


class SeleniumTestDependencyFinderJava(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'org.seleniumhq.selenium':
                path_list = self.find_import_selenium(repo_path)
                if len(path_list) > 0:
                    webrepository.set_is_selenium_tested_java(True)
                    webrepository.add_path_in_list(path_list)
                print("usa selenium")
                return True
        return False

    def find_import_selenium(self, directory):
        files_with_selenium_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.java'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r', encoding='utf-8') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'import org.openqa.selenium' in line:
                                files_with_selenium_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_selenium_import


class SeleniumTestDependencyFinderPython(ToolFinderForLanguage, ABC):

    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'selenium':
                path_list = self.find_import_selenium(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_selenium_tested_python(True)
                print("usa selenium")
                return True
        return False

    def find_import_selenium(self, directory):
        files_with_selenium_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'from selenium import' in line:
                                files_with_selenium_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_selenium_import


class SeleniumTestDependencyFinderJavaScript(ToolFinderForLanguage, ABC):

    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'selenium' or dependency[0] == 'selenium-webdriver':
                path_list = self.find_import_selenium(repo_path)
                if len(path_list) > 0:
                    webrepository.set_is_selenium_tested_javascript(True)
                    webrepository.add_path_in_list(path_list)
                print("usa selenium")
                return True
        return False

    def find_import_selenium(self, directory):
        files_with_selenium_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.js'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'require(\'selenium-webdriver\')' in line or 'import selenium' in line:
                                files_with_selenium_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_selenium_import


class SeleniumTestDependencyFinderTypeScript(ToolFinderForLanguage, ABC):

    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == '@types/selenium' or dependency[0] == '#types/selenium-webdriver':
                path_list = self.find_import_selenium(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_selenium_tested_typescript(True)
                    print("usa selenium")
                return True
        return False

    def find_import_selenium(self, directory):
        files_with_selenium_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.ts'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'from "selenium-webdriver"' in line:
                                files_with_selenium_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_selenium_import


class PlayWrightTestDependencyFinder(TestDependencyFinderInterface, ABC):

    def has_test_dependency(self, dependencies, repository, webrepository, repo_path):
        if 'Java' in repository.languages:
            return PlayWrightTestDependencyFinderJava().find_dependency(dependencies, webrepository, repo_path)
        if 'Python' in repository.languages:
            return PlayWrightTestDependencyFinderPython().find_dependency(dependencies, webrepository, repo_path)
        if 'JavaScript' in repository.languages:
            return PlayWrightTestDependencyFinderJavaScript().find_dependency(dependencies, webrepository, repo_path)
        if 'TypeScript' in repository.languages:
            return PlayWrightTestDependencyFinderTypeScript().find_dependency(dependencies, webrepository, repo_path)


class PlayWrightTestDependencyFinderJava(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'com.microsoft.playwright':
                path_list = self.find_import_playwright(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_playwright_tested_java(True)
                print("usa playwright")
                return True
        return False

    def find_import_playwright(self, directory):
        files_with_playwright_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.java'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'import com.microsoft.playwright' in line:
                                files_with_playwright_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_playwright_import


class PlayWrightTestDependencyFinderPython(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'playwright' or dependency[0] == 'pytest-playwright':
                path_list = self.find_import_playwright(repo_path)
                if len(path_list) > 0:
                    webrepository.set_is_playwright_tested_python(True)
                    webrepository.add_path_in_list(path_list)
                print("usa playwright")
                return True
        return False

    def find_import_playwright(self, directory):
        files_with_playwright_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'from playwright.async_api import' in line or 'from playwright.sync_api import' in line:
                                files_with_playwright_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_playwright_import


class PlayWrightTestDependencyFinderJavaScript(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'playwright':
                print("usa playwright")
                path_list = self.find_import_playwright(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_playwright_tested_javascript(True)
                return True

    def find_import_playwright(self, directory):
        files_with_playwright_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.js'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'from \'@playwright/test\'' in line:
                                files_with_playwright_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_playwright_import


class PlayWrightTestDependencyFinderTypeScript(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'playwright':
                print("usa playwright")
                path_list = self.find_import_playwright(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_playwright_tested_typescript(True)
                return True

    def find_import_playwright(self, directory):
        files_with_playwright_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.ts'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'from \'@playwright/test\'' in line:
                                files_with_playwright_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_playwright_import


class PuppeteerTestDependencyFinder(TestDependencyFinderInterface, ABC):

    def has_test_dependency(self, dependencies, repository, webrepository, repo_path):
        # if 'Java' in repository.languages:
        #    return PuppeteerTestDependencyFinderJava().find_dependency(dependencies, webrepository)
        if 'Python' in repository.languages:
            return PuppeteerTestDependencyFinderPython().find_dependency(dependencies, webrepository, repo_path)
        if 'JavaScript' in repository.languages:
            return PuppeteerTestDependencyFinderJavaScript().find_dependency(dependencies, webrepository, repo_path)
        if 'TypeScript' in repository.languages:
            return PuppeteerTestDependencyFinderTypeScript().find_dependency(dependencies, webrepository, repo_path)


'''
class PuppeteerTestDependencyFinderJava:
    def find_dependency(self, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'org.webjars.npm' and dependency[1] == 'puppeteer':
                webrepository.set_is_puppeteer_tested_java(True)
                print("usa puppeteer")
                return True
        return False
'''


class PuppeteerTestDependencyFinderPython(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'pyppeteer':
                path_list = self.find_import_puppeteer(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_puppeteer_tested_python(True)
                print("usa puppeteer")
                return True
        return False

    def find_import_puppeteer(self, directory):
        files_with_puppeteer_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'from pyppeteer import' in line:
                                files_with_puppeteer_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_puppeteer_import


class PuppeteerTestDependencyFinderJavaScript(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'puppeteer':
                path_list = self.find_import_puppeteer(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_puppeteer_tested_javascript(True)
                print("usa puppeteer")
                return True
        return False

    def find_import_puppeteer(self, directory):
        files_with_puppeteer_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'require(\'puppeteer\')' in line:
                                files_with_puppeteer_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_puppeteer_import


class PuppeteerTestDependencyFinderTypeScript(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == '@types/puppeteer':
                path_list = self.find_import_puppeteer(repo_path)
                if len(path_list) > 0:
                    webrepository.set_is_puppeteer_tested_typescript(True)
                    webrepository.add_path_in_list(path_list)
                print("usa puppeteer")
                return True
        return False

    def find_import_puppeteer(self, directory):
        files_with_puppeteer_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.ts'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'from \'puppeteer\'' in line:
                                files_with_puppeteer_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_puppeteer_import


class CypressTestDependencyFinder(TestDependencyFinderInterface, ABC):
    def has_test_dependency(self, dependencies, repository, webrepository, repo_path):
        if 'JavaScript' in repository.languages:
            return CypressTestDependencyFinderJavaScript().find_dependency(dependencies, webrepository, repo_path)
        if 'TypeScript' in repository.languages:
            return CypressTestDependencyFinderTypeScript().find_dependency(dependencies, webrepository, repo_path)


class CypressTestDependencyFinderJavaScript(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependencies, webrepository, repo_path):
        for dependency in dependencies:
            if dependency[0] == 'cypress':
                path_list = self.find_import_cypress(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_cypress_tested_javascript(True)
                print("usa cypress")
                return True
        return False

    def find_import_cypress(self, directory):
        files_with_cypress_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.cy.js'):
                    file_path = os.path.join(root, file_name)
                    files_with_cypress_import.append(file_path)
        return files_with_cypress_import


class CypressTestDependencyFinderTypeScript(ToolFinderForLanguage, ABC):
    def find_dependency(self, dependencies, webrepository, repo_path):
        for dependency in dependencies:
            if dependency[0] == 'cypress':
                path_list = self.find_import_cypress(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_cypress_tested_typescript(True)
                print("usa cypress")
                return True
        return False

    def find_import_cypress(self, directory):
        files_with_cypress_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.cy.ts'):
                    file_path = os.path.join(root, file_name)
                    files_with_cypress_import.append(file_path)
        return files_with_cypress_import


class LocustTestDependencyFinder(TestDependencyFinderInterface, ABC):
    def has_test_dependency(self, dependencies, repository, webrepository, repo_path):
        if 'Java' in repository.languages:
            return LocustTestDependencyFinderJava().find_dependency(dependencies, webrepository, repo_path)
        if 'Python' in repository.languages:
            return LocustTestDependencyFinderPython().find_dependency(dependencies, webrepository, repo_path)
        # if 'JavaScript' in repository.languages:
        #     return LocustTestDependencyFinderJavaScript().find_dependency(dependencies, webrepository)


class LocustTestDependencyFinderJava(ToolFinderForLanguage, ABC):

    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'com.github.myzhan' and dependency[1] == 'locust4j':
                path_list = self.find_import_locust(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                    webrepository.set_is_locust_tested_java(True)
                print("usa locust")
                return True
        return False

    def find_import_locust(self, directory):
        files_with_locust_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.java'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'import com.github.myzhan.locust4j' in line:
                                files_with_locust_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_locust_import


class LocustTestDependencyFinderPython(ToolFinderForLanguage, ABC):

    def find_dependency(self, dependency_list, webrepository, repo_path):
        for dependency in dependency_list:
            if dependency[0] == 'locust' or dependency[0] == 'locustio':
                webrepository.set_is_locust_tested_python(True)
                path_list = self.find_import_locust(repo_path)
                if len(path_list) > 0:
                    webrepository.add_path_in_list(path_list)
                print("usa locust")
                return True
        return False

    def find_import_locust(self, directory):
        files_with_locust_import = []

        # Attraversa ricorsivamente tutte le sottodirectory
        for root, dirs, files in os.walk(directory):
            for file_name in files:
                if file_name.endswith('.py'):
                    file_path = os.path.join(root, file_name)
                    with open(file_path, 'r') as file:
                        lines = file.readlines()
                        for line in lines:
                            # Verifica se la riga contiene un'importazione di Selenium
                            if 'from locust import' in line:
                                files_with_locust_import.append(file_path)
                                break  # Se l'importazione è stata trovata nel file, non è necessario cercare ulteriormente
        return files_with_locust_import


'''
class LocustTestDependencyFinderJavaScript:

    def find_dependency(self, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'locust':
                webrepository.set_is_locust_tested_javascript(True)
                print("usa locust")
                return True
        return False
'''


class JMeterTestDependencyFinder(TestDependencyFinderInterface, ABC):
    def has_test_dependency(self, dependencies, repository, webrepository, repo_path):
        ret = False
        for root, dirs, files in os.walk(repo_path):
            for file in files:
                if file.endswith('.jmx'):
                    webrepository.set_is_jmeter_tested(True)
                    ret = True
                    webrepository.test_path.append(os.path.join(root, file))
                    print("Usa JMeter")

        # if len(file_with_jmx_file) > 0:
        #    webrepository.add_path_in_list(file_with_jmx_file)

        return ret

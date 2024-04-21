from abc import ABC, abstractmethod


class TestDependencyFinderInterface(ABC):

    @abstractmethod
    def factory_test_dependency(self, repository):
        pass


class SeleniumDependencyFinderInterface(TestDependencyFinderInterface):

    def factory_test_dependency(self, repository):
        if repository.main_language == 'Java':
            if self.check_implementation(SeleniumDependencyFinderInJava):
                return SeleniumDependencyFinderInJava()
        elif repository.main_language == 'Python':
            if self.check_implementation(SeleniumDependencyFinderInPython):
                return SeleniumDependencyFinderInPython()
        elif repository.main_language == 'JavaScript':
            if self.check_implementation(SeleniumDependencyFinderInJavaScript):
                return SeleniumDependencyFinderInJavaScript()

    @classmethod
    def check_implementation(cls, subclass):
        required_methods = ['find_test_dependency_in_repository']
        for method_name in required_methods:
            if not hasattr(subclass, method_name) or not callable(getattr(subclass, method_name)):
                raise TypeError(f"Class {subclass.__name__} must implement method {method_name}")
        return True


class PlayWrightDependencyFinderInterface(TestDependencyFinderInterface):

    def factory_test_dependency(self, repository):
        if repository.main_language == 'Java':
            if self.check_implementation(PlayWrightDependencyFinderInJava):
                return PlayWrightDependencyFinderInJava()
        elif repository.main_language == 'Python':
            if self.check_implementation(PlayWrightDependencyFinderInPython):
                return PlayWrightDependencyFinderInPython()
        elif repository.main_language == 'JavaScript':
            if self.check_implementation(PlayWrightDependencyFinderInJavaScript):
                return PlayWrightDependencyFinderInJavaScript()

    @classmethod
    def check_implementation(cls, subclass):
        required_methods = ['find_test_dependency_in_repository']
        for method_name in required_methods:
            if not hasattr(subclass, method_name) or not callable(getattr(subclass, method_name)):
                raise TypeError(f"Class {subclass.__name__} must implement method {method_name}")
        return True


class PuppeteerDependencyFinderInterface(TestDependencyFinderInterface):

    def factory_test_dependency(self, repository):
        if repository.main_language == 'Java':
            if self.check_implementation(PuppeteerDependencyFinderInJava):
                return PuppeteerDependencyFinderInJava()
        elif repository.main_language == 'Python':
            if self.check_implementation(PuppeteerDependencyFinderInPython):
                return PuppeteerDependencyFinderInPython()
        elif repository.main_language == 'JavaScript':
            if self.check_implementation(PuppeteerDependencyFinderInJavaScript):
                return PuppeteerDependencyFinderInJavaScript()

    @classmethod
    def check_implementation(cls, subclass):
        required_methods = ['find_test_dependency_in_repository']
        for method_name in required_methods:
            if not hasattr(subclass, method_name) or not callable(getattr(subclass, method_name)):
                raise TypeError(f"Class {subclass.__name__} must implement method {method_name}")
        return True


class CypressDependencyFinderInterface(TestDependencyFinderInterface):
    def factory_test_dependency(self, repository):
        if repository.main_language == 'Java':
            if self.check_implementation(CypressDependencyFinderInJava):
                return CypressDependencyFinderInJava()
        if repository.main_language == 'Python':
            if self.check_implementation(CypressDependencyFinderInPython):
                return CypressDependencyFinderInPython()
        if repository.main_language == 'JavaScript':
            if self.check_implementation(CypressDependencyFinderInJavaScript):
                return CypressDependencyFinderInJavaScript()

    @classmethod
    def check_implementation(cls, subclass):
        required_methods = ['find_test_dependency_in_repository']
        for method_name in required_methods:
            if not hasattr(subclass, method_name) or not callable(getattr(subclass, method_name)):
                raise TypeError(f"Class {subclass.__name__} must implement method {method_name}")
        return True


class LocustDependencyFinderInterface(TestDependencyFinderInterface):
    def factory_test_dependency(self, repository):
        if repository.main_language == 'Java':
            if self.check_implementation(LocustDependencyFinderInJava):
                return LocustDependencyFinderInJava()
        elif repository.main_language == 'Python':
            if self.check_implementation(LocustDependencyFinderInPython):
                return LocustDependencyFinderInPython()
        elif repository.main_language == 'JavaScript':
            if self.check_implementation(LocustDependencyFinderInJavaScript):
                return LocustDependencyFinderInJavaScript()

    @classmethod
    def check_implementation(cls, subclass):
        required_methods = ['find_test_dependency_in_repository']
        for method_name in required_methods:
            if not hasattr(subclass, method_name) or not callable(getattr(subclass, method_name)):
                raise TypeError(f"Class {subclass.__name__} must implement method {method_name}")
        return True


class JMeterDependencyFinderInterface(TestDependencyFinderInterface):
    def factory_test_dependency(self, repository):
        if repository.main_language == 'Java':
            if self.check_implementation(JMeterDependencyFinderInJava):
                return JMeterDependencyFinderInJava()
        elif repository.main_language == 'Python':
            if self.check_implementation(JMeterDependencyFinderInPython):
                return JMeterDependencyFinderInPython()
        elif repository.main_language == 'JavaScript':
            if self.check_implementation(LocustDependencyFinderInJavaScript):
                return JMeterDependencyFinderInJavaScript()

    @classmethod
    def check_implementation(cls, subclass):
        required_methods = ['find_test_dependency_in_repository']
        for method_name in required_methods:
            if not hasattr(subclass, method_name) or not callable(getattr(subclass, method_name)):
                raise TypeError(f"Class {subclass.__name__} must implement method {method_name}")
        return True


class JMeterDependencyFinderInJavaScript(JMeterDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        import os
        for root, dirs, files in os.walk(repository):
            for file in files:
                if file.endswith('.jmx'):
                    webrepository.set_is_jmeter_tested(True)
                    print("Usa JMeter")
                    return True
        return False


class JMeterDependencyFinderInPython(JMeterDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):

        for dependency in dependency_list:
            if dependency[0] == 'pymeter':
                webrepository.set_is_jmeter_tested(True)
                print("usa Jmeter")
                return True

        import os
        for root, dirs, files in os.walk(repository):
            for file in files:
                if file.endswith('.jmx'):
                    webrepository.set_is_jmeter_tested(True)
                    print("Usa JMeter")
                    return True
        return False


class JMeterDependencyFinderInJava(JMeterDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        import os
        for root, dirs, files in os.walk(repository):
            for file in files:
                if file.endswith('.jmx'):
                    webrepository.set_is_jmeter_tested(True)
                    print("Usa JMeter")
                    return True
        return False


class LocustDependencyFinderInJava(LocustDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'com.github.myzhan' and dependency[1] == 'locust4j':
                webrepository.set_is_locust_tested(True)
                print("usa locust")
                return True
        return False


class LocustDependencyFinderInPython(LocustDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'locust':
                webrepository.set_is_locust_tested(True)
                print("usa locust")
                return True
        return False


class LocustDependencyFinderInJavaScript(LocustDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'locust':
                webrepository.set_is_locust_tested(True)
                print("usa locust")
                return True
        return False


class CypressDependencyFinderInJava(CypressDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        import os
        for root, dirs, files in os.walk(repository):
            if 'cypress.json' in files:
                webrepository.set_is_cypress_tested(True)
                print("usa cypress")
                return True
        return False


class CypressDependencyFinderInPython(CypressDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        import os
        for root, dirs, files in os.walk(repository):
            if 'cypress.json' in files:
                print("usa cypress")
                webrepository.set_is_cypress_tested(True)
                return True
        return False


class CypressDependencyFinderInJavaScript(CypressDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'cypress':
                webrepository.set_is_cypress_tested(True)
                print("usa cypress")
                return True
        return False


class PuppeteerDependencyFinderInJava(PuppeteerDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'org.webjars.npm' and dependency[1] == 'puppeteer':
                webrepository.set_is_puppeteer_tested(True)
                print("usa puppeteer")
                return True
        return False


class PuppeteerDependencyFinderInPython(PuppeteerDependencyFinderInterface):
    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'pyppeteer':
                webrepository.set_is_puppeteer_tested(True)
                print("usa puppeteer")
                return True
        return False


class PuppeteerDependencyFinderInJavaScript(PuppeteerDependencyFinderInterface):
    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'puppeteer':
                webrepository.set_is_puppeteer_tested(True)
                print("usa puppeteer")
                return True
        return False


class PlayWrightDependencyFinderInJavaScript(PlayWrightDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'playwright':
                webrepository.set_is_playwright_tested(True)
                print("usa playwright")
                return True
        return False


class PlayWrightDependencyFinderInJava(PlayWrightDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'com.microsoft.playwright':
                webrepository.set_is_playwright_tested(True)
                print("usa playwright")
                return True
        return False


class PlayWrightDependencyFinderInPython(PlayWrightDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'pytest-playwright':
                webrepository.set_is_playwright_tested(True)
                print("usa playwright")
                return True
        return False


class SeleniumDependencyFinderInJava(SeleniumDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'org.seleniumhq.selenium':
                webrepository.set_is_selenium_tested(True)
                print("usa selenium")
                return True
        return False


class SeleniumDependencyFinderInPython(SeleniumDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'selenium':
                webrepository.set_is_selenium_tested(True)
                print("usa selenium")
                return True
        return False


class SeleniumDependencyFinderInJavaScript(SeleniumDependencyFinderInterface):

    def find_test_dependency_in_repository(self, repository, dependency_list, webrepository):
        for dependency in dependency_list:
            if dependency[0] == 'selenium':
                webrepository.set_is_selenium_tested(True)
                print("usa selenium")
                return True
        return False

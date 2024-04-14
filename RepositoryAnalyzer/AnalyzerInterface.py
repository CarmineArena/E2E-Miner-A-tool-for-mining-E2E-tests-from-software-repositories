from abc import ABC, abstractmethod

# from RepositoryAnalyzer.Analyzer import JavaDependencyFinder


class Analyzer(ABC):
    @abstractmethod
    def analyze_all_repository(self):
        pass


class DependencyFileFinderInterface(ABC):
    @abstractmethod
    def find_dependency_file(self, repository):
        pass

    @staticmethod
    def factory_finder(main_language):
        if main_language == 'Java':
            from RepositoryAnalyzer.Analyzer import JavaDependencyFileFinder
            return JavaDependencyFileFinder()

        elif main_language == 'Python':
            from RepositoryAnalyzer.Analyzer import PythonDependencyFileFinder
            return PythonDependencyFileFinder()

        elif main_language == 'JavaScript':
            from RepositoryAnalyzer.Analyzer import JavaScriptDependencyFileFinder
            return JavaScriptDependencyFileFinder()
        else:
            raise ValueError("Linguaggio non ancora implementato")

class WebAnalyzerInterface(ABC):

    @abstractmethod
    def find_web_dependency(self, dependency_list):
        pass
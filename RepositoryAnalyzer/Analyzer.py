import json
import os
import queue
import threading
import re
import time
from lxml import etree
from abc import ABC, abstractmethod

from RepositoryAnalyzer.AnalyzerInterface import Analyzer, DependencyFileFinderInterface, WebAnalyzerInterface
from RepositoryAnalyzer.RepositoryCloner import Cloner
from RepositoryAnalyzer.TestFinder import SeleniumFinder, PuppeteerFinder, PlayWrightFinder, CypressFinder, \
    LocustFinder, JMeterFinder
from RepositoryAnalyzer.TestFinderInterface import SeleniumDependencyFinderInterface, \
    PlayWrightDependencyFinderInterface, PuppeteerDependencyFinderInterface, CypressDependencyFinderInterface, \
    LocustDependencyFinderInterface, JMeterDependencyFinderInterface


class AnalyzerController(Analyzer, ABC):
    def __init__(self, repository, max_threads=10, output_folder=r"C:\rep"):
        self.repository = repository
        self.max_threads = max_threads
        self.output_folder = output_folder
        self.repositories_queue = self.create_repositories_queue(repository)
        self.lock = threading.Lock()
        self.test_dependency = [SeleniumDependencyFinderInterface(), PlayWrightDependencyFinderInterface(),
                                PuppeteerDependencyFinderInterface(), CypressDependencyFinderInterface(),
                                LocustDependencyFinderInterface(), JMeterDependencyFinderInterface()]

    def create_repositories_queue(self, repositories):
        q = queue.Queue()
        for item in repositories:
            q.put(item)
        return q

    def analyze_all_repository(self):
        while True:
            with self.lock:
                if self.repositories_queue.empty():
                    break
                repository_to_analyze = self.repositories_queue.get()
            repository = str(repository_to_analyze[0]) if repository_to_analyze[0] else ''

            print(repository)

            print(f"analyzing {repository}...")

            # mettilo in un metodo
            cloner = Cloner(self.output_folder)
            cloned_repository = cloner.clone_repository(repository)

            repository_analyzer = DependencyFileFinderInterface.factory_finder(repository_to_analyze[1])
            dependencies = repository_analyzer.find_dependency_file(cloned_repository)

            # interfaccia di analisi di una repository -> quindi fare metodi per cercare file delle dipendenze e altro

            # fai interfaccia + factory method

            # if WebAnalyzer.is_web_repository(repository_to_analyze, dependencies):
            web_list = WebDependencyListCreator(repository_to_analyze).trasport_file_dependencies_in_list()
            if WebAnalyzer().has_web_dependencies(web_list, dependencies):
                print(repository + "è web")
                for dependency in self.test_dependency:
                    if dependency.factory_test_dependency(repository_to_analyze).find_test_dependency_in_repository(
                            repository, dependencies):
                        print(repository + "è web tested")

            time.sleep(1)
            self.repositories_queue.task_done()

    def analyze_repositories(self):
        threads = []
        for i in range(self.max_threads):
            print("sto creando il thread numero " + str(i))
            thread = threading.Thread(target=self.analyze_all_repository, )
            thread.start()
            threads.append(thread)
            time.sleep(1)

        for thread in threads:
            print("nel secondo for")
            thread.join()


class WebDependencyListCreator:
    def __init__(self, repository):
        if (repository[1]) == 'Java':
            self.txt_file_with_dependencies = r"C:\Users\carmi\PycharmProjects\MiningRepositorySoftware\RepositoryAnalyzer\WebJavaDependency.txt"
        elif (repository[1]) == 'Python':
            self.txt_file_with_dependencies = r"C:\Users\carmi\PycharmProjects\MiningRepositorySoftware\RepositoryAnalyzer\WebPythonDependency.txt"
        elif (repository[1]) == 'JavaScript':
            self.txt_file_with_dependencies = r"C:\Users\carmi\PycharmProjects\MiningRepositorySoftware\RepositoryAnalyzer\WebJSDependency.txt"

    def trasport_file_dependencies_in_list(self):
        list_web = []
        with open(self.txt_file_with_dependencies, 'r') as file:
            # Leggo ogni riga del file, rimuovo il carattere di nuova riga e le metto in una lista
            lines = [line.strip() for line in file.readlines()]

        # Aggiungo ogni riga (senza il carattere di nuova riga) alla lista
        for line in lines:
            list_web.append(line.lower())

        print(list_web)
        return list_web


class WebAnalyzer:

    def has_web_dependencies(self, web_dependencies_list, repository_dependencies):
        for web_dependency in web_dependencies_list:
            for dependency in repository_dependencies:
                if dependency[0] == web_dependency:
                    return True
        return False


class DependencyFinderInterface(ABC):
    @abstractmethod
    def find_dependency(self, dependency_file, dependency_list):
        pass

    @abstractmethod
    def add_dependency_in_list(self, dependency, dependency_list):
        pass

    @staticmethod
    def factory_analyzer(dependency_file):
        if 'pom.xml' in dependency_file or 'build.gradle' in dependency_file:
            return JavaDependencyFinder()
        elif 'requirements' in dependency_file:
            return PythonDependencyFinder()
        elif 'package.json' in dependency_file or 'package-lock.json' in dependency_file:
            return  JavaScriptDependencyFinder()


class JavaScriptDependencyFileFinder(DependencyFileFinderInterface, ABC):
    def find_dependency_file(self, repository):
        dependencies = []
        print("vedo questo ->" + str(repository))
        for root, dirs, files in os.walk(repository):
            if 'package.json' in files:
                json_file = os.path.join(root, 'package.json')
                analyzer = DependencyFinderInterface.factory_analyzer(json_file)
                dependencies = analyzer.find_dependency(json_file, dependencies)
            if 'package-lock.json' in files:
                json_file = os.path.join(root, 'package-lock.json')
                analyzer = DependencyFinderInterface.factory_analyzer(json_file)
                dependencies = analyzer.find_dependency(json_file, dependencies)
        return dependencies


class PythonDependencyFileFinder(DependencyFileFinderInterface, ABC):
    def find_dependency_file(self, repository):
        dependencies = []
        print("vedo questo ->" + str(repository))
        for root, dirs, files in os.walk(repository):
            for file in files:
                if file.endswith('.txt') and file.startswith('requirements'):
                    txtfile = os.path.join(root, file)
                    analyzer = DependencyFinderInterface.factory_analyzer(txtfile)
                    dependencies = analyzer.find_dependency(txtfile, dependencies)
            # if 'requirements.txt' in files:
            #    txtfile = os.path.join(root, 'requirements.txt')
            #    analyzer = DependencyFinderInterface.factory_analyzer(txtfile)
            #    dependencies = analyzer.find_dependency(txtfile, dependencies)
        return dependencies


class JavaDependencyFileFinder(DependencyFileFinderInterface, ABC):

    def find_dependency_file(self, repository):
        dependencies = []
        print("vedo questo ->" + str(repository))
        for root, dirs, files in os.walk(repository):
            if 'build.gradle' in files:
                gradle_file = os.path.join(root, 'build.gradle')
                analyzer = DependencyFinderInterface.factory_analyzer(gradle_file)
                dependencies = analyzer.find_dependency(gradle_file, dependencies)
                # break  # Interrompi la ricerca se viene trovato build.gradle

            elif 'pom.xml' in files:
                pom_file = os.path.join(root, 'pom.xml')
                analyzer = DependencyFinderInterface.factory_analyzer(pom_file)
                dependencies = analyzer.find_dependency(pom_file, dependencies)
                # break  # Interrompi la ricerca se viene trovato pom.xml

        return dependencies


class JavaScriptDependencyFinder(DependencyFinderInterface, ABC):
    def add_dependency_in_list(self, dependency, dependency_list):
        if dependency not in dependency_list:
            dependency_list.append(dependency)

    def find_dependency(self, dependency_file, dependency_list):
        with open(dependency_file, 'r') as file:
            data = json.load(file)
            # Definisci il pattern regex per estrarre il nome del pacchetto
            pattern = r'^@?([^/]+)'

            # Controlla se il file contiene una sezione "dependencies"
            if 'dependencies' in data:
                for dependency, version in data['dependencies'].items():
                    # Cerca il pattern nella dipendenza
                    match = re.match(pattern, dependency)
                    if match:
                        # Aggiungi il nome del pacchetto alla lista delle dipendenze
                        self.add_dependency_in_list((match.group(1), version), dependency_list)

            # Controlla se il file contiene una sezione "devDependencies" (dipendenze di sviluppo)
            if 'devDependencies' in data:
                for dependency, version in data['devDependencies'].items():
                    # Cerca il pattern nella dipendenza
                    match = re.match(pattern, dependency)
                    if match:
                        # Aggiungi il nome del pacchetto alla lista delle dipendenze
                        self.add_dependency_in_list((match.group(1), version), dependency_list)

        return dependency_list


class PythonDependencyFinder(DependencyFinderInterface, ABC):

    def add_dependency_in_list(self, dependency, dependency_list):
        if dependency not in dependency_list:
            dependency_list.append(dependency)

    def find_dependency(self, dependency_file, dependency_list):
        print("reading... " + dependency_file)
        with open(dependency_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):  # Ignora commenti e linee vuote
                    if '==' in line:
                        dependency, version = line.split('==')
                    elif '>=' in line:
                        dependency, version = line.split('>=')
                    elif '<=' in line:
                        dependency, version = line.split('<=')
                    else:
                        dependency = line
                        version = ''  # Assegna una stringa vuota alla versione
                    self.add_dependency_in_list((dependency.strip(), version.strip()), dependency_list)
        return dependency_list


class JavaDependencyFinder(DependencyFinderInterface, ABC):

    def add_dependency_in_list(self, dependency, dependency_list):
        if dependency not in dependency_list:
            dependency_list.append(dependency)

    def find_dependency(self, dependency_file, dependency_list):
        if 'build.gradle' in dependency_file:
            return self.analyze_gradle_file(dependency_file, dependency_list)
        elif 'pom.xml' in dependency_file:
            return self.analyze_pom_file(dependency_file, dependency_list)

    def analyze_gradle_file(self, gradle_file, dependency_list):
        with open(gradle_file, 'r') as file:
            # Cerca le dipendenze nel file Gradle
            gradle_content = file.read()
            pattern = re.compile(r"(['\"])(.*?):(.*?):(.*?)\1")
            matches = pattern.findall(gradle_content)
            print("reading " + gradle_file + "...")
            for match in matches:
                group_id, artifact_id, version = match[1:]
                self.add_dependency_in_list((group_id, artifact_id, version), dependency_list)

        return dependency_list

    def analyze_pom_file(self, pom_file, dependency_list):
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(pom_file, parser=parser)
        root = tree.getroot()

        if root is not None:
            # Trova tutte le dipendenze nel file pom.xml

            for dependency in root.findall('.//{http://maven.apache.org/POM/4.0.0}dependency'):
                group_id_element = dependency.find('{http://maven.apache.org/POM/4.0.0}groupId')
                artifact_id_element = dependency.find('{http://maven.apache.org/POM/4.0.0}artifactId')
                version_element = dependency.find('{http://maven.apache.org/POM/4.0.0}version')

                # Verifica se gli elementi sono stati trovati prima di accedere al loro attributo 'text'
                group_id = group_id_element.text if group_id_element is not None else "GroupId non trovato"
                artifact_id = artifact_id_element.text if artifact_id_element is not None else "ArtifactId non trovato"
                version = version_element.text if version_element is not None else "Version non trovata"
                # print("aggiunti" + group_id + artifact_id + version)
                self.add_dependency_in_list((group_id, artifact_id, version), dependency_list)

        return dependency_list

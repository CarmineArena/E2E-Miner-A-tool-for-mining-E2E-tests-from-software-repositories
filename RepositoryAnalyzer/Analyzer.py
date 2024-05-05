import errno
import json
import os
import queue
import shutil
import stat
import subprocess
import threading
import re
import time
import git
from lxml import etree
from abc import ABC, abstractmethod
import logging

logger = logging.getLogger(__name__)
logging.basicConfig(filename='example.log', encoding='utf-8', level=logging.INFO)

from Dataset.Repository import WebRepository, WebRepositoryDAO
from RepositoryAnalyzer.AnalyzerInterface import Analyzer, DependencyFileFinderInterface, WebAnalyzerInterface
from RepositoryAnalyzer.RepositoryCloner import Cloner

from RepositoryAnalyzer.TestFinderInterface import SeleniumTestDependencyFinder, \
    PlayWrightTestDependencyFinder, PuppeteerTestDependencyFinder, CypressTestDependencyFinder, \
    LocustTestDependencyFinder, JMeterTestDependencyFinder


def handle_remove_readonly(func, path, exc):
    excvalue = exc[1]
    if func in (os.rmdir, os.remove, os.unlink) and excvalue.errno == errno.EACCES:
        os.chmod(path, stat.S_IRWXU | stat.S_IRWXG | stat.S_IRWXO)  # 0777
        func(path)
    else:
        raise


class AnalyzerController(Analyzer, ABC):
    def __init__(self, repository, max_threads=10, output_folder=r"C:\re"):
        self.repository = repository
        self.max_threads = max_threads
        self.output_folder = output_folder
        self.repositories_queue = self.create_repositories_queue(repository)
        self.lock = threading.Lock()
        self.language_to_analyze = ["Java", "Python", "JavaScript"]
        self.test_dependency = [SeleniumTestDependencyFinder(), PlayWrightTestDependencyFinder(),
                                PuppeteerTestDependencyFinder(), CypressTestDependencyFinder(),
                                LocustTestDependencyFinder(), JMeterTestDependencyFinder()]

    def create_repositories_queue(self, repositories):
        q = queue.Queue()
        c = 0
        for item in repositories:
            q.put(item)
            c += 1
        print("coda lunga " + str(c))
        return q

    def analyze_all_repository(self):
        while True:
            with self.lock:
                if self.repositories_queue.empty():
                    break
                repository_to_analyze = self.repositories_queue.get()
                logging.info("ho preso dalla coda " + repository_to_analyze.name)

            print(repository_to_analyze.name)

            print(f"analyzing {repository_to_analyze.name}...")

            cloner = Cloner(self.output_folder)
            cloned_repository = cloner.clone_repository(repository_to_analyze.name)
            dependencies = []
            for language in self.language_to_analyze:
                repository_analyzer = DependencyFileFinderInterface.factory_finder(language)
                dependencies = repository_analyzer.find_dependency_file(cloned_repository, dependencies)
                print("dipendenze per " + repository_to_analyze.name)
                print(dependencies)

            webrepository = WebRepository(repository_to_analyze.ID, repository_to_analyze.name)

            # if WebAnalyzer.is_web_repository(repository_to_analyze, dependencies):
            for language in self.language_to_analyze:
                web_list = WebDependencyListCreator(language).trasport_file_dependencies_in_list()
                if WebAnalyzer().has_web_dependencies(web_list, dependencies):
                    WebFlags().change_flag(language, webrepository)

            if WebFlags().check_flag(webrepository):
                print(repository_to_analyze.name + "è web")

                for dependency in self.test_dependency:
                    if dependency.find_test_dependency(dependencies, repository_to_analyze, webrepository,
                                                       cloned_repository):
                        print("trovata una dipendenza test")

                with self.lock:
                    WebRepositoryDAO(webrepository).add_web_repository_to_db()

            else:
                shutil.rmtree(cloned_repository, ignore_errors=False, onerror=handle_remove_readonly)

            with self.lock:
                repository_to_analyze.update_processed_repository()

            self.repositories_queue.task_done()

    '''
            if WebAnalyzer().has_web_dependencies(web_list, dependencies):
                print(repository_to_analyze.name + "è web")

                for dependency in self.test_dependency:
                    if dependency.factory_test_dependency(repository_to_analyze).find_test_dependency_in_repository(
                            cloned_repository, dependencies, webrepository):
                        print(repository_to_analyze.name + "è web tested")
                print(webrepository.name + " oggetto creato correttamente")
                with self.lock:
                    WebRepositoryDAO(webrepository).add_web_repository_to_db()
            else:
                shutil.rmtree(cloned_repository, ignore_errors=False, onerror=handle_remove_readonly)
                self.repositories_queue.task_done()
                # repo = git.Repo(cloned_repository)
                # repo.git.execute(['git', 'rm', '-rf', cloned_repository])
                # time.sleep(5)
                # shutil.rmtree(cloned_repository)
    '''

    def analyze_repositories(self):

        # Definisci il comando da eseguire per disattivare core.protectNTFS
        command = ["git", "config", "--global", "core.protectNTFS", "false"]

        # Esegui il comando
        subprocess.run(command)

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
    def __init__(self, language):
        if language == 'Java':
            self.txt_file_with_dependencies = r"C:\Users\carmi\PycharmProjects\DataMiningRepositorySoftware\RepositoryAnalyzer\WebJavaDependency.txt"
        elif language == 'Python':
            self.txt_file_with_dependencies = r"C:\Users\carmi\PycharmProjects\DataMiningRepositorySoftware\RepositoryAnalyzer\WebPythonDependency.txt"
        elif language == 'JavaScript':
            self.txt_file_with_dependencies = r"C:\Users\carmi\PycharmProjects\DataMiningRepositorySoftware\RepositoryAnalyzer\WebJSDependency.txt"

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


class WebFlags:
    def change_flag(self, language, webrepository):
        if language == 'Java':
            webrepository.set_is_web_java(True)
        if language == 'Python':
            webrepository.set_is_web_python(True)
        if language == 'JavaScript':
            webrepository.set_is_web_javascript(True)

    def check_flag(self, webrepository):
        if webrepository.is_web_java or webrepository.is_web_python or webrepository.is_web_javascript:
            return True
        return False


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

    @staticmethod
    def add_dependency_in_list(dependency, dependency_list):
        if dependency not in dependency_list:
            dependency_list.append(dependency)

    @staticmethod
    def factory_analyzer(dependency_file):
        if 'pom.xml' in dependency_file or 'build.gradle' in dependency_file:
            return JavaDependencyFinder()
        elif 'requirements' in dependency_file:
            return PythonDependencyFinder()
        elif 'package.json' in dependency_file or 'package-lock.json' in dependency_file:
            return JavaScriptDependencyFinder()


class JavaScriptDependencyFileFinder(DependencyFileFinderInterface, ABC):
    def find_dependency_file(self, repository, dependencies):
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
    def find_dependency_file(self, repository, dependencies):
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

    def find_dependency_file(self, repository, dependencies):
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

    def find_dependency(self, dependency_file, dependency_list):
        if 'package.json' in dependency_file:
            return self.analyze_package_file(dependency_file, dependency_list)
        elif 'package-lock.json' in dependency_file:
            return self.analyze_packagelock_file(dependency_file, dependency_list)

    def analyze_package_file(self, dependency_file, dependency_list):
        try:
            with open(dependency_file, 'r', encoding='utf-8') as file:
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
        except json.JSONDecodeError as e:
            print("file malformato-> ")
            print(e)
            return dependency_list

        print(dependency_list)
        print("ho analizzato " + str(dependency_file))
        return dependency_list

    def analyze_packagelock_file(self, dependency_file, dependency_list):
        try:
            with open(dependency_file, 'r', encoding='utf-8') as file:
                lockfile = json.load(file)
        except json.JSONDecodeError as e:
            print("file malformato-> ")
            print(e)
            return dependency_list

        def process_dependencies(dependencies):
            for package_name, package_details in dependencies.items():
                version = package_details.get('version', 'version not found')
                self.add_dependency_in_list((self.get_package_name(package_name), version), dependency_list)
                if 'dependencies' in package_details:
                    process_dependencies(package_details['dependencies'])

        if 'dependencies' in lockfile:
            process_dependencies(lockfile['dependencies'])

        if 'devDependencies' in lockfile:
            process_dependencies(lockfile['devDependencies'])
        print(dependency_list)
        return dependency_list

    def get_package_name(self, full_name):
        # Rimuove il carattere '@' e prende solo la parte del nome del pacchetto prima del carattere '/'
        return full_name.lstrip('@').split('/')[0]

'''
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

print(dependency_list)
return dependency_list
'''


class PythonDependencyFinder(DependencyFinderInterface, ABC):

    def find_dependency(self, dependency_file, dependency_list):
        print("reading... " + dependency_file)
        with open(dependency_file, 'r') as file:
            lines = file.readlines()
            for line in lines:
                line = line.strip()
                if line and not line.startswith('#'):  # Ignora commenti e linee vuote
                    if '==' in line:
                        dependency, version = line.split('==', 1)
                    elif '>=' in line:
                        dependency, version = line.split('>=', 1)
                    elif '<=' in line:
                        dependency, version = line.split('<=', 1)
                    else:
                        dependency = line
                        version = ''  # Assegna una stringa vuota alla versione
                    self.add_dependency_in_list((dependency.strip(), version.strip()), dependency_list)
        return dependency_list


class JavaDependencyFinder(DependencyFinderInterface, ABC):

    def find_dependency(self, dependency_file, dependency_list):
        if 'build.gradle' in dependency_file:
            return self.analyze_gradle_file(dependency_file, dependency_list)
        elif 'pom.xml' in dependency_file:
            return self.analyze_pom_file(dependency_file, dependency_list)

    def analyze_gradle_file(self, gradle_file, dependency_list):
        print("vedo il file gradle di " + gradle_file)
        logging.info("vedo il file gradle di " + gradle_file)
        with open(gradle_file, 'r', encoding='utf-8') as file:
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
        '''
        parser = etree.XMLParser(recover=True)
        tree = etree.parse(pom_file, parser=parser)
        root = tree.getroot()
        print("vedo il file pom di " + pom_file)

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
                
        '''
        '''
        if root is not None:
            # Trova tutte le dipendenze nel file pom.xml
            for dependency in root.findall('.//{*/}dependency'):
                # Trova gli elementi groupId, artifactId e version indipendentemente dal namespace
                group_id_element = dependency.find('.//{*/}groupId')
                artifact_id_element = dependency.find('.//{*/}artifactId')
                version_element = dependency.find('.//{*/}version')

                # Estrai il testo dagli elementi se presenti
                group_id = group_id_element.text.strip() if group_id_element is not None else "GroupId non trovato"
                artifact_id = artifact_id_element.text.strip() if artifact_id_element is not None else "ArtifactId non trovato"
                version = version_element.text.strip() if version_element is not None else "Version non trovata"

                # Aggiungi la dipendenza alla lista
                self.add_dependency_in_list((group_id, artifact_id, version), dependency_list)
        '''
        logging.info("sto analizzando " + pom_file)
        print("vedo il file pom di " + pom_file)
        '''
        root = etree.parse(pom_file).getroot()
        tree = etree.ElementTree(root)

        depend = tree.xpath("//*[local-name()='dependency']")

        for dep in depend:
            infoDict = {}
            for child in dep.getchildren():
                tag = child.tag.split('}')[1]
                text = child.text
                infoDict[tag] = text

            dependency_list.append((infoDict.get('groupId'), infoDict.get('artifactId'), infoDict.get('version')))
        '''
        from lxml import etree

        try:
            root = etree.parse(pom_file).getroot()
            tree = etree.ElementTree(root)

            depend = tree.xpath("//*[local-name()='dependency']")

            for dep in depend:
                infoDict = {}
                for child in dep.getchildren():
                    tag = child.tag
                    if isinstance(tag, str) and '}' in tag:
                        tag = tag.split('}')[1]
                    text = child.text
                    infoDict[tag] = text

                dependency_list.append((infoDict.get('groupId'), infoDict.get('artifactId'), infoDict.get('version')))

            return dependency_list

        except Exception as e:
            logging.warning("eccezione nel file " + pom_file + ": " + str(e))
            print("eccezione nel file " + pom_file + ": " + str(e))
            return dependency_list

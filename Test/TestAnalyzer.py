
import time
import unittest
import os
from queue import Queue
from unittest.mock import  patch

from RepositoryAnalyzer.Analyzer import JavaDependencyAnalyzer

'''
class TestRepositoryAnalyzer(unittest.TestCase):

    def setUp(self):
        # Crea una cartella temporanea vuota
        self.temp_folder = tempfile.mkdtemp()
        print(self.temp_folder)

    def tearDown(self):
        # Elimina la cartella temporanea dopo il test
        shutil.rmtree(self.temp_folder)

    def test_analyze_all_empty_folder(self):
        # Usa la cartella temporanea creata per il test
        your_instance = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=2)
        your_instance.analyze_repository = MagicMock()  # Mock il metodo analyze_repository
        your_instance.analyze_all()
        your_instance.analyze_repository.assert_not_called()

    def test_analyze_all_with_repositories(self):
        # Crea dei repository finti nella cartella temporanea
        fake_repo1 = os.path.join(self.temp_folder, 'repo1')
        os.makedirs(fake_repo1)
        fake_repo2 = os.path.join(self.temp_folder, 'repo2')
        os.makedirs(fake_repo2)
        fake_repo3 = os.path.join(self.temp_folder, 'repo3')
        os.makedirs(fake_repo3)

        # Utilizza la cartella temporanea creata per il test
        your_instance = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=2)
        your_instance.analyze_repository = MagicMock(return_value=None)
        your_instance.analyze_all()
        self.assertEqual(your_instance.analyze_repository.call_count, 3)  # Numero di repository creati

    @patch('RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.analyze_pom_file')
    def test_analyze_repository_pom(self, mock_analyze_pom_file):
        # Configura il mock per restituire dipendenze fittizie
        mock_analyze_pom_file.return_value = ['dependency1', 'dependency2']

        fake_repo_path = os.path.join(self.temp_folder, 'fake_repo')
        os.makedirs(fake_repo_path)
        fake_pom_path = os.path.join(fake_repo_path, 'pom.xml')
        with open(fake_pom_path, 'w') as pom_file:
            pom_file.write('<xml>...</xml>')

        # Istanzia JavaDependencyAnalyzer utilizzando la repository fittizia
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=2)

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository(fake_repo_path)

        # Verifica che il mock sia stato chiamato correttamente
        mock_analyze_pom_file.assert_called_once_with(fake_repo_path, fake_pom_path, [])

    @patch('RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.analyze_gradle_file')
    def test_analyze_repository_gradle(self, mock_analyze_gradle_file):
        # Configura il mock per restituire dipendenze fittizie
        mock_analyze_gradle_file.return_value = ['dependency1', 'dependency2']

        fake_repo_path = os.path.join(self.temp_folder, 'fake_repo')
        os.makedirs(fake_repo_path)
        fake_gradle_path = os.path.join(fake_repo_path, 'build.gradle')
        with open(fake_gradle_path, 'w') as gradle_file:
            gradle_file.write('dependencies {....}')

        # Istanzia JavaDependencyAnalyzer utilizzando la repository fittizia
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=2)

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository(fake_repo_path)

        # Verifica che il mock sia stato chiamato correttamente
        mock_analyze_gradle_file.assert_called_once_with(fake_repo_path, fake_gradle_path, [])

    @patch('RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_web_repository')
    def test_analyze_repository_web(self, mock_is_web_repository):
        # Configura l'istanza di JavaDependencyAnalyzer
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=5)

        # Configura i mock per i metodi is_web_repository e is_tested_repository
        mock_is_web_repository.return_value = True

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository('fake_repository')

        # Verifica che i metodi is_web_repository e is_tested_repository siano stati chiamati correttamente
        mock_is_web_repository.assert_called_once()

    @patch('RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_web_repository')
    @patch('RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_tested_repository')
    def test_analyze_repository(self, mock_is_tested_repository, mock_is_web_repository):
        # Configura l'istanza di JavaDependencyAnalyzer
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=5)

        # Configura i mock per i metodi is_web_repository e is_tested_repository
        mock_is_tested_repository.return_value = True

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository('fake_repository')

        # Verifica che i metodi is_web_repository e is_tested_repository siano stati chiamati correttamente
        mock_is_tested_repository.assert_called_once()

    @patch('RepositoryAnalyzer.Analyzer.etree.parse')
    def test_analyze_pom_file(self, mock_parse):
        fake_folder = os.path.join(self.temp_folder, 'fake')
        os.makedirs(fake_folder)

        # Crea il file pom.xml fittizio all'interno della cartella fake
        fake_pom_path = os.path.join(fake_folder, 'pom.xml')
        with open(fake_pom_path, 'w') as pom_file:
            pom_file.write(
                '<project><dependencies><dependency><groupId>test_group</groupId><artifactId>test_artifact</artifactId><version>1.0</version></dependency></dependencies></project>')

        # Configura il mock per restituire un oggetto XML fittizio
        mock_root = MagicMock()
        mock_parse.return_value.getroot.return_value = mock_root

        # Configura il mock per il metodo findall
        mock_dependency = MagicMock()

        # Configura il mock per il groupId
        mock_group_id = MagicMock()
        mock_group_id.text = 'test_group'
        mock_dependency.find.return_value = mock_group_id

        # Configura il mock per il artifactId
        mock_artifact_id = MagicMock()
        mock_artifact_id.text = 'test_artifact'
        mock_dependency.find.side_effect = [mock_group_id, mock_artifact_id]

        # Configura il mock per il version
        mock_version = MagicMock()
        mock_version.text = '1.0'
        mock_dependency.find.side_effect = [mock_group_id, mock_artifact_id, mock_version]

        mock_root.findall.return_value = [mock_dependency]

        # Istanzia JavaDependencyAnalyzer con la cartella fake e il numero massimo di thread
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=5)

        # Esegui il metodo analyze_pom_file
        dependencies = []
        result = analyzer.analyze_pom_file(self.temp_folder, os.path.join(fake_folder, 'pom.xml'), dependencies)

        # Verifica che le dipendenze siano state aggiunte correttamente
        expected_dependencies = [('test_group', 'test_artifact', '1.0')]
        self.assertEqual(expected_dependencies, result)

    @patch('RepositoryAnalyzer.Analyzer.etree.parse')
    def test_analyze_gradle_file(self, mock_parse):
        fake_folder = os.path.join(self.temp_folder, 'fake')
        os.makedirs(fake_folder)

        # Crea il file gradle fittizio all'interno della cartella fake
        fake_gradle_path = os.path.join(fake_folder, 'build.gradle')
        with open(fake_gradle_path, 'w') as gradle_file:
            gradle_file.write("dependencies {\n\timplementation 'group:artifact:1.0'\n}")

        mock_root = MagicMock()
        mock_parse.return_value.getroot.return_value = mock_root

        # Configura il mock per il metodo findall
        mock_dependency = MagicMock()
        mock_group_id = MagicMock()
        mock_group_id.text = 'group'
        mock_dependency.find.return_value = mock_group_id

        mock_artifact_id = MagicMock()
        mock_artifact_id.text = 'artifact'
        mock_dependency.find.side_effect = [mock_group_id, mock_artifact_id]

        mock_version = MagicMock()
        mock_version.text = '1.0'
        mock_dependency.find.side_effect = [mock_group_id, mock_artifact_id, mock_version]

        mock_root.findall.return_value = [mock_dependency]

        # Istanzia JavaDependencyAnalyzer con la cartella fake e il numero massimo di thread
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=5)

        # Esegui il metodo analyze_pom_file
        dependencies = []
        result = analyzer.analyze_gradle_file(self.temp_folder, os.path.join(fake_folder, 'build.gradle'), dependencies)

        # Verifica che le dipendenze siano state aggiunte correttamente
        expected_dependencies = [('group', 'artifact', '1.0')]
        self.assertEqual(expected_dependencies, result)

    def test_is_tested_repository_with_testing_dependencies(self):
        # Configura l'istanza di JavaDependencyAnalyzer con alcune dipendenze di testing
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=5,
                                          testing_tools=['org.junit', 'org.mockito'])

        # Dipendenze con uno strumento di testing
        dependencies_with_testing = [('group', 'artifact', '1.0'), ('org.junit', 'junit', '4.12')]

        # Verifica che il metodo restituisca True quando ci sono dipendenze di testing
        result = analyzer.is_tested_repository(dependencies_with_testing)
        self.assertTrue(result)

    def test_is_not_tested_repository_with_testing_dependencies(self):
        # Configura l'istanza di JavaDependencyAnalyzer con alcune dipendenze di testing
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=5,
                                          testing_tools=['org.junit', 'org.mockito'])

        # Dipendenze con uno strumento di testing
        dependencies_with_testing = [('group', 'artifact', '1.0'), ('not_org.junit', 'not_junit', '4.12')]

        # Verifica che il metodo restituisca True quando ci sono dipendenze di testing
        result = analyzer.is_tested_repository(dependencies_with_testing)
        self.assertFalse(result)

    def test_is_tested_repository_empty_dependencies(self):
        # Configura l'istanza di JavaDependencyAnalyzer senza dipendenze di testing
        analyzer = JavaDependencyAnalyzer(folder=self.temp_folder, max_threads=5, testing_tools=['junit', 'mockito'])

        # Dipendenze vuote
        dependencies = []

        # Verifica che il metodo restituisca False quando la lista delle dipendenze è vuota
        result = analyzer.is_tested_repository(dependencies)
        self.assertFalse(result)

'''


class TestRepositoryAnalyzer(unittest.TestCase):

    def setUp(self):
        # Creare una directory temporanea per i test
        self.test_dir = "temp_test_dir"
        os.makedirs(self.test_dir, exist_ok=True)

        # Creare alcuni file Gradle e pom.xml di esempio per i test
        # self.create_gradle_files()
        # self.create_pom_files()

        # Inizializzare l'istanza del JavaDependencyAnalyzer per i test
        self.analyzer = JavaDependencyAnalyzer(folder=self.test_dir)

    def tearDown(self):
        # Rimuovere la directory temporanea e i file creati durante i test
        for root, dirs, files in os.walk(self.test_dir, topdown=False):
            for name in files:
                os.remove(os.path.join(root, name))
            for name in dirs:
                os.rmdir(os.path.join(root, name))
        os.rmdir(self.test_dir)

    def create_gradle_files(self):
        # Crea un file build.gradle di esempio
        with open(os.path.join(self.test_dir, "build.gradle"), 'w') as file:
            file.write("""
            dependencies {
                implementation 'org.springframework.boot:spring-boot-starter-web:2.5.0'
                testImplementation 'org.junit.jupiter:junit-jupiter:5.7.2'
            }
            """)

    def create_pom_files(self):
        # Crea un file pom.xml di esempio
        with open(os.path.join(self.test_dir, "pom.xml"), 'w') as file:
            file.write("""<project xmlns="http://maven.apache.org/POM/4.0.0"
         xmlns:xsi="http://www.w3.org/2001/XMLSchema-instance"
         xsi:schemaLocation="http://maven.apache.org/POM/4.0.0 http://maven.apache.org/xsd/maven-4.0.0.xsd">
    <dependencies>
        <dependency>
            <groupId>org.junit.jupiter</groupId>
            <artifactId>junit-jupiter</artifactId>
            <version>5.7.2</version>
        </dependency>
        <dependency>
            <groupId>org.springframework.boot</groupId>
            <artifactId>spring-boot-starter-web</artifactId>
            <version>2.5.0</version>
        </dependency>
    </dependencies>

</project>""")

    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_gradle_file(self, mock_print):
        self.create_gradle_files()
        dependencies = []
        dependencies = self.analyzer.analyze_gradle_file(self.test_dir, os.path.join(self.test_dir, "build.gradle"),
                                                         dependencies)
        expected_dependencies_gradle = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0'),
                                        ('org.junit.jupiter', 'junit-jupiter', '5.7.2')]
        self.assertEqual(dependencies, expected_dependencies_gradle)

    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_pom_file(self, mock_print):
        self.create_pom_files()
        dependencies = []
        dependencies = self.analyzer.analyze_pom_file(self.test_dir, os.path.join(self.test_dir, "pom.xml"),
                                                      dependencies)
        expected_dependencies_pom = [('org.junit.jupiter', 'junit-jupiter', '5.7.2'),
                                     ('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        self.assertEqual(dependencies, expected_dependencies_pom)

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.analyze_gradle_file")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_find_gradle_or_pom_with_gradle(self, mock_print, mock_analyze_gradle_file):
        # Creare alcuni file Gradle e pom.xml di esempio per i test
        self.create_gradle_files()

        # Eseguire il metodo find_gradle_or_pom
        self.analyzer.find_dependencies(self.test_dir)

        # Verificare che le funzioni analyze_gradle_file e analyze_pom_file siano state chiamate con i parametri corretti
        mock_analyze_gradle_file.assert_called_once_with(self.test_dir, os.path.join(self.test_dir, 'build.gradle'), [])

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.analyze_pom_file")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_find_gradle_or_pom_with_pom(self, mock_print, mock_analyze_pom_file):
        # Creare alcuni file Gradle e pom.xml di esempio per i test
        self.create_pom_files()

        # Eseguire il metodo find_gradle_or_pom
        self.analyzer.find_dependencies(self.test_dir)

        # Verificare che le funzioni analyze_gradle_file e analyze_pom_file siano state chiamate con i parametri corretti
        mock_analyze_pom_file.assert_called_once_with(self.test_dir, os.path.join(self.test_dir, 'pom.xml'), [])

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.analyze_gradle_file")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.analyze_pom_file")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_find_gradle_or_pom(self, mock_print, mock_analyze_pom_file, mock_analyze_gradle_file):
        # Creare alcuni file Gradle e pom.xml di esempio per i test
        self.create_gradle_files()
        self.create_pom_files()

        # Configurare i mock per ritornare dei valori specifici
        mock_analyze_gradle_file.return_value = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        mock_analyze_pom_file.return_value = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]

        # Eseguire il metodo find_gradle_or_pom
        dependencies = self.analyzer.find_dependencies(self.test_dir)

        # Verificare che l'output del metodo sia corretto
        expected_dependencies = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        self.assertEqual(dependencies, expected_dependencies)

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.analyze_repository")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_all(self, mock_print, mock_analyze_repository):
        # Configura il mock per il metodo analyze_repository
        mock_analyze_repository.side_effect = self.mock_analyze_repository

        # Crea un'istanza di JavaDependencyAnalyzer per i test
        max_threads = 3
        analyzer = JavaDependencyAnalyzer(self.test_dir, max_threads)

        # Esegui il metodo analyze_all
        analyzer.analyze_all()

        # Verifica che il numero corretto di thread sia stato creato
        self.assertEqual(mock_analyze_repository.call_count, max_threads)

        # Verifica che "Analysis completed." sia stato stampato alla fine
        mock_print.assert_called_with("Analysis completed.")

    def mock_analyze_repository(self):
        # Funzione mock per simulare il comportamento di analyze_repository
        time.sleep(1)  # Simula l'analisi
        print("Mock analyze_repository executed.")

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.find_dependencies")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_web_repository")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_tested_repository")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_repository_dipendenze(self, mock_print, mock_is_tested_repository, mock_is_web_repository,
                                           mock_find_dependencies):
        # Configura i mock per i metodi chiamati internamente da analyze_repository
        mock_find_dependencies.return_value = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        mock_is_web_repository.return_value = True
        mock_is_tested_repository.return_value = True

        # Crea un'istanza di JavaDependencyAnalyzer per i test
        analyzer = JavaDependencyAnalyzer(self.test_dir)

        # Crea una coda di repository fittizia con un elemento
        repository_queue = Queue()
        repository_queue.put("test_repository")

        # Assegna la coda di repository fittizia all'istanza di JavaDependencyAnalyzer
        analyzer.repositories = repository_queue

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository()

        # Verifica che i metodi interni siano stati chiamati correttamente
        mock_find_dependencies.assert_called_once_with("test_repository")

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.find_dependencies")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_web_repository")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_tested_repository")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_repository_web(self, mock_print, mock_is_tested_repository, mock_is_web_repository,
                                    mock_find_dependencies):
        # Configura i mock per i metodi chiamati internamente da analyze_repository
        mock_find_dependencies.return_value = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        mock_is_web_repository.return_value = True
        mock_is_tested_repository.return_value = True

        # Crea un'istanza di JavaDependencyAnalyzer per i test
        analyzer = JavaDependencyAnalyzer(self.test_dir)

        # Crea una coda di repository fittizia con un elemento
        repository_queue = Queue()
        repository_queue.put("test_repository")

        # Assegna la coda di repository fittizia all'istanza di JavaDependencyAnalyzer
        analyzer.repositories = repository_queue

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository()

        # Verifica che i metodi interni siano stati chiamati correttamente

        mock_is_web_repository.assert_called_once_with(
            [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')])

        # Verifica che i messaggi di analisi siano stati stampati correttamente
        mock_print.assert_any_call(
            "dipendenze per test_repository: [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]")
        mock_print.assert_any_call("test_repository è web")

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.find_dependencies")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_web_repository")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_tested_repository")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_repository_dipendenze_web_tested(self, mock_print, mock_is_tested_repository,
                                                      mock_is_web_repository,
                                                      mock_find_dependencies):
        # Configura i mock per i metodi chiamati internamente da analyze_repository
        mock_find_dependencies.return_value = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        mock_is_web_repository.return_value = True
        mock_is_tested_repository.return_value = True

        # Crea un'istanza di JavaDependencyAnalyzer per i test
        analyzer = JavaDependencyAnalyzer(self.test_dir)

        # Crea una coda di repository fittizia con un elemento
        repository_queue = Queue()
        repository_queue.put("test_repository")

        # Assegna la coda di repository fittizia all'istanza di JavaDependencyAnalyzer
        analyzer.repositories = repository_queue

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository()

        # Verifica che i metodi interni siano stati chiamati correttamente

        mock_is_tested_repository.assert_called_once_with(
            [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')])

        # Verifica che i messaggi di analisi siano stati stampati correttamente
        mock_print.assert_any_call(
            "dipendenze per test_repository: [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]")
        mock_print.assert_any_call("test_repository è web")
        mock_print.assert_any_call("test_repository è web tested")

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.find_dependencies")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_web_repository")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_tested_repository")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_repository_dipendenze_check(self, mock_print, mock_is_tested_repository,
                                                 mock_is_web_repository,
                                                 mock_find_dependencies):
        # Configura i mock per i metodi chiamati internamente da analyze_repository
        mock_find_dependencies.return_value = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        mock_is_web_repository.return_value = True
        mock_is_tested_repository.return_value = True

        # Crea un'istanza di JavaDependencyAnalyzer per i test
        analyzer = JavaDependencyAnalyzer(self.test_dir)

        # Crea una coda di repository fittizia con un elemento
        repository_queue = Queue()
        repository_queue.put("test_repository")

        # Assegna la coda di repository fittizia all'istanza di JavaDependencyAnalyzer
        analyzer.repositories = repository_queue

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository()

        # Verifica che i messaggi di analisi siano stati stampati correttamente
        mock_print.assert_any_call(
            "dipendenze per test_repository: [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]")

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.find_dependencies")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_web_repository")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_tested_repository")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_repository_dipendenze_check_web(self, mock_print, mock_is_tested_repository,
                                                     mock_is_web_repository,
                                                     mock_find_dependencies):
        # Configura i mock per i metodi chiamati internamente da analyze_repository
        mock_find_dependencies.return_value = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        mock_is_web_repository.return_value = True
        mock_is_tested_repository.return_value = True

        # Crea un'istanza di JavaDependencyAnalyzer per i test
        analyzer = JavaDependencyAnalyzer(self.test_dir)

        # Crea una coda di repository fittizia con un elemento
        repository_queue = Queue()
        repository_queue.put("test_repository")

        # Assegna la coda di repository fittizia all'istanza di JavaDependencyAnalyzer
        analyzer.repositories = repository_queue

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository()

        # Verifica che i messaggi di analisi siano stati stampati correttamente
        mock_print.assert_any_call("test_repository è web")

    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.find_dependencies")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_web_repository")
    @patch("RepositoryAnalyzer.Analyzer.JavaDependencyAnalyzer.is_tested_repository")
    @patch("builtins.print")  # Per ignorare le stampe durante i test
    def test_analyze_repository_dipendenze_check_web_tested(self, mock_print, mock_is_tested_repository,
                                                            mock_is_web_repository,
                                                            mock_find_dependencies):
        # Configura i mock per i metodi chiamati internamente da analyze_repository
        mock_find_dependencies.return_value = [('org.springframework.boot', 'spring-boot-starter-web', '2.5.0')]
        mock_is_web_repository.return_value = True
        mock_is_tested_repository.return_value = True

        # Crea un'istanza di JavaDependencyAnalyzer per i test
        analyzer = JavaDependencyAnalyzer(self.test_dir)

        # Crea una coda di repository fittizia con un elemento
        repository_queue = Queue()
        repository_queue.put("test_repository")

        # Assegna la coda di repository fittizia all'istanza di JavaDependencyAnalyzer
        analyzer.repositories = repository_queue

        # Esegui il metodo analyze_repository
        analyzer.analyze_repository()

        # Verifica che i metodi interni siano stati chiamati correttamente
        mock_print.assert_any_call("test_repository è web tested")

    def test_with_testing_tool_dependency(self):
        # Definisce una lista di dipendenze che include uno strumento di testing
        dependencies = [
            ("org.seleniumhq.selenium", "selenium-java", "3.141.59"),
            ("com.example", "example-artifact", "1.0.0")
        ]
        # Verifica che is_tested_repository ritorni True quando viene trovata una dipendenza di testing
        self.assertTrue(self.analyzer.is_tested_repository(dependencies))

    def test_without_testing_tool_dependency(self):
        # Definisce una lista di dipendenze senza strumenti di testing
        dependencies = [
            ("com.example", "example-artifact", "1.0.0"),
            ("org.example", "another-example-artifact", "2.0.0")
        ]
        # Verifica che is_tested_repository ritorni False quando non vengono trovate dipendenze di testing
        self.assertFalse(self.analyzer.is_tested_repository(dependencies))

    def test_with_web_tool_dependency(self):
        # Definisce una lista di dipendenze che include uno strumento web
        dependencies = [
            ("org.springframework.boot", "spring-boot-starter-web", "2.3.1.RELEASE"),
            ("com.example", "example-artifact", "1.0.0")
        ]
        # Verifica che is_web_repository ritorni True quando viene trovata una dipendenza web
        self.assertTrue(self.analyzer.is_web_repository(dependencies))

    def test_without_web_tool_dependency(self):
        # Definisce una lista di dipendenze senza strumenti web
        dependencies = [
            ("com.example", "example-artifact", "1.0.0"),
            ("org.example", "another-example-artifact", "2.0.0")
        ]
        # Verifica che is_web_repository ritorni False quando non vengono trovate dipendenze web
        self.assertFalse(self.analyzer.is_web_repository(dependencies))

    def test_add_new_dependency(self):
        # Inizializza una lista vuota di dipendenze
        dependencies = []
        # Definisce una dipendenza da aggiungere
        new_dependency = ("org.example", "example-artifact", "1.0.0")
        # Aggiunge la dipendenza alla lista
        self.analyzer.add_unique_element(dependencies, new_dependency)
        # Verifica che la lista di dipendenze ora contenga la nuova dipendenza
        self.assertIn(new_dependency, dependencies)

    def test_add_duplicate_dependency(self):
        # Inizializza una lista di dipendenze contenente già una dipendenza
        existing_dependency = ("org.example", "example-artifact", "1.0.0")
        dependencies = [existing_dependency]
        # Prova ad aggiungere la stessa dipendenza alla lista
        self.analyzer.add_unique_element(dependencies, existing_dependency)
        # Verifica che la dipendenza non sia stata aggiunta una seconda volta (ossia, non ci sono duplicati)
        self.assertEqual(len(dependencies), 1)

    def test_add_another_unique_dependency(self):
        # Inizializza una lista di dipendenze con una dipendenza esistente
        dependencies = [("org.example", "example-artifact", "1.0.0")]
        # Definisce una nuova dipendenza da aggiungere
        new_dependency = ("com.another", "another-artifact", "2.0.0")
        # Aggiunge la nuova dipendenza alla lista
        self.analyzer.add_unique_element(dependencies, new_dependency)
        # Verifica che entrambe le dipendenze siano presenti nella lista
        self.assertEqual(len(dependencies), 2)
        self.assertIn(new_dependency, dependencies)

    def test_get_subdirectories_1(self):
        os.mkdir(os.path.join(self.test_dir, "subdir1"))
        os.mkdir(os.path.join(self.test_dir, "subdir2"))
        # Crea un file di prova nella directory temporanea (che non dovrebbe essere incluso nel risultato)
        with open(os.path.join(self.test_dir, "file.txt"), "w") as f:
            f.write("Just a test file.")
        analyzer = JavaDependencyAnalyzer(
            folder=self.test_dir)  # Assicurati che JavaDependencyAnalyzer non necessiti di argomenti aggiuntivi
        subdirectories_queue = analyzer.get_subdirectories(self.test_dir)

        # Converti la coda in un elenco per facilitare l'assert
        subdirs = []
        while not subdirectories_queue.empty():
            subdirs.append(subdirectories_queue.get())

        # Verifica che la coda contenga le sottodirectory create e nulla più
        self.assertIn(os.path.join(self.test_dir, "subdir1"), subdirs)

    def test_get_subdirectories_2(self):
        os.mkdir(os.path.join(self.test_dir, "subdir1"))
        os.mkdir(os.path.join(self.test_dir, "subdir2"))
        # Crea un file di prova nella directory temporanea (che non dovrebbe essere incluso nel risultato)
        with open(os.path.join(self.test_dir, "file.txt"), "w") as f:
            f.write("Just a test file.")
        analyzer = JavaDependencyAnalyzer(
            folder=self.test_dir)  # Assicurati che JavaDependencyAnalyzer non necessiti di argomenti aggiuntivi
        subdirectories_queue = analyzer.get_subdirectories(self.test_dir)

        # Converti la coda in un elenco per facilitare l'assert
        subdirs = []
        while not subdirectories_queue.empty():
            subdirs.append(subdirectories_queue.get())

        # Verifica che la coda contenga le sottodirectory create e nulla più

        self.assertIn(os.path.join(self.test_dir, "subdir2"), subdirs)

    def test_get_two_subdirectories(self):
        os.mkdir(os.path.join(self.test_dir, "subdir1"))
        os.mkdir(os.path.join(self.test_dir, "subdir2"))
        # Crea un file di prova nella directory temporanea (che non dovrebbe essere incluso nel risultato)
        with open(os.path.join(self.test_dir, "file.txt"), "w") as f:
            f.write("Just a test file.")
        analyzer = JavaDependencyAnalyzer(
            folder=self.test_dir)  # Assicurati che JavaDependencyAnalyzer non necessiti di argomenti aggiuntivi
        subdirectories_queue = analyzer.get_subdirectories(self.test_dir)

        # Converti la coda in un elenco per facilitare l'assert
        subdirs = []
        while not subdirectories_queue.empty():
            subdirs.append(subdirectories_queue.get())

        # Verifica che la coda contenga le sottodirectory create e nulla più
        self.assertEqual(len(subdirs), 2)  # Assicurati che non ci siano altri elementi nella coda


if __name__ == '__main__':
    unittest.main()

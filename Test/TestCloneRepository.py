
import unittest
from unittest.mock import patch

from RepositoryAnalyzer.RepositoryCloner import RepositoryCloner

'''
class TestRepositoryCloner(unittest.TestCase):

    def test_clone_all(self):
        output_folder = "output_folder_test"
        os.makedirs(output_folder)
        # Creare un'istanza di TestClass con un numero massimo di thread impostato su 2 per scopi di testing
        test_instance = RepositoryCloner(output_folder, max_threads=2)

        # Creare una lista di repository fittizi
        repositories = ["AlessandroLori/LinkActivity",
                        "CarmineArena/DietiDeals24-frontend",
                        "SimDeveloper-cripto/DietiDeals24-backend",
                        "seart-group/ghs",
                        "gianlucalauro/Auto-SMS-Excel",
                        "gianlucalauro/agendaSpring",
                        "azure-samples/ms-identity-java-webapp", ]

        # Chiamare il metodo clone_all
        test_instance.clone_all(repositories)

        print(repositories)

        for repository in repositories:
            repository_name = repository.split("/")[-1]
            cloned_repository_path = os.path.join(output_folder, repository_name)
            self.assertTrue(os.path.exists(cloned_repository_path))

    def test_clone_repository_from_url(self):
        output_folder = "output_folder_test"
        test_instance = RepositoryCloner(output_folder)
        repo_url = "https://github.com/username/repository.git"

        # Mocking Repo.clone_from
        with patch.object(Repo, 'clone_from') as mock_clone_from:
            # Calling the method under test
            test_instance.clone_repository_from_url(repo_url)

            # Verifying that Repo.clone_from is called once
            mock_clone_from.assert_called_once()

    def test_clone_repository_from_url_failure(self):
        invalid_repo_url = "https://github.com/name/repository.git"

        # Verifying that an exception is raised when clone_repository_from_url is called with an invalid URL
        with self.assertRaises(Exception):
            RepositoryCloner().clone_repository_from_url(invalid_repo_url)

    def test_clone_repository(self):
        output_folder = "output_folder_test"
        test_instance = RepositoryCloner(output_folder)
        repository_name = "repository"
        repo_url = "https://github.com/" + repository_name + ".git"

        # Mocking clone_repository_from_url
        with patch.object(RepositoryCloner, 'clone_repository_from_url') as mock_clone_from_url:
            # Calling the method under test
            test_instance._clone_repository(repository_name)

            # Verifying that clone_repository_from_url is called once with the correct arguments
            mock_clone_from_url.assert_called_once_with(repo_url)
'''


class TestRepositoryCloner(unittest.TestCase):
    def setUp(self):
        self.output_folder = "test_output"
        self.max_threads = 2
        self.repositories = ["user/repo1", "user/repo2"]
        self.cloner = RepositoryCloner(self.output_folder, self.max_threads)

    @patch('os.path.exists')
    @patch('git.Repo.clone_from')
    def test_clone_repository_from_url_clone_function(self, mock_clone_from, mock_exists):
        mock_exists.return_value = False
        test_url = "https://github.com/user/repo1.git"
        self.cloner.clone_repository_from_url(test_url)

        # Verifica se la funzione Repo.clone_from è stata chiamata
        mock_clone_from.assert_called_once()

    @patch('os.path.exists')
    @patch('git.Repo.clone_from')
    def test_clone_repository_from_url_exist_function(self, mock_clone_from, mock_exists):
        mock_exists.return_value = False
        test_url = "https://github.com/user/repo1.git"
        self.cloner.clone_repository_from_url(test_url)

        # Verifica se la funzione Repo.clone_from è stata chiamata
        mock_exists.assert_called_once()

    def test_convert_list_to_queue(self):
        self.cloner.convert_list_to_queue(self.repositories)
        self.assertEqual(self.cloner.repositories.qsize(), len(self.repositories))

    @patch('RepositoryAnalyzer.RepositoryCloner.RepositoryCloner._clone_repository')
    def test_clone_all(self, mock_clone_repository):
        self.cloner.clone_all(self.repositories)

        # Verifica che i thread siano stati avviati correttamente
        # Si noti che questa è una semplificazione; nella realtà, il threading potrebbe
        # necessitare di approcci di test più complessi.
        self.assertEqual(mock_clone_repository.call_count, self.max_threads)

    @patch('os.path.exists')
    @patch('git.Repo.clone_from')
    @patch('builtins.print')
    def test_clone_repository_from_url_failure(self, mock_print, mock_clone_from, mock_exists):
        # Configura il mock per sollevare un'eccezione quando viene chiamato
        mock_clone_from.side_effect = Exception("Errore di clonazione")
        mock_exists.return_value = False  # Assicura che la logica proceda al tentativo di clonazione

        test_url = "not_valid_url"

        self.cloner = RepositoryCloner("output_folder")  # Assicurati di inizializzare correttamente la tua classe
        self.cloner.clone_repository_from_url(test_url)

        # Verifica che la funzione print sia stata chiamata con il messaggio di errore corretto
        mock_print.assert_called_once_with(f"Failed to clone repository '{test_url}': Errore di clonazione")


if __name__ == '__main__':
    unittest.main()

import unittest

from unittest.mock import MagicMock
from Dataset.DataSet import DataSet


class TestDataSet(unittest.TestCase):
    def setUp(self):
        # Creo un file JSON fittizio per il test
        self.file_path = 'test_data.json'
        with open(self.file_path, 'w', encoding='utf-8') as file:
            file.write('{"items": [{"name": "repo1"}, {"name": "repo2"}, {"name": "repo3"}]}')

    def tearDown(self):
        # Rimuovo il file JSON fittizio dopo il test
        import os
        os.remove(self.file_path)

    # Serie di test per il metodo read_all_repositories()
    def test_read_all_repositories_size(self):
        dataset = DataSet(self.file_path)
        repositories = dataset.read_all_repositories()
        self.assertEqual(len(repositories), 3)

    def test_first_repository_from_all_repository(self):
        dataset = DataSet(self.file_path)
        repositories = dataset.read_all_repositories()
        self.assertEqual(repositories[0]['name'], 'repo1')

    def test_second_repository_from_all_repository(self):
        dataset = DataSet(self.file_path)
        repositories = dataset.read_all_repositories()
        self.assertEqual(repositories[1]['name'], 'repo2')

    def test_third_repository_from_all_repository(self):
        dataset = DataSet(self.file_path)
        repositories = dataset.read_all_repositories()
        self.assertEqual(repositories[2]['name'], 'repo3')

    def test_error_all_repositories(self):
        dataset = DataSet('not_existent_file.json')
        # Sarebbe un assert per verificare se lancio l'eccezione corretta
        with self.assertRaises(FileNotFoundError):
            dataset.read_all_repositories()

    # Serie di test per filter_repositories()
    # NB: creare stub per la classe FilterStrategy con la classe MagicMock
    def test_filter_repositories_size(self):
        mock_filter_strategy = MagicMock()
        mock_filter_strategy.filtering.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]

        dataset = DataSet(self.file_path)
        filtered_repositories = dataset.filter_repositories(mock_filter_strategy)

        # Verifica se la strategia di filtro è stata chiamata correttamente con i repository
        mock_filter_strategy.filtering.assert_called_once()

        self.assertEqual(len(filtered_repositories), 2)

    def test_filter_repositories_first_item(self):
        mock_filter_strategy = MagicMock()
        mock_filter_strategy.filtering.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]

        dataset = DataSet(self.file_path)
        filtered_repositories = dataset.filter_repositories(mock_filter_strategy)

        mock_filter_strategy.filtering.assert_called_once()
        self.assertEqual(filtered_repositories[0]['name'], 'repo1')

    def test_filter_repositories_second_item(self):
        mock_filter_strategy = MagicMock()
        mock_filter_strategy.filtering.return_value = [{'name': 'repo1'}, {'name': 'repo2'}]

        dataset = DataSet(self.file_path)
        filtered_repositories = dataset.filter_repositories(mock_filter_strategy)

        mock_filter_strategy.filtering.assert_called_once()
        self.assertEqual(filtered_repositories[1]['name'], 'repo2')


if __name__ == '__main__':
    unittest.main()

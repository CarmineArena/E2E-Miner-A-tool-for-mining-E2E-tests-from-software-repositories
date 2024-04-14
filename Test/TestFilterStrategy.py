import unittest
from Dataset.FilterStrategy import Filter


class TestFilter(unittest.TestCase):
    def test_filtering_size(self):

        filter_instance = Filter(is_fork=True, commits=10, main_language=['Python'], stargazers=50, contributors=5)

        # Creo una lista di dizionari simulando dei repository da filtrare
        repositories = [
            {'isFork': True, 'commits': 12, 'mainLanguage': 'Python', 'stargazers': 120, 'contributors': 7},
            {'isFork': False, 'commits': 8, 'mainLanguage': 'Java', 'stargazers': 50, 'contributors': 3},
            {'isFork': True, 'commits': 15, 'mainLanguage': 'Python', 'stargazers': 80, 'contributors': 6}
        ]

        filtered_results = filter_instance.filtering(repositories)

        self.assertEqual(len(filtered_results), 2)  # Si aspetta che ci siano 2 risultati filtrati

    def test_filtering_first_element(self):
        filter_instance = Filter(is_fork=True, commits=10, main_language=['Python'], stargazers=50, contributors=5)

        repositories = [
            {'isFork': True, 'commits': 12, 'mainLanguage': 'Python', 'stargazers': 120, 'contributors': 7},
            {'isFork': False, 'commits': 8, 'mainLanguage': 'Java', 'stargazers': 50, 'contributors': 3},
            {'isFork': True, 'commits': 15, 'mainLanguage': 'Python', 'stargazers': 80, 'contributors': 6}
        ]

        filtered_results = filter_instance.filtering(repositories)

        # Assert per capire se un elemento si trova nella lista
        self.assertIn(repositories[0], filtered_results)

    def test_filtering_second_element(self):
        filter_instance = Filter(is_fork=True, commits=10, main_language=['Python'], stargazers=50, contributors=5)

        repositories = [
            {'isFork': True, 'commits': 12, 'mainLanguage': 'Python', 'stargazers': 120, 'contributors': 7},
            {'isFork': False, 'commits': 8, 'mainLanguage': 'Java', 'stargazers': 50, 'contributors': 3},
            {'isFork': True, 'commits': 15, 'mainLanguage': 'Python', 'stargazers': 80, 'contributors': 6}
        ]

        filtered_results = filter_instance.filtering(repositories)

        self.assertIn(repositories[2], filtered_results)  # Il terzo repository deve essere incluso nei risultati

    def test_filtering_empty_list(self):
        filter_instance = Filter(is_fork=True, commits=10, main_language=['Python'], stargazers=50, contributors=5)

        repositories = []
        filtered_results = filter_instance.filtering(repositories)
        self.assertEqual(len(filtered_results), 0)

    def test_with_no_element_to_filter(self):
        filter_instance = Filter(is_fork=True, commits=10, main_language=['C##'], stargazers=50, contributors=5)

        repositories = [
            {'isFork': True, 'commits': 12, 'mainLanguage': 'Python', 'stargazers': 120, 'contributors': 7},
            {'isFork': False, 'commits': 8, 'mainLanguage': 'Java', 'stargazers': 50, 'contributors': 3},
            {'isFork': True, 'commits': 15, 'mainLanguage': 'Python', 'stargazers': 80, 'contributors': 6}
        ]

        filtered_results = filter_instance.filtering(repositories)

        self.assertEqual(len(filtered_results), 0)


if __name__ == '__main__':
    unittest.main()

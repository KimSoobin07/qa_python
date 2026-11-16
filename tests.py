import pytest
from main import BooksCollector

class TestBooksCollector:

    # --- add_new_book ---
    def test_add_new_book_adds_book_with_empty_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        assert collector.books_genre == {'Гарри Поттер': ''}

    def test_add_new_book_does_not_add_duplicate(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.add_new_book('Гарри Поттер')
        assert len(collector.books_genre) == 1

    @pytest.mark.parametrize('name', ['', 'А' * 41])
    def test_add_new_book_rejects_invalid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name not in collector.books_genre

    @pytest.mark.parametrize('name', ['А', 'А' * 40])
    def test_add_new_book_accepts_valid_name(self, name):
        collector = BooksCollector()
        collector.add_new_book(name)
        assert name in collector.books_genre

    # --- set_book_genre ---
    def test_set_book_genre_sets_valid_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        assert collector.get_book_genre('Гарри Поттер') == 'Фантастика'

    def test_set_book_genre_does_not_set_invalid_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Неизвестный жанр')
        assert collector.get_book_genre('Гарри Поттер') == ''

    # --- get_book_genre ---
    def test_get_book_genre_returns_genre(self):
        collector = BooksCollector()
        collector.add_new_book('Гарри Поттер')
        collector.set_book_genre('Гарри Поттер', 'Фантастика')
        assert collector.get_book_genre('Гарри Поттер') == 'Фантастика'

    def test_get_book_genre_returns_none_for_missing_book(self):
        collector = BooksCollector()
        assert collector.get_book_genre('Несуществующая книга') is None

    # --- get_books_with_specific_genre ---
    @pytest.mark.parametrize('genre, expected', [
        ('Фантастика', ['Книга 1']),
        ('Ужасы', ['Книга 2']),
        ('Комедии', []),
    ])
    def test_get_books_with_specific_genre(self, genre, expected):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.set_book_genre('Книга 1', 'Фантастика')
        collector.add_new_book('Книга 2')
        collector.set_book_genre('Книга 2', 'Ужасы')
        assert collector.get_books_with_specific_genre(genre) == expected

    # --- get_books_genre ---
    def test_get_books_genre_returns_dict(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.set_book_genre('Книга 1', 'Фантастика')
        assert collector.get_books_genre() == {'Книга 1': 'Фантастика'}

    # --- get_books_for_children ---
    def test_get_books_for_children_excludes_age_rated_genres(self):
        collector = BooksCollector()
        collector.add_new_book('Детская')
        collector.set_book_genre('Детская', 'Мультфильмы')
        collector.add_new_book('Страшная')
        collector.set_book_genre('Страшная', 'Ужасы')
        collector.add_new_book('Без жанра')
        assert collector.get_books_for_children() == ['Детская']

    # --- add_book_in_favorites ---
    def test_add_book_in_favorites_adds_book(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_book_in_favorites('Книга 1')
        assert collector.get_list_of_favorites_books() == ['Книга 1']

    def test_add_book_in_favorites_ignores_duplicate_and_unknown(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_book_in_favorites('Книга 1')
        collector.add_book_in_favorites('Книга 1')
        collector.add_book_in_favorites('Нет книги')
        assert collector.get_list_of_favorites_books() == ['Книга 1']

    # --- delete_book_from_favorites ---
    def test_delete_book_from_favorites_removes_book(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_book_in_favorites('Книга 1')
        collector.delete_book_from_favorites('Книга 1')
        assert collector.get_list_of_favorites_books() == []

    def test_delete_book_from_favorites_ignores_missing(self):
        collector = BooksCollector()
        collector.delete_book_from_favorites('Нет книги')
        assert collector.get_list_of_favorites_books() == []

    # --- get_list_of_favorites_books ---
    def test_get_list_of_favorites_books_returns_list(self):
        collector = BooksCollector()
        collector.add_new_book('Книга 1')
        collector.add_new_book('Книга 2')
        collector.add_book_in_favorites('Книга 1')
        collector.add_book_in_favorites('Книга 2')
        assert collector.get_list_of_favorites_books() == ['Книга 1', 'Книга 2']
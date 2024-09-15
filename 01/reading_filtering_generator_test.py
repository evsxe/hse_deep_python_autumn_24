import io
import unittest

from reading_filtering_generator import reading_filtering_generator


class ReadingFilteringGeneratorTest(unittest.TestCase):
    def test_empty_file(self):
        """Checks that the generator returns nothing for an empty file."""
        file_obj = io.StringIO()

        generator = reading_filtering_generator(
            file_obj,
            ['word'],
            []
        )

        self.assertEqual(list(generator), [])

    def test_no_matching_words(self):
        """Checks that the generator returns nothing if there are no matches."""

        file_obj = io.StringIO()
        test_data = [
            "This is a line with no matching words\n",
            "Another line, still no matches\n"
        ]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            ['apple', 'banana'],
            []
        )

        self.assertEqual(list(generator), [])

    def test_matching_words_found(self):
        """Checks that the generator returns strings with matches."""
        file_obj = io.StringIO()
        test_data = [
            "This line has the word apple\n",
            "And this one has banana\n",
            "This line has apple and banana\n"
        ]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            ['apple', 'banana'],
            []
        )

        self.assertEqual(list(generator), [
            "This line has the word apple\n",
            "And this one has banana\n",
            "This line has apple and banana\n"
        ])

    def test_stop_words_filtering(self):
        """Checks that the generator discards strings with stop words."""

        file_obj = io.StringIO()
        test_data = [
            "This line contains stop word\n",
            "This line has apple but also stop word\n"
        ]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            ['apple'],
            ['stop']
        )

        self.assertEqual(list(generator), [])

    def test_multiple_matches_in_one_line(self):
        """Checks that the generator returns the string only once,
         even if there are multiple matches."""

        file_obj = io.StringIO()
        test_data = ["This line has apple and banana and apple again"]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            ['apple', 'banana'],
            []
        )

        self.assertEqual(
            list(generator),
            ["This line has apple and banana and apple again"]
        )

    def test_file_object_input(self):
        """Checks work with a file object as input data."""
        file_obj = io.StringIO()
        test_data = ["This line has apple"]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            ['apple'],
            []
        )
        self.assertEqual(
            list(generator),
            ["This line has apple"]
        )

    def test_filename_input(self):
        generator = reading_filtering_generator(
            'test.txt',
            ['apple'],
            ['']
        )
        self.assertEqual(
            list(generator),
            ["This line has apple"]
        )

    def test_empty_search_words(self):
        """Checks that the generator returns nothing
            if the search word list is empty."""

        file_obj = io.StringIO()
        test_data = ["This line has some words"]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            [],
            []
        )

        self.assertEqual(list(generator), [])

    def test_empty_stop_words(self):
        """Checks that the generator is running
            if the stop word list is empty."""

        file_obj = io.StringIO()
        test_data = ["This line has apple"]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            ['apple'],
            []
        )

        self.assertEqual(list(generator), ["This line has apple"])

    def test_duplicate_words_in_search_list(self):
        """Checks that the generator is running
            if there are duplicates in the search word list."""

        file_obj = io.StringIO()
        test_data = ["This line has apple and apple again"]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            ['apple', 'apple'],
            []
        )

        self.assertEqual(
            list(generator),
            ["This line has apple and apple again"]
        )

    def test_duplicate_words_in_stop_list(self):
        """Checks that the generator is running
            if there are duplicates in the stop word list."""

        file_obj = io.StringIO()
        test_data = ["This line has apple and stop"]
        file_obj.writelines(test_data)
        file_obj.seek(0)

        generator = reading_filtering_generator(
            file_obj,
            ['apple'],
            ['stop', 'stop']
        )

        self.assertEqual(list(generator), [])


if __name__ == '__main__':
    unittest.main()

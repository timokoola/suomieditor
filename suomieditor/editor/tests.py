from django.test import TestCase
from django.urls import reverse
from .models import BaseForm, WordForm
from .views import form_mapper, index, detail, analyze, add_cases, search


class EditorTestCase(TestCase):
    def setUp(self):
        # Create test data for BaseForm and WordForm
        self.base_form = BaseForm.objects.create(
            word="kääre", declension="1", gradation="1"
        )
        self.word_form = WordForm.objects.create(
            baseform=self.base_form,
            wordform="kääre",
            number=WordForm.Number.SINGULAR,
            case=WordForm.Case.NOMINATIVE,
            source="editor",
        )

    def test_form_mapper_with_valid_data(self):
        # Test form_mapper with valid data
        kotus_result = {
            "BASEFORM": "kääre",
            "NUMBER": "singular",
            "SIJAMUOTO": "nimento",
        }
        word_form = "kääre"
        result = form_mapper(kotus_result, word_form)
        self.assertTrue(result)

    def test_form_mapper_with_missing_fields(self):
        # Test form_mapper with missing fields in kotus_result
        kotus_result = {"BASEFORM": "kääre", "NUMBER": "singular"}
        word_form = "kääre"
        result = form_mapper(kotus_result, word_form)
        self.assertFalse(result)

    def test_index_view(self):
        # Test index view
        response = self.client.get(reverse("editor:index"))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editor/index.html")

    def test_detail_view(self):
        # Test detail view
        response = self.client.get(reverse("editor:detail", args=[self.base_form.id]))
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editor/detail.html")

    def test_analyze_view(self):
        # Test analyze view with POST request
        data = {"word": "kääre"}
        response = self.client.post(reverse("editor:analyze"), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_analyze_view_with_get_request(self):
        # Test analyze view with GET request (should return 405 Method Not Allowed)
        response = self.client.get(reverse("editor:analyze"))
        self.assertEqual(response.status_code, 405)

    def test_add_cases_view(self):
        # Test add_cases view with POST request
        data = {"base_form": self.base_form.id, "case_1": "kääre", "case_2": ""}
        response = self.client.post(reverse("editor:add_cases"), data)
        self.assertEqual(response.status_code, 302)  # Redirect status code

    def test_add_cases_view_with_get_request(self):
        # Test add_cases view with GET request (should return 405 Method Not Allowed)
        response = self.client.get(reverse("editor:add_cases"))
        self.assertEqual(response.status_code, 405)

    def test_search_view(self):
        # Test search view with GET request
        data = {"word": "kääre"}
        response = self.client.get(reverse("editor:search"), data)
        self.assertEqual(response.status_code, 200)
        self.assertTemplateUsed(response, "editor/search_results.html")

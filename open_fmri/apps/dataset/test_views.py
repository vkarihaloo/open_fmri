import logging

from django.contrib.auth.models import User
from django.core.urlresolvers import reverse, reverse_lazy
from django.test import TestCase, RequestFactory

from model_mommy import mommy as ModelFactory

from dataset.models import Dataset
from dataset.views import DatasetCreate

class DatasetViewTestCase(TestCase):
    def setUp(self):
        self.dataset = ModelFactory.make('Dataset')
        self.request_factory = RequestFactory()
        self.password = 'pass'
        self.user = User.objects.create_user(
            username='user', email='email@example.com', password=self.password)
        

    def test_list_view(self):
        response = self.client.get(reverse('dataset_list'))
        self.assertEqual(response.status_code, 200)
    
    def test_create_view_nologin(self):
        response = self.client.get(reverse('dataset_create'))
        self.assertEqual(response.status_code, 302)

    def test_create_view_login(self):
        self.assertTrue(self.client.login(
            username=self.user.username, password=self.password))
        response = self.client.get(reverse('dataset_create'))
        self.assertEqual(response.status_code, 200)

    '''
    Currently there are only 3 required fields. we will check that these
    generate errors. Untouched formsets can be left blank and not run unto
    validation errors
    '''
    def test_create_view_login_blank_data(self):
        self.assertTrue(self.client.login(
            username=self.user.username, password=self.password))
        response = self.client.post(reverse('dataset_create'))
        self.assertFormError(response, 'form', 'project_name', 
                             'This field is required.')
        self.assertFormError(response, 'form', 'summary', 
                             'This field is required.')
        self.assertFormError(response, 'form', 'sample_size', 
                             'This field is required.')

    '''
    Create view redirects to the list view. lets check the response to see if
    we are redirected. (should also check the template hit...)
    '''
    def test_create_view_login_valid_data(self):
        data = {
            'project_name': 'unique', 
            'summary': self.dataset.summary,
            'sample_size': self.dataset.sample_size,
            'workflow_stage': 'SUBMITTED',
            'license_title': 'PPDL',
            'investigator_set-TOTAL_FORMS': 0,
            'investigator_set-INITIAL_FORMS': 0,
            'investigator_set-MIN_NUM_FORMS': 0,
            'investigator_set-MAX_NUM_FORMS': 0,
            'publicationdocument_set-TOTAL_FORMS': 0,
            'publicationdocument_set-INITIAL_FORMS': 0,
            'publicationdocument_set-MIN_NUM_FORMS': 0,
            'publicationdocument_set-MAX_NUM_FORMS': 0,
            'publicationpubmedlink_set-TOTAL_FORMS': 0,
            'publicationpubmedlink_set-INITIAL_FORMS': 0,
            'publicationpubmedlink_set-MIN_NUM_FORMS': 0,
            'publicationpubmedlink_set-MAX_NUM_FORMS': 0,
            'task_set-TOTAL_FORMS': 0,
            'task_set-INITIAL_FORMS': 0,
            'task_set-MIN_NUM_FORMS': 0,
            'task_set-MAX_NUM_FORMS': 0,

        }
        self.assertTrue(self.client.login(
            username=self.user.username, password=self.password))
        response = self.client.post(reverse('dataset_create'), data)
        self.assertEqual(response.status_code, 302)

    def test_update_view_nologin(self):
        response = self.client.get(reverse('dataset_update', 
                                           args=[self.dataset.id]))
        self.assertEqual(response.status_code, 302)

    def test_update_view_login(self):
        self.assertTrue(self.client.login(
            username=self.user.username, password=self.password))
        response = self.client.get(reverse('dataset_update', 
                                           args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)

    def test_update_view_login_valid_data(self):
        dataset = ModelFactory.make('Dataset')
        data = {
            'project_name': 'unique', 
            'summary': self.dataset.summary,
            'sample_size': self.dataset.sample_size,
            'workflow_stage': 'SUBMITTED',
            'license_title': 'PPDL',
            'investigator_set-TOTAL_FORMS': 0,
            'investigator_set-INITIAL_FORMS': 0,
            'investigator_set-MIN_NUM_FORMS': 0,
            'investigator_set-MAX_NUM_FORMS': 0,
            'publicationdocument_set-TOTAL_FORMS': 0,
            'publicationdocument_set-INITIAL_FORMS': 0,
            'publicationdocument_set-MIN_NUM_FORMS': 0,
            'publicationdocument_set-MAX_NUM_FORMS': 0,
            'publicationpubmedlink_set-TOTAL_FORMS': 0,
            'publicationpubmedlink_set-INITIAL_FORMS': 0,
            'publicationpubmedlink_set-MIN_NUM_FORMS': 0,
            'publicationpubmedlink_set-MAX_NUM_FORMS': 0,
            'task_set-TOTAL_FORMS': 0,
            'task_set-INITIAL_FORMS': 0,
            'task_set-MIN_NUM_FORMS': 0,
            'task_set-MAX_NUM_FORMS': 0,

        }
        self.assertTrue(self.client.login(
            username=self.user.username, password=self.password))
        response = self.client.post(
            reverse('dataset_update', args=[dataset.id]), data)
        self.assertEqual(response.status_code, 302)


    '''
    Test to see if the detail view is displaying the three values that the 
    model factory is generating appear in the response
    '''
    def test_detail_view(self):
        response = self.client.get(reverse('dataset_detail', 
                                           args=[self.dataset.id]))
        self.assertEqual(response.status_code, 200)
        self.assertContains(response, self.dataset.project_name)
        self.assertContains(response, self.dataset.summary)
        self.assertContains(response, self.dataset.sample_size)



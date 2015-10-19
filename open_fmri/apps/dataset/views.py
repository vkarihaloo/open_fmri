import requests
import requests_cache

from django import forms
from django.core.urlresolvers import reverse, reverse_lazy
from django.shortcuts import render
from django.views.generic import CreateView, DeleteView, DetailView, \
    ListView, UpdateView

from braces.views import LoginRequiredMixin

from dataset.forms import DatasetForm, FeaturedDatasetForm, InvestigatorFormSet, \
    PublicationDocumentFormSet, PublicationPubMedLinkFormSet, TaskFormSet
from dataset.models import Dataset, Investigator, PublicationDocument, \
    PublicationPubMedLink, FeaturedDataset

requests_cache.install_cache('test_cache')

class DatasetList(ListView):
    model = Dataset

class DatasetDelete(LoginRequiredMixin, DeleteView):
    model = Dataset
    success_url = reverse_lazy('dataset_list')

class DatasetDetail(DetailView):
    model = Dataset

class DatasetCreate(LoginRequiredMixin, CreateView):
    model = Dataset
    form_class = DatasetForm
    success_url = reverse_lazy('dataset_list')

    def get_context_data(self, **kwargs):
        context = super(DatasetCreate, self).get_context_data(**kwargs)
        context['investigator_formset'] = InvestigatorFormSet()
        context['publication_document_formset'] = PublicationDocumentFormSet()
        context['publication_pubmed_link_formset'] = \
            PublicationPubMedLinkFormSet()
        context['task_formset'] = TaskFormSet()
        return context

    def form_valid(self, form):
        dataset = form.save()
        
        investigator_formset = InvestigatorFormSet(self.request.POST,
            self.request.FILES, instance=dataset)
        if investigator_formset.is_valid():
            investigator_formset.save()

        publication_document_formset = PublicationDocumentFormSet(
            self.request.POST, self.request.FILES, instance=dataset)
        if publication_document_formset.is_valid():
            investigator_formset.save()

        publication_pubmed_link_formset = PublicationPubMedLinkFormSet(
            self.request.POST, instance=dataset)
        if publication_pubmed_link_formset.is_valid():
            publication_pubmed_link_formset.save()

        task_formset = TaskFormSet(self.request.POST, self.request.FILES,
            instance=dataset)
        if task_formset.is_valid():
            task_formset.save()

        return super(DatasetCreate, self).form_valid(form)

class DatasetUpdate(LoginRequiredMixin, UpdateView):
    model = Dataset
    form_class = DatasetForm

    def get_success_url(self):
        return reverse('dataset_update', kwargs={'pk': self.object.id})

    def get_context_data(self, **kwargs):
        context = super(DatasetUpdate, self).get_context_data(**kwargs)
        context['investigator_formset'] = InvestigatorFormSet(
            instance=self.object)
        context['publication_document_formset'] = PublicationDocumentFormSet(
            instance=self.object)
        context['publication_pubmed_link_formset'] = \
            PublicationPubMedLinkFormSet(instance=self.object)
        context['task_formset'] = TaskFormSet(instance=self.object)
        return context

    def form_valid(self, form):
        dataset = form.save()
        
        investigator_formset = InvestigatorFormSet(self.request.POST,
            self.request.FILES, instance=self.object)
        if investigator_formset.is_valid():
            investigator_formset.save()

        publication_document_formset = PublicationDocumentFormSet(
            self.request.POST, self.request.FILES, instance=self.object)
        if publication_document_formset.is_valid():
            investigator_formset.save()
        
        publication_pubmed_link_formset = PublicationPubMedLinkFormSet(
            self.request.POST, instance=self.object)
        if publication_pubmed_link_formset.is_valid():
            publication_pubmed_link_formset.save()
        
        task_formset = TaskFormSet(self.request.POST, self.request.FILES,
            instance=self.object)
        if task_formset.is_valid():
            task_formset.save()
        else:
            raise forms.ValidationError(task_formset.errors)
            
        return super(DatasetUpdate, self).form_valid(form)

class FeaturedDatasetEdit(LoginRequiredMixin, CreateView):
    model = FeaturedDataset
    form_class = FeaturedDatasetForm
    success_url = reverse_lazy('dataset_list')

    def get_context_data(self, **kwargs):
        context = super(FeaturedDatasetEdit, self).get_context_data(**kwargs)
        context['featured_datasets'] = FeaturedDataset.objects.order_by(
            '-date_featured')
        return context

class FeaturedDatasetDelete(LoginRequiredMixin, DeleteView):
    model = FeaturedDataset
    success_url = reverse_lazy('dataset_list')


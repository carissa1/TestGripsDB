from django.shortcuts import render

# Create your views here.
import os
import io
from pyexpat.errors import messages
from django.http import HttpResponse, Http404, HttpResponseRedirect
from django.shortcuts import get_object_or_404, render
from django.utils.decorators import method_decorator
from django.views.generic import DetailView
from django.utils.text import slugify
from django.views.decorators.cache import cache_page
from django.views.decorators.vary import vary_on_cookie
from django.db import transaction
from django.db import models
from django.db.models import Count, F, Func, Value
# from reversion.models import Version

from .models import ProteinTF

from django.conf import settings
from django.http import FileResponse, HttpRequest, HttpResponse
from django.views.decorators.cache import cache_control
from django.views.decorators.http import require_GET

@require_GET
@cache_control(max_age=60 * 60 * 24, immutable=True, public=True)  # one day
def favicon(request: HttpRequest) -> HttpResponse:
    file = (settings.BASE_DIR / "static" / "icon_img.png").open("rb")
    return FileResponse(file)

def home_page(request):
   return render(request, "home.html")

def get_database(request):
   proteins = ProteinTF.objects.order_by("gene")
   # print(proteins)
   return render(request, "proteins.html", {"proteins": proteins})

class ProteinDetailView(DetailView):
   """renders html for single protein page"""

   # slug_field = 'gene'
   model = ProteinTF
   context_object_name = 'protein'   # name for the data that will be used by template
   queryset = ProteinTF.objects
   template_name = 'proteins/proteinPage.html'
   
   def get_object(self, query_set=None):
      # print(self.kwargs['slug'])
      if query_set is None:
            query_set = self.get_queryset()
      # print(self.kwargs['slug'])
      # print(ProteinTF.objects.get(gene=self.kwargs['slug']))
      obj = ProteinTF.objects.get(gene=self.kwargs['gene'])
      # print(query_set.get(gene=self.kwargs['slug']))
      # obj = query_set.get(gene=self.kwargs['slug'])
      # obj = queryset.get(uuid=self.kwargs.get("slug", "").upper())
      return obj

   def get(self, request, *args, **kwargs):
      self.object = self.get_object()
      # print(self.object)
      context = self.get_context_data(object=self.object)
      # print(context['protein'].satellite)
      return render(request, 'proteins/proteinPage.html', context)
     
      # context = {'protein': obj}
      # return render(request, 'proteins/proteinPage.html', context)
   
   def get_context_data(self, **kwargs):
      data = super().get_context_data(**kwargs)

      return data
   
   #  queryset = (
   #      ProteinTF.objects.annotate()
   #      .prefetch_related("validations", "predictions")
   #      .select_related("microscopy_summary", "motif_enrichment", "motif_Q_score")
   #  )

   #  @method_decorator(cache_page(60 * 30))
   #  @method_decorator(vary_on_cookie)
   #  def dispatch(self, *args, **kwargs):
   #      return super().dispatch(*args, **kwargs)

   #  def version_view(self, request, version, *args, **kwargs):
   #      try:
   #          with transaction.atomic(using=version.db):
   #              # Revert the revision.
   #              version.revision.revert(delete=True)
   #              # Run the normal changeform view.
   #              self.object = self.get_object()
   #              context = self.get_context_data(object=self.object)
   #              context["version"] = version
   #              response = self.render_to_response(context)
   #              response.render()  # eager rendering of response is necessary before db rollback
   #              raise _RollBackRevisionView(response)
   #      except _RollBackRevisionView as ex:
   #          return ex.response

   #  def get_object(self, queryset=None):
   #      if queryset is None:
   #          queryset = self.get_queryset()
   #      try:
   #          obj = queryset.get(slug=self.kwargs.get("slug"))
   #      except ProteinTF.DoesNotExist:
   #          try:
   #              obj = queryset.get(uuid=self.kwargs.get("slug", "").upper())
   #          except ProteinTF.DoesNotExist as e:
   #              raise Http404("No protein found matching this query") from e
   #      if obj.status == "hidden" and obj.created_by != self.request.user and not self.request.user.is_staff:
   #          raise Http404("No protein found matching this query")
   #      return obj

   #  def get(self, request, *args, **kwargs):
   #      if "rev" in kwargs:
   #          try:
   #              rev = int(kwargs["rev"])  # has to be int or indexing will fail
   #          except Exception:
   #              rev = 0
   #          # if rev > 0:
   #             #  versions = Version.objects.get_for_object(self.get_object())
   #             #  version = versions[min(versions.count() - 1, rev)]
   #             #  return self.version_view(request, version, *args, **kwargs)
   #    #   elif "ver" in kwargs:
   #          # version = get_object_or_404(Version, id=kwargs["ver"])
   #          # if int(version.object_id) == self.get_object().id:
   #             #  return self.version_view(request, version, *args, **kwargs)
   #          # TODO:  ELSE WHAT??
   #      try:
   #          return super().get(request, *args, **kwargs)
   #      except Http404:
   #          from django.contrib.postgres.fields import ArrayField
   #          from django.db import models

   #          name = slugify(self.kwargs.get(self.slug_url_kwarg))
   #          aliases_lower = Func(Func(F("aliases"), function="unnest"), function="LOWER")
   #          remove_space = Func(aliases_lower, Value(" "), Value("-"), function="replace")
   #          final = Func(
   #              remove_space,
   #              Value("."),
   #              Value(""),
   #              function="replace",
   #              output_field=ArrayField(models.CharField(max_length=200)),
   #          )
   #          d = dict(ProteinTF.objects.annotate(aka=final).values_list("aka", "id"))
   #          if name in d:
   #              obj = ProteinTF.objects.get(id=d[name])
   #              messages.add_message(
   #                  self.request,
   #                  messages.INFO,
   #                  f"The URL {self.request.get_full_path()} was not found.  You have been forwarded here",
   #              )
   #              return HttpResponseRedirect(obj.get_absolute_url())
   #          raise

   #  def get_context_data(self, **kwargs):
   #      data = super().get_context_data(**kwargs)
   #    #   if self.object.status != "approved":
   #    #       data["last_approved"] = self.object.last_approved_version()

   #      similar = ProteinTF.visible.filter(name__iexact=f"m{self.object.gene}")
   #      similar = similar | ProteinTF.visible.filter(name__iexact=f"monomeric{self.object.satellite}")
   #    #   similar = similar | ProteinTF.visible.filter(name__iexact=self.object.name.lstrip("m"))
   #    #   similar = similar | ProteinTF.visible.filter(name__iexact=self.object.name.lower().lstrip("td"))
   #    #   similar = similar | ProteinTF.visible.filter(name__iexact=f"td{self.object.name}")
   #      data["similar"] = similar.exclude(id=self.object.my_id)
   #    #   spectra = [sp for state in self.object.states.all() for sp in state.spectra.all()]

   #    #   data["spectra_ids"] = ",".join([str(sp.id) for sp in spectra])
   #    #   data["hidden_spectra"] = ",".join([str(sp.id) for sp in spectra if sp.subtype in ("2p")])

   #      # put links in excerpts
   #    #   data["excerpts"] = link_excerpts(self.object.excerpts.all(), self.object.name, self.object.aliases)

   #      # Add country code to context
   #    #   try:
   #    #       data["country_code"] = get_country_code(self.request)
   #    #   except Exception:
   #    #       data["country_code"] = ""

   #      return data
   
import contextlib
from django.db import models
from django.utils.text import slugify
from django.db.models import Count, F, Func, Q, Value
from django_mongodb_backend.fields import ObjectIdAutoField

# class ProteinManager(models.Manager):
#     def deep_get(self, name):
#         slug = slugify(name)
#         with contextlib.suppress(ProteinTF.DoesNotExist):
#             return self.get(slug=slug)
#         aliases_lower = Func(Func(F("aliases"), function="unnest"), function="LOWER")
#         remove_space = Func(aliases_lower, Value(" "), Value("-"), function="replace")
#         final = Func(remove_space, Value("."), Value(""), function="replace")
#         D = dict(ProteinTF.objects.annotate(aka=final).values_list("aka", "id"))
#         if slug in D:
#             return self.get(id=D[slug])
#         else:
#             raise ProteinTF.DoesNotExist("Protein matching query does not exist.")
# 
    # def get_queryset(self):
    #     return ProteinQuerySet(self.model, using=self._db)

class ProteinTF(models.Model):
    # my_id = models.IntegerField(primary_key=True)
    # id = models.IntegerField(primary_key=True)
    # id = ObjectIdAutoField(primary_key=True)
    gene = models.SlugField(max_length=20)
    satellite = models.CharField(max_length=20)
    validation_grade = models.CharField(max_length=5)
    prediction_method = models.CharField(max_length=100)
    microscopy_result = models.CharField(max_length=200)
    motif_enrichment = models.DecimalField(decimal_places=5, max_digits=10)
    motif_q_score = models.DecimalField(decimal_places=5, max_digits=10)
    existing_images = models.CharField(max_length=100)
    existing_images_link = models.CharField(max_length=200)
    # slug = models.SlugField(max_length=20, blank=True)

    # class Meta:
        # constraints = []

    def __str__(self):
        return self.gene
    
    # def save(self, *args, **kwargs):
    #     if not self.slug:
    #         self.slug = slugify(self.gene)
    #     super().save(*args, **kwargs)

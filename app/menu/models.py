from django.db import models
from django.utils.translation import ugettext_lazy as _





class Dish(models.Model):
    name = models.CharField(_("Nazwa"),\
        max_length=50)
    description = models.TextField(_("Opis"))
    price = models.FloatField(_("Cena"))
    etc = models.DurationField(_("Czas oczekiwania"))
    created = models.DateTimeField(_("Utworzono"),\
        auto_now=False, auto_now_add=False)
    updated = models.DateTimeField(_("Zaktualizowano"),\
        auto_now=False, auto_now_add=False)
    is_vege = models.BooleanField(_("Danie wegańskie"))
    
    class Meta:
        verbose_name = _("Dish")
        verbose_name_plural = _("Dish")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Menu_detail", kwargs={"pk": self.pk})

class Menu(models.Model):
    name = models.CharField(_("Nazwa unikalna menu"), max_length=50)
    dish = models.ManyToManyField(Dish, verbose_name=_("Danie"))
    
    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menu")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Menu_detail", kwargs={"pk": self.pk})

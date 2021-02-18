from django.db import models
from django.utils.translation import ugettext_lazy as _

# Models
class Dish(models.Model):
    name = models.CharField(_("Nazwa"),\
        max_length=50)
    description = models.TextField(_("Opis"))
    price = models.FloatField(_("Cena"))
    etc = models.DurationField(_("Czas oczekiwania"))
    created = models.DateTimeField(_("Utworzono"),\
        auto_now=False, auto_now_add=False,blank=True,null=True)
    updated = models.DateTimeField(_("Zaktualizowano"),\
        auto_now=False, auto_now_add=False,blank=True,null=True)
    is_vege = models.BooleanField(_("Danie wegańskie"))
    
    class Meta:
        verbose_name = _("Danie")
        verbose_name_plural = _("Dania")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Menu_detail", kwargs={"pk": self.pk})

    def get_view_fields(self):
        """ Zwraca widoczne pola instancji """
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]
    
class Menu(models.Model):
    name = models.CharField(_("Nazwa unikalna menu"),unique=True,max_length=50)
    dish = models.ManyToManyField(Dish, verbose_name=_("Danie"))
    created = models.DateTimeField(_("Utworzono"),\
        auto_now=False, auto_now_add=False,blank=True,null=True)
    updated = models.DateTimeField(_("Zaktualizowano"),\
        auto_now=False, auto_now_add=False,blank=True,null=True)
    
    class Meta:
        verbose_name = _("Menu")
        verbose_name_plural = _("Menu")

    def __str__(self):
        return self.name

    def get_absolute_url(self):
        return reverse("Menu_detail", kwargs={"pk": self.pk})

    def get_view_fields(self):
        """ Zwraca widoczne pola instancji """
        return [(field.verbose_name, field.value_to_string(self)) for field in self.__class__._meta.fields]



# Signals
from menu.additional.signals import Signals
from django.db.models.signals import \
    post_save, post_delete, pre_delete, pre_save
from django.dispatch import receiver

@receiver(post_save, sender=Dish)
def dish_update(sender, instance, created, **kwargs):
    """ aktualizacja czasu dodania,aktualizacji """
    s = Signals(model=sender,instance=instance,**kwargs)
    if created:
        s.save_created_date()
    s.save_updated_date()
    
@receiver(post_save, sender=Menu)
def menu_update(sender, instance, created, **kwargs):
    """ aktualizacja czasu dodania,aktualizacji """
    s = Signals(model=sender,instance=instance,**kwargs)
    if created:
        s.save_created_date()
    s.save_updated_date()
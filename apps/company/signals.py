from django.db.models.signals import post_save
from django.dispatch import receiver

from apps.company.models import Company, CompanyDetails


@receiver(post_save, sender=Company)
def create_or_update_company_details(sender, instance, created, **kwargs):
    """Create company details"""
    if created:
        CompanyDetails.objects.create(company=instance)
    instance.company_details.save()

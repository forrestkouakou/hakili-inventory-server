from apps.managers.defaults import GlobalQuerySet


class CompanyQuerySet(GlobalQuerySet):
    def reserved_company_list(self):
        """Returns reserved company_list"""
        return self.filter(id__in=[1])

    def company_list(self):
        """Returns all available company list"""
        return self.exclude(id__in=[1])

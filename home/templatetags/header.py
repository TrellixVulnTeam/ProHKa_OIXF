from django import template
from administration.models import GlobalSetting

# ces templates tags sont utilises afin de ne plus repeter l'operation de fetcher les services sur chaque controlleur
# comme dans le register.inclusion_tag on specifie le chemin du template, on ne va plus l'inclure dans le base.

register = template.Library()

# @register.inclusion_tag("public/header.html")
# def setting():
#     return {"setting":GlobalSetting.objects.get(status=True)}


@register.inclusion_tag("public/footer.html")
def settingFooter():
    return {"setting":GlobalSetting.objects.get(status=True)}
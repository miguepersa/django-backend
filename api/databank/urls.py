from rest_framework.routers import DefaultRouter
from api.databank.views import DataEntryViewSet, RelatedEntryViewSet

router = DefaultRouter()
router.register(r'data_entry', DataEntryViewSet)
router.register(r'program_entry', RelatedEntryViewSet)
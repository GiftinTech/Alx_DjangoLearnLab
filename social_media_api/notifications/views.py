from rest_framework.decorators import api_view, permission_classes
from rest_framework.permissions import IsAuthenticated
from rest_framework.response import Response
from .models import Notification

@api_view(["GET"])
@permission_classes([IsAuthenticated])
def get_notifications(request):
  notifications = Notification.objects.filter(recipient=request.user).order_by("-created_at")
  data = [
    {
      "id": n.id,
      "actor": n.actor.username,
      "verb": n.verb,
      "target_id": n.target_id,
      "created_at": n.created_at,
      "read": n.read,
    }
    for n in notifications
  ]
  return Response(data)

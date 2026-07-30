from rest_framework import generics, permissions
from rest_framework.response import Response
from rest_framework.views import APIView
from .models import Notification
from .serializers import NotificationSerializer


class NotificationListView(generics.ListAPIView):
    serializer_class = NotificationSerializer
    permission_classes = [permissions.IsAuthenticated]

    def get_queryset(self):
        qs = Notification.objects.filter(user=self.request.user.profile)
        unread_only = self.request.query_params.get('unread', None)
        if unread_only and unread_only.lower() == 'true':
            qs = qs.filter(is_read=False)
        return qs


class MarkNotificationReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request, pk):
        notification = Notification.objects.filter(
            id=pk, user=request.user.profile
        ).first()
        if not notification:
            return Response({'detail': 'Notificación no encontrada.'}, status=404)

        notification.is_read = True
        notification.save()
        return Response(NotificationSerializer(notification).data)


class MarkAllNotificationsReadView(APIView):
    permission_classes = [permissions.IsAuthenticated]

    def post(self, request):
        updated = Notification.objects.filter(
            user=request.user.profile, is_read=False
        ).update(is_read=True)
        return Response({'detail': f'{updated} notificaciones marcadas como leídas.'})
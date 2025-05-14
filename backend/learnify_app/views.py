# learnify_app/views.py

from rest_framework import viewsets, status
from rest_framework.response import Response
import requests
from json import JSONDecodeError

from .serializers import ExternalCourseSerializer

class CourseProxyViewSet(viewsets.ViewSet):
    def list(self, request):
        try:
            resp = requests.get(
                'http://54.227.24.251:8000/courses/',
                timeout=30
            )
            resp.raise_for_status()
        except requests.RequestException as e:
            return Response(
                {'detail': 'No se pudo conectar al microservicio externo.', 'error': str(e)},
                status=status.HTTP_503_SERVICE_UNAVAILABLE
            )

        try:
            payload = resp.json()
        except (ValueError, JSONDecodeError) as e:
            return Response(
                {
                    'detail': 'Respuesta inválida del microservicio (no es JSON).',
                    'status_code': resp.status_code,
                    'error': str(e)
                },
                status=status.HTTP_502_BAD_GATEWAY
            )

        if isinstance(payload, list):
            items = payload
        elif isinstance(payload, dict) and 'results' in payload:
            items = payload['results']
        else:
            items = []

        serializer = ExternalCourseSerializer(items, many=True)
        return Response(serializer.data, status=status.HTTP_200_OK)

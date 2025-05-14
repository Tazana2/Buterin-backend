from rest_framework import viewsets, permissions
from .serializers import NftSerializer
from .models import Nft
from rest_framework.views import APIView
from rest_framework.response import Response
from rest_framework import status, permissions
import requests

class NftViewSet(viewsets.ModelViewSet):
    queryset = Nft.objects.all()
    serializer_class = NftSerializer
    permission_classes = [permissions.IsAuthenticatedOrReadOnly]
    
class NftWalletView(APIView):
    permission_classes = [permissions.AllowAny]

    def get(self, request, format=None):
        # Obtener la dirección de la wallet desde los parámetros GET
        wallet_address = request.query_params.get('wallet')
        if not wallet_address:
            return Response(
                {"error": "Se requiere la dirección de la wallet (parámetro 'wallet')."},
                status=status.HTTP_400_BAD_REQUEST
            )

        # Parámetros para la consulta a la API de Rarible
        eth_string = "ETHEREUM"
        max_nfts = 20  # Límite máximo de NFTs a mostrar
        url = f"https://api.rarible.org/v0.1/items/byOwner?blockchains=&owner={eth_string}%3A{wallet_address}"

        headers = {
            "accept": "application/json",
            "X-API-KEY": "24a5ce07-8654-4628-a778-4ceae56cbf1f"
        }
        try:
            response = requests.get(url, headers=headers)
            response.raise_for_status()  # Lanza error si el status no es 200
            data = response.json()
        except Exception as e:
            return Response(
                {"error": str(e)},
                status=status.HTTP_500_INTERNAL_SERVER_ERROR
            )

        filtered_items = []
        # Procesamos solo los primeros 'max_nfts' items
        for item in data.get("items", [])[:max_nfts]:
            meta = item.get("meta", {})
            name = meta.get("name", "Sin nombre")
            
            # Buscar en 'meta.content' la imagen original
            image_url = None
            for content in meta.get("content", []):
                if content.get("@type") == "IMAGE" and content.get("representation") == "ORIGINAL":
                    image_url = content.get("url")
                    break

            # URL adicional (se deja comentado en el endpoint por ahora)
            additional_url = meta.get("originalMetaUri", image_url)
            
            filtered_items.append({
                "name": name,
                "image": image_url,
                # "url": additional_url
            })

        return Response(filtered_items, status=status.HTTP_200_OK)

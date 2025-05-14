import json
import os
import django

# Configurar Django
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "backend.settings")  # Ajusta el nombre de tu proyecto
django.setup()

from nft_app.models import Nft  # Importa el modelo

# Cargar los datos del JSON generado por tu script
json_file_path = "nfts_output.json"

if not os.path.exists(json_file_path):
    print("❌ No se encontró el archivo nfts_output.json")
    exit()

with open(json_file_path, "r") as f:
    nfts_data = json.load(f)

# Insertar NFTs en la base de datos
for nft in nfts_data:
    details = nft.get("nftDetails", {})

    if not details or not details.get("imageUrl") or not details.get("makePrice"):
        print("⚠️  NFT sin detalles, se omite.")
        continue

    nft_obj, created = Nft.objects.get_or_create(
        name=details.get("name", "Sin nombre"),
        defaults={
            "description": details.get("description", ""),
            "image_url": details.get("imageUrl", ""),
            "rarible_url": details.get("raribleUrl", ""),
            "price": details.get("makePrice") or None,
        },
    )

    if created:
        print(f"✅ NFT creado: {nft_obj.name}")
    else:
        print(f"🔁 NFT ya existía: {nft_obj.name}")

print("✅ Población de la base de datos completada.")

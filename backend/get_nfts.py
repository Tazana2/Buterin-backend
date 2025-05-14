import requests
import random
import json
from urllib.parse import quote

def get_collections(api_key, num=10):
    url = f"https://api.nftpricefloor.com/api/projects?qapikey={api_key}"
    try:
        response = requests.get(url)
        if response.status_code == 200:
            collections = response.json()
            return random.sample(collections, min(num, len(collections)))
        return []
    except Exception as e:
        print(f"Error fetching collections: {str(e)}")
        return []

def get_nft_details(blockchain, contract, token_id, api_key):
    blockchains = [
        "APTOS", "ETHEREUM", "POLYGON", "FLOW", "TEZOS", "SOLANA", "IMMUTABLEX", "MANTLE",
        "ARBITRUM", "CHILIZ", "LIGHTLINK", "ZKSYNC", "ASTARZKEVM", "BASE", "RARI", "CELO",
        "FIEF", "XAI", "KROMA", "ZKLINK", "OASYS", "QUAI", "ECLIPSE", "SAAKURU", "OASIS",
        "PALM", "MATCH", "FIVIRE", "SEI", "CAMP", "LISK", "MOONBEAM", "ETHERLINK",
        "ZKCANDY", "ALEPHZERO", "BERACHAIN", "ABSTRACT", "SHAPE", "TELOS", "HEDERAEVM",
        "VICTION", "SETTLUS", "GOAT", "HYPEREVM", "HEDERA", "CROSSFI"
    ]

    if blockchain.upper() in blockchains:
        item_id = f"{blockchain.upper()}:{contract}:{token_id}"
        print(item_id)
        encoded_item = quote(item_id, safe='')
        url = f"https://api.rarible.org/v0.1/items/{encoded_item}"
        headers = {"accept": "application/json", "X-API-KEY": api_key}
        
        try:
            response = requests.get(url, headers=headers)
            if response.status_code == 200:
                return response.json()
            return None
        except Exception as e:
            print(f"Error fetching NFT details: {str(e)}")
            return None

def main():
    # Configuración de APIs
    PRICE_FLOOR_API_KEY = "2114f282-8ddc-4926-863e-e90b7093c263"
    RARIBLE_API_KEY = "24a5ce07-8654-4628-a778-4ceae56cbf1f"
    
    # Obtener colecciones aleatorias
    collections = get_collections(PRICE_FLOOR_API_KEY, 10)
    
    nfts_data = []
    
    for collection in collections:
        try:
            # Extraer datos básicos de la colección
            floor_info = collection.get('stats', {}).get('floorInfo', {})
            token_info = floor_info.get('tokenInfo', {})
            
            if not all([token_info.get('contract'), token_info.get('tokenId')]):
                continue
            
            nft_data = {
                # 'collection': {
                #     'name': collection.get('name'),
                #     'slug': collection.get('slug'),
                #     'floorPriceNative': floor_info.get('currentFloorNative'),
                #     'floorPriceUSD': floor_info.get('currentFloorUsd'),
                #     'stats': collection.get('stats'),
                #     'creator': collection.get('creator'),
                #     'types': collection.get('types'),
                #     'bestPriceUrl': collection.get('bestPriceUrl')
                # },
                # 'tokenInfo': token_info,
                # 'nftDetails': None
            }
            
            # Obtener detalles del NFT
            details = get_nft_details(
                token_info.get('blockchain', 'ethereum').lower(),
                token_info['contract'],
                token_info['tokenId'],
                RARIBLE_API_KEY
            )
            
            if details:
                nft_data['nftDetails'] = {
                    'name': details.get('meta', {}).get('name'),
                    'description': details.get('meta', {}).get('description'),
                    'imageUrl': next((c['url'] for c in details.get('meta', {}).get('content', []) if c['@type'] == 'IMAGE'), None),
                    # 'attributes': details.get('meta', {}).get('attributes', []),
                    'raribleUrl': f"https://rarible.com/token/{token_info['contract']}:{token_info['tokenId']}",
                    'makePrice': details.get('bestSellOrder', {}).get('makePrice'),
                }
            
            nfts_data.append(nft_data)
            
        except Exception as e:
            print(f"Error processing collection: {str(e)}")
            continue
    
    # Guardar resultados en JSON
    with open('nfts_output.json', 'w') as f:
        json.dump(nfts_data, f, indent=2)
    
    # Imprimir información requerida
    for index, nft in enumerate(nfts_data, 1):
        details = nft.get('nftDetails') or {}  # Asegurar que siempre sea un diccionario
        try:
            collection_name = nft['collection']['name'] or 'Colección desconocida'
        except KeyError:
            collection_name = 'Colección desconocida'
        
        print(f"\n=== NFT {index} ({collection_name}) ===")
        
        if not nft.get('nftDetails'):
            print("⚠️  No se pudieron obtener detalles del NFT")
            continue
            
        # Si llegamos aquí, hay detalles del NFT
        print(f"Nombre: {details.get('name', 'Sin nombre')}")
        
        # Manejo de imagen
        image_url = details.get('imageUrl')
        if image_url:
            print(f"Imagen: {image_url}")
        else:
            print("Imagen: No disponible")
            
        # Enlace Rarible
        rarible_url = details.get('raribleUrl', '')
        if rarible_url:
            print(f"Enlace: {rarible_url}")
        else:
            print("Enlace: No disponible")

if __name__ == "__main__":
    main()
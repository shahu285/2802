import requests

r = requests.get('http://127.0.0.1:8001/api/posts/pending')
data = r.json()

print(f'\n📊 Total pending posts: {len(data)}\n')
print('='*70)

for i, p in enumerate(data, 1):
    print(f'{i}. [{p["severity_tier"]}] {p["source_feed"]}')
    print(f'   {p["raw_headline"][:70]}...')
    print()

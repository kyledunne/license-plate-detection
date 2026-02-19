from pathlib import Path
import pandas as pd

BASE = Path('data/license_plates')

for split in ('train', 'val'):
    images_dir = BASE / split / 'images'
    ids = sorted(p.stem for p in images_dir.glob('*.jpg'))
    pd.DataFrame({'id': ids}).to_csv(f'data/{split}.csv', index=False)
    print(f'{split}.csv: {len(ids)} rows')

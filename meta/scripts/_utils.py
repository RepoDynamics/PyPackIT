
from pathlib import Path


path = {'root': Path(__file__).parents[2].resolve()}
path['src'] = path['root'] / 'src'
path['github'] = path['root'] / '.github'
path['local_outputs'] = path['root'] / 'data' / '_local_outputs'
path['metadata'] = [
    path['root'] / 'meta' / 'metadata' / f'{filename}.yaml'
    for filename in {'project', 'website', 'maintainers', 'paths'}
] + [path['src'] / 'metadata.yaml']
path['template_health_files'] = path['root'] / 'meta' / 'templates' / 'health_files'
path['template_licenses'] = path['root'] / 'meta' / 'templates' / 'licenses'
path['config'] = path['root'] / 'meta' / 'config'

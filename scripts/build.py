from frictionless import Package
from datetime import datetime
from scripts.pipelines import build_pipeline

def build_package(descriptor: str = 'datapackage.json'):
    package = Package(descriptor)
    package.transform(build_pipeline)
    package.custom['updated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    package.to_json(descriptor)

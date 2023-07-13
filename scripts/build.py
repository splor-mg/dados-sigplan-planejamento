from frictionless import Package, Resource
from datetime import datetime
from scripts.pipelines import build_pipeline

def build_package(source_descriptor: str = 'datapackage.yaml', target_descriptor: str = 'datapackage.json'):
    
    source = Package(source_descriptor)

    target = Package.from_descriptor({
        "name": source.name,
        "resources": [
            {
            "profile": "tabular-data-resource",
            "name": resource_name,
            "path": f'data/{resource_name}.csv',
            "format": "csv",
            "encoding": "utf-8",
            "schema": {"fields": []}
            } for resource_name in source.resource_names
        ]
    })
    
    target.transform(build_pipeline)
    target.custom['updated_at'] = datetime.now().strftime('%Y-%m-%dT%H:%M:%S')
    output = target.to_dict()
    for resource_name in target.resource_names:
        resource_descriptor = Resource(f'logs/transform/{resource_name}.json').to_descriptor()
        output['resources'] = [
        resource_descriptor if resource['name'] == resource_name else resource
        for resource in output['resources']
    ]
    
    Package.from_descriptor(output).to_json(target_descriptor)

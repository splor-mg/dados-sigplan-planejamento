from frictionless import Package

def init_package(source_descriptor: str = 'datapackage.yaml', target_descriptor: str = 'datapackage.json'):

    package = Package(source_descriptor)

    descriptor = {
        "profile": "tabular-data-package",
        "name": package.name,
        "resources": [
            {
            "profile": "tabular-data-resource",
            "name": resource_name,
            "path": f'data/{resource_name}.csv',
            "format": "csv",
            "encoding": "utf-8",
            "schema": {"fields": []}
            } for resource_name in package.resource_names
        ]
    }

    target = Package.from_descriptor(descriptor)
    target.to_json(target_descriptor)

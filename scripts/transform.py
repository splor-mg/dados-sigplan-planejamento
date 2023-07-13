from frictionless import Package
import logging
from scripts.pipelines import transform_pipeline

logger = logging.getLogger(__name__)

def transform_resource(resource_name: str, source_descriptor: str = 'datapackage.yaml', target_descriptor: str = 'datapackage.json'):
    logger.info(f'Transforming resource {resource_name}')
    
    source = Package(source_descriptor)
    resource = source.get_resource(resource_name)
    resource.transform(transform_pipeline)
    target = Package(target_descriptor).to_descriptor()
    target_resource = resource.to_descriptor()
    target['resources'] = [
        target_resource if resource['name'] == resource_name else resource
        for resource in target['resources']
    ]
    
    Package.from_descriptor(target).to_json(target_descriptor)

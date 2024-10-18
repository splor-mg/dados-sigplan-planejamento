import logging
from frictionless import Package, Checklist
import petl
from frictionless import validate

logger = logging.getLogger(__name__)

def validate_package(descriptor: str, stop_on_failure: bool = False):
    package = Package(descriptor)
    
    report = validate(descriptor)

    report_fields = ['title', 'rowNumber', 'fieldNumber', 'fieldName', 'description', 'message', 'note']
    errors = [['resource'] + report_fields]

    for resource in package.resources:
        try:
            report = resource.validate(limit_errors = 100) #checklist, 
            data = report.flatten(report_fields)
            table = [report_fields] + data
            table = petl.addfield(table, 'resource', resource.name, 0)
            errors = petl.cat(errors, table)
        except Exception as err:
            logger.error("%s: Unexpected error: %s", resource.name, err)         
   
    if errors.data():        
        unique_errors = petl.cut(errors, ["resource", "fieldName", "title", "description", "note"]).distinct().records()
        for row in unique_errors:
            logger.warning(f"{row.resource}: Coluna '{row.fieldName}' | Erro '{row.title}' | Descrição '{row.description}' | Regra '{row.note}'")
    
        if stop_on_failure == True: 
            raise Exception(errors)

    return errors
   
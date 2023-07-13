from frictionless import Pipeline
from dpm.steps import field_rename_to_target, table_write_normalized

transform_pipeline = Pipeline(steps=[
    field_rename_to_target(),
    table_write_normalized(output_dir = 'data'),
])

build_pipeline = Pipeline(steps=[

])

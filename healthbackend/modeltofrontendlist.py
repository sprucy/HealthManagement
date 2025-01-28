#from django.db.models import get_app, get_models, get_model

from pathlib import Path
backendPath=Path(f'D:/pythonprj/django/healthbackend')
frontendPath=Path(f'D:/reactadmin/test-admin/src')
app=Path('api')
modelfile=Path('models.py')


print(backendPath/app/modelfile)
import os
import django
from django.apps import apps
os.environ.setdefault("DJANGO_SETTINGS_MODULE", "healthbackend.settings")
django.setup() 




models=apps.get_app_config('api').models
for model in models:
    modelname = models[model]._meta.model_name
    filename = modelname+'.tsx'

    with open(frontendPath/filename, 'w', encoding='utf-8') as f:
        tsstr = f'import {{ List, Datagrid, TextField, EmailField, BooleanField, NumberField, DateField, ImageField, FileField, UrlField, ReferenceField, ReferenceOneField, ReferenceManyToManyField }} from "react-admin";' 
        f.write(tsstr)
        #print(model)
        #print(models[model]._meta.verbose_name)
        #print(models[model]._meta.verbose_name_plural)
        modelname = modelname.title()
        print(f'正在生成{modelname}List.tsx...')

        tsstr = f'\n\nexport const {modelname}List = () => ('
        f.write(tsstr)
        tsstr = f'\n  <List title="{models[model]._meta.verbose_name_plural}">'
        f.write(tsstr)
        tsstr = f'\n    <Datagrid  rowClick="edit">'
        f.write(tsstr)
        for field in models[model]._meta.get_fields():
            if field.__class__.__name__ == 'CharField':
                tsstr = f'<TextField source="{field.name}" />'
            elif field.__class__.__name__ == 'TextField':
                tsstr = f'<TextField source="{field.name}" />'
            elif field.__class__.__name__ == 'BooleanField':
                tsstr = f'<BooleanField source="{field.name}" />'
            elif field.__class__.__name__ == 'BigAutoField':
                tsstr = f'<TextField source="{field.name}" />'
            elif field.__class__.__name__ == 'AutoField':
                tsstr = f'<TextField source="{field.name}" />'
            elif field.__class__.__name__ == 'SmallIntegerField':
                tsstr = f'<NumberField source="{field.name}" />'
            elif field.__class__.__name__ == 'IntegerField':
                tsstr = f'<NumberField source="{field.name}" />'
            elif field.__class__.__name__ == 'DecimalField':
                tsstr = f'<NumberField source="{field.name}" />'
            elif field.__class__.__name__ == 'PositiveIntegerField':
                tsstr = f'<NumberField source="{field.name}" />'
            elif field.__class__.__name__ == 'PositiveSmallIntegerField':
                tsstr = f'<NumberField source="{field.name}" />'
            elif field.__class__.__name__ == 'FloatField':
                tsstr = f'<NumberField source="{field.name}" />'
            elif field.__class__.__name__ == 'DateField':
                tsstr = f'<DateField source="{field.name}" />'
            elif field.__class__.__name__ == 'TimeField':
                tsstr = f'<DateField source="{field.name}" />'
            elif field.__class__.__name__ == 'DateTimeField':
                tsstr = f'<DateField source="{field.name}" />'
            elif field.__class__.__name__ == 'EmailField':
                tsstr = f'<EmailField source="{field.name}" />'
            elif field.__class__.__name__ == 'ImageField':
                tsstr = f'<ImageField source="{field.name}" />'
            elif field.__class__.__name__ == 'FileField':
                tsstr = f'<FileField source="{field.name}" />'
            elif field.__class__.__name__ == 'FilePathField':
                tsstr = f'<FileField source="{field.name}" />'
            elif field.__class__.__name__ == 'URLField':
                tsstr = f'<UrlField source="{field.name}" />'
            elif field.__class__.__name__ == 'ForeignKey':
                tsstr = f'<ReferenceField source="{field.name}" />'
            elif field.__class__.__name__ == 'ManyToManyField':
                tsstr = f'<ReferenceManyToManyField source="{field.name}" />'
            elif field.__class__.__name__ == 'OneToOneField':
                tsstr = f'<ReferenceOneField source="{field.name}" />'
            else:
                tsstr = f'<TextField source="{field.name}" {field.__class__.__name__} />'
            ''' 
            elif field.__class__.__name__ == 'GenericIPAddressField':
                tsstr = f'<TextField source="{field.name}" />'
            elif field.__class__.__name__ == 'SlugField':
                tsstr = f'<TextField source="{field.name}" />'
            elif field.__class__.__name__ == 'UUIDField':
                tsstr = f'<TextField source="{field.name}" />'            
            elif field.__class__.__name__ == 'ManyToOneRel':
                tsstr = f'<TextField source="{field.name}" />'
            elif field.__class__.__name__ == 'OneToOneRel':
                tsstr = f'<TextField source="{field.name}" />'
            elif field.__class__.__name__ == 'ManyToManyRel':
                tsstr = f'<TextField source="{field.name}" />'
            '''
            tsstr = f'\n      {tsstr}' 
            f.write(tsstr)

        tsstr = f'\n    </Datagrid>'
        f.write(tsstr)
        tsstr = f'\n  </List>'
        f.write(tsstr)
        tsstr = f'\n);'
        f.write(tsstr)
    #print(models[model]._meta.app_label)
    #print(models[model]._meta.db_table)

print('end')
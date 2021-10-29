import warnings
import cerberus
import json
warnings.simplefilter("ignore", UserWarning)
        
class Validator(cerberus.Validator):
    def __init__(self, schema, *args, **kwargs):
        super().__init__(schema, *args, **kwargs)
        self._ordered = kwargs.get('_ordered', False)

    def validate(self, document, schema=None, update=False, normalize=True):
        schema = schema or self.schema
        if schema is not None:
            root_schema = schema.get('__root__', None)
            if root_schema:
                document = {'__root__': document}
        result = super(Validator, self).validate(document, schema, update, normalize)
        if self.document.get('__root__'):
            # Unwrap.
            self.wrapped = self.document
            self.document = self.document['__root__']
            for e in self._errors:
                e.schema_path = tuple(e.schema_path[1:])
                if len(e.document_path) > 1:
                    e.document_path = tuple(e.document_path[1:])
        return result
    
    def normalized(self, document=None, schema=None, *args, **kwargs):
        document = document or self.document
        schema = schema or self.schema
        if schema is not None:
            root_schema = schema.get('__root__', None)
            if root_schema:
                document = {'__root__': document}
        self.document = super(Validator, self).normalized(document, schema, *args, **kwargs)
        if self.ordered:
            self.document = dict(sorted(self.document.items(), key=lambda x: -1 if x[0] == 'kind' else schema[x[0]].get('order', float('inf')))) 
        if self.document.get('__root__'):
            # Unwrap.
            self.wrapped = self.document
            self.document = self.document['__root__']
            for e in self._errors:
                e.schema_path = tuple(e.schema_path[1:])
                if len(e.document_path) > 1:
                    e.document_path = tuple(e.document_path[1:])
        return self.document

    def _validate_order(self, constraint, field, value):
        '''For use YAML Editor'''
    
    def _validate_selector(self, constraint, field, value):
        _errors = []
        default_key = next(iter(constraint)).title()
        for k, v in reversed(constraint.items()):
            v['kind'] = {
                'type': 'string',
                'allowed': [k.title()],
                'required': True,
                'default': default_key,
                'order': 0
            }
            sub_schema = json.loads(json.dumps(v))
            #validator = Validator(sub_schema)
            validator = self.__class__(sub_schema)
            if validator.validate(value):
                new_schema = dict(self.schema)
                del new_schema[field]['selector']
                new_schema[field]['schema'] = dict(validator.schema)
                self.schema = new_schema
                self.document[field] = validator.document
                return
            _errors = validator._errors
            if not validator.errors.get('kind'):
                break
        if _errors:
            def update_document_path(errors):
                if isinstance(errors, list):
                    for error in errors:
                        if field == '__root__':
                            error.document_path = (*self.document_path, *error.document_path)
                        else:
                            error.document_path = (*self.document_path, field, *error.document_path)
                        if error.info:
                            for info in error.info:
                                update_document_path(info)
            update_document_path(_errors)
            self._error(_errors)

    def normalized_by_order(self, document=None, schema=None, *args, **kwargs):
        return Validator(schema, _ordered=True).normalized(
            document or self.document, 
            schema or self.schema,
            *args, **kwargs)

    @property
    def ordered(self):
        return self._ordered if hasattr(self, '_ordered') else False
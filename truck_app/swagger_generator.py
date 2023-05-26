from drf_yasg.generators import OpenAPISchemaGenerator


class CustomOpenAPISchemaGenerator(OpenAPISchemaGenerator):
    def get_schema(self, request=None, public=False):
        swagger = super().get_schema(request, public)
        swagger.tags = [
            {"name": "goods", "description": "View goods and nearby trucks (has filters), add and edit goods"},
            {"name": "truck", "description": "View and edit truck"},
            {"name": "token", "description": "Get and refresh JWT"},
        ]

        return swagger

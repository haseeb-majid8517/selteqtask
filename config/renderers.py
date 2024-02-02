from rest_framework.renderers import JSONRenderer


class CustomSELTEQCustomRenderer(JSONRenderer):
    def render(self, data, accepted_media_type=None, renderer_context=None):
        status_code = renderer_context["response"].status_code
        response = {
            "status": "success",
            "status_code": status_code,
            "data": data,
            "message": None,
        }

        if not str(status_code).startswith("2"):
            response["status"] = "error"
            response["data"] = None
            try:
                response["message"] = data["detail"]
            except KeyError:
                response["message"] = data
            except TypeError:
                response["message"] = "No data" if data is None else data
            except Exception as e:
                response["message"] = str(e)
        return super().render(response, accepted_media_type, renderer_context)

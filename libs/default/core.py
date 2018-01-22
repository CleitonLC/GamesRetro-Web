from django.core.exceptions import ValidationError

from modules.core.config import ERRORS_MESSAGES
from datetime import date, datetime, timedelta
from django.http import Http404, HttpResponse

from django.contrib.auth import login
from django.db import IntegrityError
from django.core import serializers
from GamesRetro import settings
import datetime
import json
import sys


def json_serial(obj):
    """JSON serializer for objects not serializable by default json code"""
    if isinstance(obj, (datetime, date, timedelta)):
        return obj.isoformat()
    raise TypeError ("Type %s not serializable" % type(obj))


class Notify:



    def datalist(self, datalist, list_fields=None, extra_fields=None):
        response_dict = []
        for item in datalist:
            response_data = self.__format_serialized_model(item, list_fields)
            if extra_fields is not None:
                for item in extra_fields:
                    response_data[item] = None
            response_dict.append(response_data)
        return response_dict

    def success(self, object, message='', list_fields=None):
        return self.__response_format(True, message, object, list_fields)

    def error(self, exceptions):
        return self.__response_format(False,self.__format_exceptions(exceptions),None, None)

    def __response_format(self,result, message, obj=None, list_fields=None):
        response_dict = {}
        response_dict['result'] = result
        response_dict['message'] = message
        if result:
            response_dict['object'] = self.__format_serialized_model(obj, list_fields)
        else:
            response_dict['object'] = None
        return response_dict

    def __format_serialized_model(self,object,list_fields=None):
        if list_fields is not None:
            response_model = serializers.serialize('json', [object], fields=tuple(list_fields))
        else:
            response_model = serializers.serialize('json', [object])

        response_model = json.loads(response_model)[0]
        response_model = response_model['fields']
        response_model['id'] = object.id
        response_model['selected'] = ''
        return response_model




    def __format_exceptions(self,exceptions):
        message_dict = {}

        if type(exceptions) == dict:
            message_dict = exceptions

        elif isinstance(exceptions,ValidationError):
            try:
                for item in exceptions.error_dict:
                    field = item
                    exception = exceptions.error_dict[field][0]
                    error_code = exception.code
                    value = exception.args[0]
                    if ': ' in value:
                        value = value.split(": ")[1]
                    message_dict[field] = ERRORS_MESSAGES[error_code]#value
            except Exception as error:
                print("ERRO INTERNO: ",error)
                message_dict = error

        elif isinstance(exceptions,IntegrityError):
            params = exceptions.args[0].split(": ")
            field = params[1].split('.')[1]
            value = ERRORS_MESSAGES["unique"]
            message_dict[field] = value

        else:
            print("ERRO! VERIFIQUE A EXCESSAO: ",exceptions, type(exceptions))
            #paramters = exceptions.args[0].split(': ')
            #code_status = exceptions.args[1]
            #field = paramters[0]
            # value = paramters[1]
            #message_dict[field] = ERRORS_MESSAGES[code_status]
            message_dict = exceptions.args[0]
        return message_dict


class BaseController(Notify):
    request = None
    notify = Notify()
    server_startup_time_process = None
    server_terminate_time_process = None
    server_processing_time = None

    def filter(self, request, model=None, queryset=None, order_by="-id", list_fields=None, limit=None, extra_fields=None):
        response_dict = {}
        response_dict['result'] = True
        response_dict['object'] = self.notify.datalist(model_list, list_fields,extra_fields)
        response_dict['message'] = str(len(self.notify.datalist(model_list, list_fields)))+" Registros carregados com sucesso!"
        print('SOU RESPONSE',response_dict)
        return self.response(response_dict)

    def object(self, request):
        self.request = request
        pass

    def execute(self, object, action):
        try:
            action()
            if object is not None:
                response_dict = self.notify.success(object)
            else:
                response_dict = self.notify.success(object)
        except Exception as e:
            response_dict = self.notify.error(e)
        return response_dict

    def get_exceptions(self, object, form):
        """
        Metodo responsavel por tentar capturar erro no formulario e modelo e retornar tudo junto
        """
        self.model_exceptions = {}
        if object is not None:
            try:
                object.full_clean()

            except Exception as exception:
                print("DEU ERRO: ",exception)
                self.model_exceptions = exception.message_dict

        self.full_exceptions = {}
        if form is not None:
            self.form_exceptions = form.format_validate_response()
        else:
            self.form_exceptions = {}

        print("FORM EXCEPTIONS: ", self.form_exceptions)
        print("MODEL EXCEPTIONS: ", self.model_exceptions)

        self.full_exceptions.update(self.model_exceptions)
        self.full_exceptions.update(self.form_exceptions)
        return self.notify.error(self.full_exceptions)

    def response(self, response_dict):
        import sys
        try:
            self.terminate_process()
            response_dict['status'] = {}
            response_dict['status']['request_path'] = self.__request_path
            response_dict['status']['request_size'] = self.__request_bytes
            response_dict['status']['response_size'] = "RESPONSE_SIZE"
            response_dict['status']['server_processing_time_duration'] = self.server_processing_time.total_seconds()  # datetime.datetime.now()
            response_dict['status']['cliente_processing_time_duration'] = ''
        except:
            pass

        print("VEJA O RESPONSE NO FINAL: ", response_dict)
        data = json.dumps(response_dict, default=json_serial)
        try:
            data = data.replace('RESPONSE_SIZE', str(sys.getsizeof(data) - 16))
        except:
            pass
        response = HttpResponse(data)  # after generate response noramlization reduce size in 16 bytes
        return response

    def filter_request(self, request, formulary=None):
        if request.is_ajax() or settings.DEBUG:
            if formulary is not None:
                form = formulary(request.POST)
                if form.is_valid():
                    return True, form
                else:
                    return False, form
            else:
                return True, True
        else:
            raise Http404


class BaseForm:

    request = None

    def format_validate_response(self):
        response_errors = {}
        if self.errors:
            errors = self.errors
            for campo in errors:
                response_errors[campo] = []
                for erro in errors[campo]:
                    erro_format = str(erro)
                    erro_format = erro_format.replace("['", "")
                    erro_format = erro_format.replace("']", "")
                    response_errors[campo].append(erro_format)
        return response_errors

    def get_object(self, object_id=None):
        if object_id is not None:
            print("veja o self.model",self.model)
            object = self.model.objects.get(pk=int(object_id))
            print("peguei o objeto")
        else:
            print('objeto vazio')
            object = self.model()
            print("pego o MOdelo")

        for attribute in self.data:
            value = self.data[attribute]
            if attribute != 'csrfmiddlewaretoken':
                if '[]' in attribute:
                    print("ATRIBUTO: ",attribute," - ",value," ReQUEST: ",self.request)
                    options_selected = self.request.POST.getlist(attribute)
                    if options_selected is not None:
                        value = ';'.join(map(str, self.request.POST.getlist(attribute)))
                    attribute = attribute.replace("[]", "")
                else:
                    if attribute != 'id':
                        if self.data[attribute] != "null" and self.data[attribute] != 'None':
                            try:
                                field = self.fields[attribute]
                                value = field.to_python(self.data[attribute])
                            except KeyError as error:
                                pass

                        else:
                            value = None
                #print("ATRIBUTO: ",attribute,': ',value)
                setattr(object, attribute , value)
        return object
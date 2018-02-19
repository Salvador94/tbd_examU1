from django.core.exceptions import ValidationError

num = ('1','2','3','4','5','6','7','8','9','0')


def Validate_studio(value):
    for i in num:
        if i in value:
            raise ValidationError("No ingresar numeros")
        else:
            continue
    return value

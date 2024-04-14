from rest_framework import serializers
from products.models import Category,Brand,Product,Comment



def id_validator(id,model,model_name):
    model_id=model.objects.filter(id=id)

    if model_id.exists():
        return id
    else:
        raise serializers.ValidationError(
            f"There Is No {model_name} With The Id Of {id}"
        )

def category_id_validator(id):
    id_validator(id,Category,'Category')

def brand_id_validator(id):
    id_validator(id,Brand,'Brand')

def product_id_validator(id):
    id_validator(id,Product,'Product')


def reply_to_id_validator(id):
    q=Comment.objects.filter(id=id)
    if q.exists():
        if q[0].reply_to is not None:
            raise serializers.ValidationError(
                "Can Reply To A Reply. Only One Level Of Reply Possible"
            )
        return id
    else:
        raise serializers.ValidationError(
            f"There Is No Comment With The Id Of {id}"
        )
    


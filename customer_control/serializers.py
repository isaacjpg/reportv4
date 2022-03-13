from rest_framework import serializers
from .models import Customer, Contact, Address
from user_control.serializers import CustomUserSerializer



class ContactSerializer(serializers.ModelSerializer):
    customer_id=serializers.CharField(write_only=True)
    class Meta:
        model = Contact
        fields = ('id','customer_id', 'fullname', 'phone', 'email')

class ContactDataSerializer(serializers.Serializer):
    fullname = serializers.CharField(max_length=255)
    phone = serializers.CharField(max_length=255)
    email = serializers.EmailField() 

class AddressSerializer(serializers.ModelSerializer):
    customer_id=serializers.CharField(write_only=True)
    class Meta:
        model = Address
        fields = ('id','customer_id','street', 'number', 'region', 'comune')

class AddressDataSerializer(serializers.Serializer):
    street = serializers.CharField(max_length=255)
    number = serializers.CharField(max_length=255)
    region = serializers.CharField(max_length=255)
    comune= serializers.CharField(max_length=255)


class CustomerSerializer(serializers.ModelSerializer):
    created_by=CustomUserSerializer(read_only=True)
    created_by_id=serializers.CharField(write_only=True,required=False)
    updated_by=CustomUserSerializer(read_only=True)
    updated_by_id=serializers.CharField(write_only=True,required=False)
    contacts=ContactSerializer(many=True,read_only=True)
    contacts_data=ContactDataSerializer(many=True,write_only=True)
    addresses=AddressSerializer(many=True,read_only=True)
    addresses_data=AddressDataSerializer(many=True,write_only=True)
    

    class Meta:
        model = Customer
        fields = '__all__'

    def create(self, validated_data):
      contacts_data=validated_data.pop('contacts_data')
      addresses_data=validated_data.pop('addresses_data')
      

      if not contacts_data:
        raise Exception("No se ha ingresado ningun contacto")

      if not addresses_data:
        raise Exception ("No se ha ingresado ninguna direccion")
      
      customer=super().create(validated_data)
      print(customer.id)
      contacts_data_serializer=ContactSerializer(data=[{"customer_id":customer.id,**contact} for contact in contacts_data],many=True)

      if contacts_data_serializer.is_valid():
        contacts_data_serializer.save()
      else:
        customer.delete()
        raise Exception(contacts_data_serializer.errors)

      addresses_data_serializer=AddressSerializer(data=[{"customer_id":customer.id,**address_data} for address_data in addresses_data],many=True)

      if addresses_data_serializer.is_valid():
        addresses_data_serializer=addresses_data_serializer.save()
      else:
        customer.delete()
        raise Exception(addresses_data_serializer.errors)

      return customer

    def update(self,instance,validated_data):
      contacts_data=validated_data.pop('contacts_data')
      addresses_data=validated_data.pop('addresses_data')

      if not contacts_data:
        raise Exception("No se ha ingresado ningun contacto")

      if not addresses_data:
        raise Exception ("No se ha ingresado ninguna direccion")

      customer=super().update(instance,validated_data)

      contacts_data_serializer=ContactSerializer(data=[{"customer_id":customer.id,**contact_data} for contact_data in contacts_data],many=True)

      if contacts_data_serializer.is_valid():
        customer.contacts.all().delete()
        contacts_data_serializer.save()
      else:
        raise Exception(contacts_data_serializer.errors)

      addresses_data_serializer=AddressSerializer(data=[{"customer_id":customer.id,**address_data} for address_data in addresses_data],many=True)

      if addresses_data_serializer.is_valid():
        customer.addresses.all().delete()
        addresses_data_serializer=addresses_data_serializer.save()
      else:
        customer.delete()
        raise Exception(addresses_data_serializer.errors)

      return customer
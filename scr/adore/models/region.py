from django.db.models import *


class Region(Model):
    name = CharField(max_length=255)

    class Meta:
        verbose_name = "Region"
        verbose_name_plural = "Regions"
        db_table = "region"

    def __str__(self):
        return self.name


class District(Model):
    name = CharField(max_length=255)
    region = ForeignKey('Region', CASCADE, related_name='district')

    class Meta:
        verbose_name = "District"
        verbose_name_plural = "Districts"
        db_table = "district"

    def __str__(self):
        return self.name


class Mahalla(Model):
    name = CharField(max_length=255)
    district = ForeignKey('District', CASCADE, related_name='mahalla')

    class Meta:
        verbose_name = "Mahalla"
        verbose_name_plural = "Mahallas"
        db_table = "mahalla"

    def __str__(self):
        return self.name


class Address(Model):
    mahalla = ForeignKey('Mahalla', CASCADE, related_name='address')
    street = CharField(max_length=255)
    house = CharField(max_length=255)

    class Meta:
        verbose_name = "Address"
        verbose_name_plural = "Addresses"
        db_table = "address"

    def __str__(self):
        return f"{self.mahalla.district.region.name}, {self.mahalla.district.name}, {self.mahalla.name}, {self.street}, {self.house}"

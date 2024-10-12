from django.urls import reverse
from .models import (
    Brand,
    Model,
    BodyType,
    Colour,
    VehicleTypeNumber,
    Vehicle
)
from apps.package.models import (
    Subscription,
    Package,
    CustomPackage
)
from apps.features.models import (
    MultimediaFeature,
    SafetyAssistanceFeature,
    StandardFeature,
    OptionalFeature
)
from datetime import datetime
from apps.users.models import User
from tests.base import BaseTestCase
from rest_framework import status
from django.core.files.uploadedfile import SimpleUploadedFile
import json


class BrandTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Brand record
        self.data = {
            "vehicle_type": 1,
            "name": "Test Brand",
            "is_active": True
        }

    def test_create_brand(self):
        url = reverse("brand-list")
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        data = json.loads(response.content)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results').get('name'), "Test Brand")
    
    def test_retrieve_brand(self):
        # Create an instance first
        brand = Brand.objects.create(name="Test Brand", vehicle_type=1)

        url = reverse("brand-detail", args=[brand.uuid])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Test Brand")
    
    def test_update_brand(self):
        # Create an instance first
        brand = Brand.objects.create(name="Test Brand", vehicle_type=1)
        
        url = reverse("brand-detail", args=[brand.uuid])
        updated_data = {"name": "Updated Brand", "vehicle_type": 1, "is_active": True}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results').get('name'), "Updated Brand")

    def test_partial_update_brand(self):
        # Create an instance first
        brand = Brand.objects.create(name="Test Brand", vehicle_type=1)
        
        url = reverse("brand-detail", args=[brand.uuid])
        updated_data = {"name": "Partially Updated Brand"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        data = json.loads(response.content)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results').get('name'), "Partially Updated Brand")

    def test_delete_brand(self):
        # Create an instance first
        brand = Brand.objects.create(name="Test Brand", vehicle_type=1)
        
        url = reverse("brand-detail", args=[brand.uuid])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertFalse(Brand.objects.filter(id=brand.id).exists())


class ModelTestCase(BaseTestCase):
    def setUp(self):
        self.brand = Brand.objects.create(name='Test Brand')
        self.model_data = {
            'brand': str(self.brand.uuid),
            'name': 'Test Model',
            'is_active': True,
        }
        
        # Create a temporary image file for testing
        self.image = SimpleUploadedFile("test_image.jpg", b"file_content", content_type="image/jpeg")
    
    def test_create_model(self):
        url = reverse('model-list')  # You need to replace 'model-list' with the actual name of your URL route
        response = self.client.post(url, self.model_data, format='multipart')
        data = json.loads(response.content)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results').get('name'), "Test Model")
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)

    def test_retrieve_model(self):
        model = Model.objects.create(brand=self.brand, name='Test Model', is_active=True)
        url = reverse('model-detail', kwargs={'uuid': model.uuid})  # You need to replace 'model-detail' with the actual name of your URL route
        response = self.client.get(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Test Model')

    def test_delete_model(self):
        model = Model.objects.create(brand=self.brand, name='Test Model', is_active=True)
        url = reverse('model-detail', kwargs={'uuid': model.uuid})  # You need to replace 'model-detail' with the actual name of your URL route
        response = self.client.delete(url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Model.objects.filter(uuid=model.uuid).exists())


class BodyTypeTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.do_login()
        self.body_type = BodyType.objects.create(name="Sedan", is_active=True)
        self.create_url = reverse('body-type-list')
        self.detail_url = reverse('body-type-detail', kwargs={'uuid': self.body_type.uuid})

    def test_create_body_type(self):
        data = {
            'name': 'Hatchback',
            'is_active': True
        }
        response = self.client.post(self.create_url, data, format='json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results').get('name'), "Hatchback")

    def test_retrieve_body_type(self):
        response = self.client.get(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Sedan')

    def test_update_body_type(self):
        data = {
            "name": "SUV",
            "is_active": False
        }
        response = self.client.put(self.detail_url, json.dumps(data), content_type="application/json")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results').get('name'), "SUV")
        self.assertFalse(data.get('results').get('is_active'))

    def test_partial_update_body_type(self):
        data = {
            "name": "Virtus"
        }
        response = self.client.patch(self.detail_url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results').get('name'), "Virtus")
        self.assertTrue(data.get('results').get('is_active'))

    def test_delete_body_type(self):
        response = self.client.delete(self.detail_url)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(BodyType.objects.filter(pk=self.body_type.pk).exists())


class ColourTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.do_login()
        self.colour = Colour.objects.create(name='Red', code='FF0000', is_active=True)
        self.create_url = reverse('color-list')
        self.detail_url = reverse('color-detail', kwargs={'uuid': self.colour.uuid})

    def test_create_colour(self):
        data = {
            'name': 'Blue',
            'code': '0000FF',
            'is_active': True
        }
        response = self.client.post(self.create_url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results')['name'], 'Blue')
        self.assertEqual(data.get('results')['code'], '0000FF')

    def test_retrieve_colour(self):
        response = self.client.get(self.detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['name'], 'Red')
        self.assertEqual(response.data['code'], 'FF0000')

    def test_update_colour(self):
        data = {
            'name': 'Green',
            'code': '00FF00',
            'is_active': False
        }
        response = self.client.put(self.detail_url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertIn('name', data.get('results'))
        self.assertEqual(data.get('results')['name'], 'Green')
        self.assertEqual(data.get('results')['code'], '00FF00')
        self.assertFalse(data.get('results')['is_active'])

    def test_partial_update_colour(self):
        data = {
            'code': '00FFFF'
        }
        response = self.client.patch(self.detail_url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get('results')['name'], 'Red')
        self.assertEqual(data.get('results')['code'], '00FFFF')

    def test_delete_colour(self):
        response = self.client.delete(self.detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Colour.objects.filter(pk=self.colour.pk).exists())


class VehicleTypeNumberTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.do_login()

        self.brand = Brand.objects.create(name='Test Brand')
        self.model = Model.objects.create(name='Test Model', brand=self.brand)
        self.vehicle_type_number = VehicleTypeNumber.objects.create(
            brand=self.brand,
            model=self.model,
            chasis_number='12345',
            no_of_seats=4,
            cylinder=4,
            fuel_type=1,
            safety_rating=5,
            type_number='VTN123',
            first_registration_year=2020
        )
        self.create_url = reverse('vehicle-type-number-list')
        self.detail_url = reverse('vehicle-type-number-detail', kwargs={'uuid': self.vehicle_type_number.uuid})

    def test_create_vehicle_type_number(self):
        data = {
            'brand': str(self.brand.uuid),
            'model': str(self.model.uuid),
            'chasis_number': '67890',
            'no_of_seats': 5,
            'cylinder': 6,
            'fuel_type': 2,
            'safety_rating': 4,
            'type_number': 'VTN456',
            'first_registration_year': 2021
        }
        response = self.client.post(self.create_url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("results")['type_number'], 'VTN456')

    def test_retrieve_vehicle_type_number(self):
        response = self.client.get(self.detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['type_number'], 'VTN123')

    def test_update_vehicle_type_number(self):
        data = {
            'brand': str(self.brand.uuid),
            'model': str(self.model.uuid),
            'chasis_number': '67890',
            'no_of_seats': 6,
            'cylinder': 8,
            'fuel_type': 3,
            'safety_rating': 3,
            'type_number': 'VTN789',
            'first_registration_year': 2019
        }
        response = self.client.put(self.detail_url, json.dumps(data), content_type='application/json')
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(data.get("results")['type_number'], 'VTN789')
        self.assertEqual(data.get("results")['no_of_seats'], 6)

    def test_delete_vehicle_type_number(self):
        response = self.client.delete(self.detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(VehicleTypeNumber.objects.filter(pk=self.vehicle_type_number.pk).exists())


class VehicleTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()
        self.do_login()
        self.package_data = {
            "user_type": 3,
            "package_type": 1, 
            "name": "Tour package",
            "description": "v5",
            "price": "100.00",
            "validity": 20, 
            "number_of_vehicle": 3,
            "number_of_image": 5,
            "is_active": True
        }
        self.custom_package_data = {
            "user": self.user,
            "package_type": 4,
            "name": "Custom tour package",
            "description": "demo",
            "validity": 20,
            "number_of_vehicle": 2,
            "number_of_image": 3,
            "price": 0
        }
        # self.user = User.objects.create(username='testuser', email='testuser@example.com', password='testpassword')
        self.package = Package.objects.create(**self.package_data)
        self.custom_package = CustomPackage.objects.create(**self.custom_package_data)
        self.subscription = Subscription.objects.create(user=self.user, package=self.package, package_category=1)
        self.custom_package_subscription = Subscription.objects.create(user=self.user, custom_package=self.custom_package, package_category=2)
        self.brand = Brand.objects.create(name='Test Brand')
        self.model = Model.objects.create(name='Test Model', brand=self.brand)
        self.vehicle_type_number = VehicleTypeNumber.objects.create(type_number='VTN123')
        self.interior_color = Colour.objects.create(name='Red')
        self.exterior_color = Colour.objects.create(name='Blue')
        self.body_type = BodyType.objects.create(name='Sedan')
        self.vehicle = Vehicle.objects.create(
            user=self.user,
            subscription=self.subscription,
            brand=self.brand,
            year_of_registration=2020,
            month_of_registration=6,
            model=self.model,
            is_from_mfk=True,
            last_mfk_inspection_year=2021,
            last_mfk_inspection_month=12,
            type_number=self.vehicle_type_number,
            is_type_number_manual=False,
            interior_color=self.interior_color,
            exterior_color=self.exterior_color,
            running_mileage=50000,
            body_type=self.body_type,
            transmission=1,
            vehicle_condition=1,
            chasis_number='CH123456789',
            price=15000.00,
            fuel_type=1,
            cubic_capacity=2000,
            doors=4,
            energy_efficiency='A',
            fuel_consumption=7.5,
            horsepower=150,
            cylinders=4,
            kerb_weight=1500,
            vehicle_total_weight=2000,
            gear_available=6,
            addition_information='Test Info',
            vehicle_rc=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            warranty_type=1,
            additional_guarantee_text='Test Guarantee',
            is_leasing=True,
            leasing_text='Leasing Text',
            is_sold=False,
            is_featured=False,
            is_verify=True,
            is_active=True,
            status=1,
            activation_date=None
        )
        self.vehicle.multimedia.add(MultimediaFeature.objects.create(name='Feature1'))
        self.vehicle.safety_and_assistance.add(SafetyAssistanceFeature.objects.create(name='Safety1'))
        self.vehicle.standard_features.add(StandardFeature.objects.create(name='Standard1'))
        self.vehicle.optional_features.add(OptionalFeature.objects.create(name='Optional1'))


        self.custom_package_vehicle = Vehicle.objects.create(
            user=self.user,
            subscription=self.custom_package_subscription,
            brand=self.brand,
            year_of_registration=2020,
            month_of_registration=6,
            model=self.model,
            is_from_mfk=True,
            last_mfk_inspection_year=2021,
            last_mfk_inspection_month=12,
            type_number=self.vehicle_type_number,
            is_type_number_manual=False,
            interior_color=self.interior_color,
            exterior_color=self.exterior_color,
            running_mileage=50000,
            body_type=self.body_type,
            transmission=1,
            vehicle_condition=1,
            chasis_number='CH123456789',
            price=15000.00,
            fuel_type=1,
            cubic_capacity=2000,
            doors=4,
            energy_efficiency='A',
            fuel_consumption=7.5,
            horsepower=150,
            cylinders=4,
            kerb_weight=1500,
            vehicle_total_weight=2000,
            gear_available=6,
            addition_information='Test Info',
            vehicle_rc=SimpleUploadedFile(name='test_image.jpg', content=b'', content_type='image/jpeg'),
            warranty_type=1,
            additional_guarantee_text='Test Guarantee',
            is_leasing=True,
            leasing_text='Leasing Text',
            is_sold=False,
            is_featured=False,
            is_verify=True,
            is_active=True,
            status=1,
            activation_date=None
        )
        self.custom_package_vehicle.multimedia.add(MultimediaFeature.objects.create(name='Feature1'))
        self.custom_package_vehicle.safety_and_assistance.add(SafetyAssistanceFeature.objects.create(name='Safety1'))
        self.custom_package_vehicle.standard_features.add(StandardFeature.objects.create(name='Standard1'))
        self.custom_package_vehicle.optional_features.add(OptionalFeature.objects.create(name='Optional1'))

        self.create_url = reverse('vehicle-list')
        self.detail_url = reverse('vehicle-detail', kwargs={'uuid': self.vehicle.uuid})

        self.custom_package_create_vehicle_url = reverse('vehicle-list')
        self.custom_package_vehicle_detail_url = reverse('vehicle-detail', kwargs={'uuid': self.vehicle.uuid})

        self.activate_url = reverse('vehicle-activate-vehicle')

        self.image = SimpleUploadedFile(name='test_image.jpg', content=b'vehicle image', content_type='image/jpeg')

        self.multimedia_feature = MultimediaFeature.objects.create(name='Feature1')
        self.safety_feature = SafetyAssistanceFeature.objects.create(name='Safety1')
        self.standard_feature = StandardFeature.objects.create(name='Standard1')
        self.optional_feature = OptionalFeature.objects.create(name='Optional1')


    def test_create_vehicle(self):
        with open('/home/gautam/Pictures/maxresdefault.jpg', 'rb') as image_file:
            vehicle_rc = SimpleUploadedFile(
                name='test_vehicle_rc.jpg', 
                content=image_file.read(), 
                content_type='image/jpeg'
            )
        data = {
            # 'user': self.user.uuid,
            'subscription': str(self.subscription.uuid),
            'brand': str(self.brand.uuid),
            'year_of_registration': 2021,
            'month_of_registration': 5,
            'model': str(self.model.uuid),
            'is_from_mfk': True,
            'last_mfk_inspection_year': 2022,
            'last_mfk_inspection_month': 11,
            'type_number': str(self.vehicle_type_number.uuid),
            'is_type_number_manual': False,
            'interior_color': str(self.interior_color.uuid),
            'exterior_color': str(self.exterior_color.uuid),
            'running_mileage': 60000,
            'body_type': str(self.body_type.uuid),
            'transmission': 2,
            'vehicle_condition': 2,
            'chasis_number': 'CH987654321',
            'price': 20000.00,
            'fuel_type': 2,
            'cubic_capacity': 2500,
            'doors': 5,
            'energy_efficiency': 'B',
            'fuel_consumption': 8.5,
            'horsepower': 200,
            'cylinders': 6,
            'kerb_weight': 1600,
            'vehicle_total_weight': 2200,
            'gear_available': 7,
            'addition_information': 'Additional Info',
            'warranty_type': 2,
            'additional_guarantee_text': 'Additional Guarantee',
            'is_leasing': True,
            'leasing_text': 'Leasing Text',
            'is_sold': False,
            'is_featured': False,
            'is_verify': True,
            'is_active': True,
            'status': 1,
            'multimedia': str([{"uuid": str(self.multimedia_feature.uuid)}]),
            'safety_and_assistance': str([{"uuid": str(self.safety_feature.uuid)}]),
            'standard_features': str([{"uuid": str(self.standard_feature.uuid)}]),
            'optional_features': str([{"uuid": str(self.optional_feature.uuid)}]),
            'images': self.image,
            'vehicle_rc': vehicle_rc,
        }
        response = self.client.post(self.create_url, data, format="multipart")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("results")['chasis_number'], 'CH987654321')

    def test_retrieve_vehicle(self):
        response = self.client.get(self.detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chasis_number'], 'CH123456789')

    def test_update_vehicle(self):
        with open('/home/gautam/Pictures/maxresdefault.jpg', 'rb') as image_file:
            vehicle_rc = SimpleUploadedFile(
                name='test_vehicle_rc.jpg', 
                content=image_file.read(), 
                content_type='image/jpeg'
            )
        data = {
            # 'user': self.user.id,
            'subscription': str(self.subscription.uuid),
            'brand': str(self.brand.uuid),
            'year_of_registration': 2019,
            'month_of_registration': 4,
            'model': str(self.model.uuid),
            'is_from_mfk': True,
            'last_mfk_inspection_year': 2020,
            'last_mfk_inspection_month': 10,
            'type_number': str(self.vehicle_type_number.uuid),
            'is_type_number_manual': False,
            'interior_color': str(self.interior_color.uuid),
            'exterior_color': str(self.exterior_color.uuid),
            'running_mileage': 70000,
            'body_type': str(self.body_type.uuid),
            'transmission': 2,
            'vehicle_condition': 2,
            'chasis_number': 'CH567890123',
            'price': 25000.00,
            'fuel_type': 3,
            'cubic_capacity': 3000,
            'doors': 6,
            'energy_efficiency': 'C',
            'fuel_consumption': 9.5,
            'horsepower': 250,
            'cylinders': 8,
            'kerb_weight': 1700,
            'vehicle_total_weight': 2300,
            'gear_available': 8,
            'addition_information': 'Updated Info',
            'warranty_type': 3,
            'additional_guarantee_text': 'Updated Guarantee',
            'is_leasing': True,
            'leasing_text': 'Updated Leasing Text',
            'is_sold': False,
            'is_featured': False,
            'is_verify': True,
            'is_active': True,
            'status': 1,
            'multimedia': str([]),
            'safety_and_assistance': str([]),
            'standard_features': str([]),
            'optional_features': str([]),
            'images': self.image,
            'vehicle_rc': vehicle_rc,
        }
        response = self.client.put(self.detail_url, data, format="multipart")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]['chasis_number'], 'CH567890123')


    def test_partial_update_vehicle(self):
        data = {
            'running_mileage': 80000,
            'brand': str(self.brand.uuid)
        }
        response = self.client.patch(self.detail_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]['running_mileage'], '80000.00')

    def test_delete_vehicle(self):
        response = self.client.delete(self.detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle.pk).exists())


    def test_custom_package_create_vehicle(self):
        with open('/home/gautam/Pictures/maxresdefault.jpg', 'rb') as image_file:
            vehicle_rc = SimpleUploadedFile(
                name='test_vehicle_rc.jpg', 
                content=image_file.read(), 
                content_type='image/jpeg'
            )
        data = {
            # 'user': self.user.uuid,
            'subscription': str(self.custom_package_subscription.uuid),
            'brand': str(self.brand.uuid),
            'year_of_registration': 2021,
            'month_of_registration': 5,
            'model': str(self.model.uuid),
            'is_from_mfk': True,
            'last_mfk_inspection_year': 2022,
            'last_mfk_inspection_month': 11,
            'type_number': str(self.vehicle_type_number.uuid),
            'is_type_number_manual': False,
            'interior_color': str(self.interior_color.uuid),
            'exterior_color': str(self.exterior_color.uuid),
            'running_mileage': 60000,
            'body_type': str(self.body_type.uuid),
            'transmission': 2,
            'vehicle_condition': 2,
            'chasis_number': 'CH987654321',
            'price': 20000.00,
            'fuel_type': 2,
            'cubic_capacity': 2500,
            'doors': 5,
            'energy_efficiency': 'B',
            'fuel_consumption': 8.5,
            'horsepower': 200,
            'cylinders': 6,
            'kerb_weight': 1600,
            'vehicle_total_weight': 2200,
            'gear_available': 7,
            'addition_information': 'Additional Info',
            'warranty_type': 2,
            'additional_guarantee_text': 'Additional Guarantee',
            'is_leasing': True,
            'leasing_text': 'Leasing Text',
            'is_sold': False,
            'is_featured': False,
            'is_verify': True,
            'is_active': True,
            'status': 1,
            'multimedia': str([{"uuid": str(self.multimedia_feature.uuid)}]),
            'safety_and_assistance': str([{"uuid": str(self.safety_feature.uuid)}]),
            'standard_features': str([{"uuid": str(self.standard_feature.uuid)}]),
            'optional_features': str([{"uuid": str(self.optional_feature.uuid)}]),
            'images': self.image,
            'vehicle_rc': vehicle_rc,
        }
        response = self.client.post(self.custom_package_create_vehicle_url, data, format="multipart")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_201_CREATED)
        self.assertEqual(data.get("results")['chasis_number'], 'CH987654321')

    def test_custom_package_retrieve_vehicle(self):
        response = self.client.get(self.custom_package_vehicle_detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data['chasis_number'], 'CH123456789')

    def test_custom_package_update_vehicle(self):
        with open('/home/gautam/Pictures/maxresdefault.jpg', 'rb') as image_file:
            vehicle_rc = SimpleUploadedFile(
                name='test_vehicle_rc.jpg', 
                content=image_file.read(), 
                content_type='image/jpeg'
            )
        data = {
            # 'user': self.user.id,
            'subscription': str(self.custom_package_subscription.uuid),
            'brand': str(self.brand.uuid),
            'year_of_registration': 2019,
            'month_of_registration': 4,
            'model': str(self.model.uuid),
            'is_from_mfk': True,
            'last_mfk_inspection_year': 2020,
            'last_mfk_inspection_month': 10,
            'type_number': str(self.vehicle_type_number.uuid),
            'is_type_number_manual': False,
            'interior_color': str(self.interior_color.uuid),
            'exterior_color': str(self.exterior_color.uuid),
            'running_mileage': 70000,
            'body_type': str(self.body_type.uuid),
            'transmission': 2,
            'vehicle_condition': 2,
            'chasis_number': 'CH567890123',
            'price': 25000.00,
            'fuel_type': 3,
            'cubic_capacity': 3000,
            'doors': 6,
            'energy_efficiency': 'C',
            'fuel_consumption': 9.5,
            'horsepower': 250,
            'cylinders': 8,
            'kerb_weight': 1700,
            'vehicle_total_weight': 2300,
            'gear_available': 8,
            'addition_information': 'Updated Info',
            'warranty_type': 3,
            'additional_guarantee_text': 'Updated Guarantee',
            'is_leasing': True,
            'leasing_text': 'Updated Leasing Text',
            'is_sold': False,
            'is_featured': False,
            'is_verify': True,
            'is_active': True,
            'status': 1,
            'multimedia': str([]),
            'safety_and_assistance': str([]),
            'standard_features': str([]),
            'optional_features': str([]),
            'images': self.image,
            'vehicle_rc': vehicle_rc,
        }
        response = self.client.put(self.custom_package_vehicle_detail_url, data, format="multipart")
        data = json.loads(response.content)
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]['chasis_number'], 'CH567890123')


    def test_custom_package_partial_update_vehicle(self):
        data = {
            'running_mileage': 80000,
            'brand': str(self.brand.uuid)
        }
        response = self.client.patch(self.custom_package_vehicle_detail_url, data, format="multipart")
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertEqual(response.data["data"]['running_mileage'], '80000.00')

    def test_custom_package_delete_vehicle(self):
        response = self.client.delete(self.custom_package_vehicle_detail_url, content_type='application/json')
        self.assertEqual(response.status_code, status.HTTP_200_OK)
        self.assertFalse(Vehicle.objects.filter(pk=self.vehicle.pk).exists())

    def test_activate_vehicle_without_payment(self):
        activation_data = {
            "subscription_uuid": str(self.subscription.uuid),
            "vehicle_uuid": str(self.vehicle.uuid),
            "status": 1,
        }
        response = self.client.post(self.activate_url, activation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_402_PAYMENT_REQUIRED)

    def test_activate_vehicle_without_payment_custom_package(self):
        activation_data = {
            "subscription_uuid": str(self.custom_package_subscription.uuid),
            "vehicle_uuid": str(self.vehicle.uuid),
            "status": 1,
        }
        response = self.client.post(self.activate_url, activation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_402_PAYMENT_REQUIRED)

    def test_reject_vehicle_without_payment(self):
        activation_data = {
            "subscription_uuid": str(self.subscription.uuid),
            "vehicle_uuid": str(self.vehicle.uuid),
            "status": 0,
        }
        response = self.client.post(self.activate_url, activation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_402_PAYMENT_REQUIRED)

    def test_reject_vehicle_without_payment_custom_package(self):
        activation_data = {
            "subscription_uuid": str(self.custom_package_subscription.uuid),
            "vehicle_uuid": str(self.vehicle.uuid),
            "status": 0,
        }
        response = self.client.post(self.activate_url, activation_data, format='json')
        self.assertEqual(response.status_code, status.HTTP_402_PAYMENT_REQUIRED)    

    def test_activate_vehicle_with_payment(self):
        self.subscription.is_paid = True
        self.subscription.is_activated = True
        self.subscription.activation_date = datetime.now()
        self.subscription.save()

        activation_data = {
            "subscription_uuid": str(self.subscription.uuid),
            "vehicle_uuid": str(self.vehicle.uuid),
            "status": 1,
        }
        # response = self.client.post(self.activate_url, activation_data, format='json')
        # self.assertEqual(response.status_code, status.HTTP_200_OK)

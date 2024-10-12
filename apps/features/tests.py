from django.urls import reverse
from .models import MultimediaFeature, StandardFeature, SafetyAssistanceFeature, OptionalFeature
from tests.base import BaseTestCase


class MultimediaFeatureTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Multimedia record
        self.data = {
            "name": "Bluetooth connectivity",
            "vehicle_type": 1
        }
    
    def test_create_multimedia_feature(self):
        url = reverse("multimediafeature-list")
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Bluetooth connectivity")
    
    def test_retrieve_multimedia_feature(self):
        # Create an instance first
        feature = MultimediaFeature.objects.create(name="Bluetooth connectivity", vehicle_type=1)
        
        url = reverse("multimediafeature-detail", args=[feature.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Bluetooth connectivity")
    
    def test_update_multimedia_feature(self):
        # Create an instance first
        feature = MultimediaFeature.objects.create(name="Bluetooth connectivity", vehicle_type=1)
        
        url = reverse("multimediafeature-detail", args=[feature.id])
        updated_data = {"name": "Updated feature", "vehicle_type": 1}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Updated feature")
    
    def test_delete_multimedia_feature(self):
        # Create an instance first
        feature = MultimediaFeature.objects.create(name="Bluetooth connectivity", vehicle_type=1)
        
        url = reverse("multimediafeature-detail", args=[feature.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(MultimediaFeature.objects.filter(id=feature.id).exists())


class StandardFeatureTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Standard feature record
        self.data = {
            "name": "Air Conditioning",
            "vehicle_type": 1
        }

    def test_create_standard_feature(self):
        url = reverse("standardfeature-list")
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Air Conditioning")
    
    def test_retrieve_standard_feature(self):
        # Create an instance first
        feature = StandardFeature.objects.create(name="Air Conditioning", vehicle_type=1)
        
        url = reverse("standardfeature-detail", args=[feature.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Air Conditioning")
    
    def test_update_standard_feature(self):
        # Create an instance first
        feature = StandardFeature.objects.create(name="Air Conditioning", vehicle_type=1)
        
        url = reverse("standardfeature-detail", args=[feature.id])
        updated_data = {"name": "Updated feature", "vehicle_type": 1}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Updated feature")
    
    def test_delete_standard_feature(self):
        # Create an instance first
        feature = StandardFeature.objects.create(name="Air Conditioning", vehicle_type=1)
        
        url = reverse("standardfeature-detail", args=[feature.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(StandardFeature.objects.filter(id=feature.id).exists())


class SafetyAssistanceFeatureTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Safety assistance feature record
        self.data = {
            "name": "ABS",
            "vehicle_type": 1
        }

    def test_create_safety_assistance_feature(self):
        url = reverse("safetyassistancefeature-list")
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "ABS")
    
    def test_retrieve_safety_assistance_feature(self):
        # Create an instance first
        feature = SafetyAssistanceFeature.objects.create(name="ABS", vehicle_type=1)
        
        url = reverse("safetyassistancefeature-detail", args=[feature.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "ABS")
    
    def test_update_safety_assistance_feature(self):
        # Create an instance first
        feature = SafetyAssistanceFeature.objects.create(name="ABS", vehicle_type=1)
        
        url = reverse("safetyassistancefeature-detail", args=[feature.id])
        updated_data = {"name": "Updated feature", "vehicle_type": 1}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Updated feature")
    
    def test_delete_safety_assistance_feature(self):
        # Create an instance first
        feature = SafetyAssistanceFeature.objects.create(name="ABS", vehicle_type=1)
        
        url = reverse("safetyassistancefeature-detail", args=[feature.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(SafetyAssistanceFeature.objects.filter(id=feature.id).exists())


class OptionalFeatureTestCase(BaseTestCase):
    def setUp(self):
        super().setUp()

        # Optional feature record
        self.data = {
            "name": "Sunroof",
            "vehicle_type": 1
        }

    def test_create_optional_feature(self):
        url = reverse("optionalfeature-list")
        response = self.client.post(url, self.data, format='json')
        self.assertEqual(response.status_code, 201)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Sunroof")
    
    def test_retrieve_optional_feature(self):
        # Create an instance first
        feature = OptionalFeature.objects.create(name="Sunroof", vehicle_type=1)
        
        url = reverse("optionalfeature-detail", args=[feature.id])
        response = self.client.get(url, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Sunroof")
    
    def test_update_optional_feature(self):
        # Create an instance first
        feature = OptionalFeature.objects.create(name="Sunroof", vehicle_type=1)
        
        url = reverse("optionalfeature-detail", args=[feature.id])
        updated_data = {"name": "Updated feature", "vehicle_type": 1}
        response = self.client.put(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Updated feature")
    
    def test_partial_update_optional_feature(self):
        # Create an instance first
        feature = OptionalFeature.objects.create(name="Sunroof", vehicle_type=1)
        
        url = reverse("optionalfeature-detail", args=[feature.id])
        updated_data = {"name": "Updated feature"}
        response = self.client.patch(url, updated_data, format='json')
        self.assertEqual(response.status_code, 200)
        self.assertIn('name', response.data)
        self.assertEqual(response.data['name'], "Updated feature")

    def test_delete_optional_feature(self):
        # Create an instance first
        feature = OptionalFeature.objects.create(name="Sunroof", vehicle_type=1)
        
        url = reverse("optionalfeature-detail", args=[feature.id])
        response = self.client.delete(url, format='json')
        self.assertEqual(response.status_code, 204)
        self.assertFalse(OptionalFeature.objects.filter(id=feature.id).exists())

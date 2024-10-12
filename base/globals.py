from django.utils.translation import gettext_lazy as _


class UserConstants:
    ADMIN, PRIVATE, DEALER = (1, 2, 3)

    @classmethod
    def get_user_type_choices(cls):
        choices = (
            (cls.ADMIN, _("Admin")),
            (cls.PRIVATE, _("Private")),
            (cls.DEALER, _("Dealer")),
        )
        return choices


class VehicleConstants:
    CAR, BIKE, GARAGE, COMPONENT = (1, 2, 3, 4)
    AUTOMATIC, MANUAL = (1, 2)
    RARE_WHEEL_DRIVE, FRONT_WHEEL_DRIVE, ALL_WHEEL_DRIVE = (1, 2, 3)
    GASOLINE, DIESEL, ELECTRIC, HYBRID = (1, 2, 3, 4)
    NEW, USED, DEMO, CLASSIC, ACCIDENT = (1, 2, 3, 4, 5)
    MR, MRS = (1, 2)
    ACCEPTED, REJECTED, PENDING = (1, 0, 2)
    FROM_DATE, FROM_REGISTRATION_DATE, FROM_TAKEOVER, NO_GUARANTEE = 1, 2, 3, 4
    RENT, SALE = (1, 2)

    @classmethod
    def get_vehicle_listing_type_choices(cls):
        choices = (
            (cls.RENT, _("Rent")),
            (cls.SALE, _("Sale"))
        )
        return choices

    @classmethod
    def get_warranty_type(cls):
        choices = (
            (cls.FROM_DATE, _("From date")),
            (cls.FROM_REGISTRATION_DATE, _("From registration date")),
            (cls.FROM_TAKEOVER, _("From takeover")),
            (cls.NO_GUARANTEE, _("From guarantee")),
        )
        return choices

    @classmethod
    def get_vehicle_type_choices(cls):
        choices = (
            (cls.CAR, _("Car")),
            (cls.BIKE, _("Bike")),
            (cls.GARAGE, _("Garage")),
            (cls.COMPONENT, _("Component"))
        )
        return choices

    @classmethod
    def get_transmission_choices(cls):
        choices = (
            (cls.AUTOMATIC, _("Automatic")),
            (cls.MANUAL, _("Manual")),
        )
        return choices

    @classmethod
    def get_drive_choices(cls):
        choices = (
            (cls.RARE_WHEEL_DRIVE, _("Rare Wheel Drive")),
            (cls.FRONT_WHEEL_DRIVE, _("Front Wheel Drive")),
            (cls.ALL_WHEEL_DRIVE, _("All Wheel Drive")),
        )
        return choices

    @classmethod
    def get_fuel_type_choices(cls):
        choices = (
            (cls.GASOLINE, _("Gasoline")),
            (cls.DIESEL, _("Diesel")),
            (cls.ELECTRIC, _("Electric")),
            (cls.HYBRID, _("Hybrid")),
        )
        return choices

    @classmethod
    def get_condition_choices(cls):
        choices = (
            (cls.NEW, _("New")),
            (cls.USED, _("Used")),
            (cls.DEMO, _("Demo")),
            (cls.CLASSIC, _("Classic")),
            (cls.ACCIDENT, _("Accident")),
        )
        return choices

    @classmethod
    def get_title_choices(cls):
        choices = (
            (cls.MR, _("Mr")),
            (cls.MRS, _("Mrs")),
        )
        return choices
    
    @classmethod
    def get_vehicle_status_choices(cls):
        choices = (
            (cls.ACCEPTED, _("Accepted")),
            (cls.REJECTED, _("Rejected")),
            (cls.PENDING, _("Pending"))
        )
        return choices

class PackageConstants:
    SELL, RENT = (1, 2)
    CAR, BIKE, LOCAL, VIP, RENT_A_CAR, RENT_A_BIKE, RENT_A_GARAGE, COMPONENT, PROMOTION_RENT_A_CAR, PROMOTION_RENT_A_BIKE, PROMOTION_RENT_A_GARAGE = (1, 2, 3, 4, 5, 6, 7, 8, 9, 10, 11)
    ACCEPTED, REJECTED, PENDING = (1, 0, 2)
    DEFAULT, CUSTOM = 1, 2

    @classmethod
    def get_package_type_choices(cls):
        choices = (
            (cls.CAR, _("Car")),
            (cls.BIKE, _("Bike")),
            (cls.LOCAL, _("Local")),
            (cls.VIP, _("VIP")),
            (cls.RENT_A_CAR, _("Rent a car")),
            (cls.RENT_A_BIKE, _("Rent a bike")),
            (cls.RENT_A_GARAGE, _("Rent a garage")),
            (cls.COMPONENT, _("Component")),
            (cls.PROMOTION_RENT_A_CAR, _("Promotion-Rent a car")),
            (cls.PROMOTION_RENT_A_BIKE, _("Promotion-Rent a bike")),
            (cls.PROMOTION_RENT_A_GARAGE, _("Promotion-Rent a garage")),
        )
        return choices
    
    @classmethod
    def get_package_for_choices(cls):
        return (
            (cls.SELL, _("Sell")),
            (cls.RENT, _("Rent")),
        )
    
    @classmethod
    def get_package_status_choices(cls):
        choices = (
            (cls.ACCEPTED, _("Accepted")),
            (cls.REJECTED, _("Rejected")),
            (cls.PENDING, _("Pending"))
        )
        return choices
    
    @classmethod
    def get_package_category_choices(cls):
        choices = (
            (cls.DEFAULT, _("Default")),
            (cls.CUSTOM, _("Custom"))
        )
        return choices


class PaymentConstants:
    PENDING, PAID, FAILED = ("pending", "paid", "failed")

    @classmethod
    def get_transaction_status(cls):
        choices = (
            (cls.PENDING, _("pending")),
            (cls.PAID, _("paid")),
            (cls.FAILED, _("failed"))
        )
    

class AdvertisementConstants:
    ACCEPTED, REJECTED, PENDING = (1, 0, 2)
    
    @classmethod
    def get_advertisement_status_choices(cls):
        choices = (
            (cls.ACCEPTED, _("Accepted")),
            (cls.REJECTED, _("Rejected")),
            (cls.PENDING, _("Pending"))
        )
        return choices

class RentacarConstants:
    ELECTRICITY,PLUGIN_HYBRID, HYBRID, GASOLINE, DIESEL = (1, 2, 3, 4, 5)
    MANUAL, AUTOMATIC = (1, 2)
    AIR_CONDITIONING, HEADTED_SEATS = (1, 2)
    NEW, USED = (1, 2)
    A, B, C, D, E, F, G = (1, 2, 3, 4, 5, 6, 7)
    SUV, HEAVY_DUTY, BDOUBLE, BMX, BOBCAT, BULLD = (1,2,3,4,5,6)
    JAN, FEB, MAR, APR, MAY, JUN, JUL, AUG, SEP, OCT, NOV, DEC = (1,2,3,4,5,6,7,8,9,10,11,12)
    ALL_SEASON, WINTER = (1,2)
    @classmethod
    def get_fuel_type_choices(cls):
        choices = (
            (cls.ELECTRICITY, _("Electricity")),
            (cls.PLUGIN_HYBRID, _("Plugin hybrid")),
            (cls.HYBRID, _("Hybrid")),
            (cls.GASOLINE, _("Gasoline")),
            (cls.DIESEL, _("Diesel"))
        )
        return choices
    
    @classmethod
    def get_transmission_choices(cls):
        choices = (
            (cls.MANUAL, _("Manual")),
            (cls.AUTOMATIC, _("Automatic"))
        )
        return choices
    
    @classmethod
    def get_comfort_choices(cls):
        choices = (
            (cls.AIR_CONDITIONING, _("Air conditioning")),
            (cls.HEADTED_SEATS, _("Heated seats"))
        )
        return choices

    @classmethod
    def get_condition_choices(cls):
        choices = (
            (cls.NEW, _("New")),
            (cls.USED, _("Used"))
        )
        return choices
    
    @classmethod
    def get_energy_efficiency_choices(cls):
        choices = (
            (cls.A, _("A")),
            (cls.B, _("B")),
            (cls.C, _("C")),
            (cls.D, _("D")),
            (cls.E, _("E")),
            (cls.F, _("F")),
            (cls.G, _("G"))
        )
        return choices
    
    @classmethod
    def get_body_type_choices(cls):
        choices = (
            (cls.SUV, _("SUV")),
            (cls.HEAVY_DUTY, _("Heavy Duty")),
            (cls.BDOUBLE, _("BDOUBLE")),
            (cls.BMX, _("BMX")),
            (cls.BOBCAT, _("BOBCAT")),
            (cls.BULLD, _("BULLD"))
        )
        return choices
    @classmethod
    def get_month_choices(cls):
        choices = (
            (cls.JAN, _("January")),
            (cls.FEB, _("February")),
            (cls.MAR, _("March")),
            (cls.APR, _("April")),
            (cls.MAY, _("May")),
            (cls.JUN, _("Jun")),
            (cls.JUL, _("July")),
            (cls.AUG, _("August")),
            (cls.SEP, _("September")),
            (cls.OCT, _("October")),
            (cls.NOV, _("November")),
            (cls.DEC, _("December")),
        )
        return choices
    @classmethod
    def get_tyre_choices(cls):
        choices = (
            (cls.ALL_SEASON, _("All season tires")),
            (cls.WINTER, _("Winter times"))
        )
        return choices

class RentagarageConstants:
    single_garage, underground_parking, double_garage, open_slot, covered_slot = (1, 2, 3, 4, 5)
    
    @classmethod
    def get_garage_type_choices(cls):
        choices = (
            (cls.single_garage, _("Single garage")),
            (cls.underground_parking, _("Underground parking")),
            (cls.double_garage, _("Double garage")),
            (cls.open_slot, _("Open slot")),
            (cls.covered_slot, _("Covered slot"))
        )
        return choices

class UserReviewConstants:
    vehicle_sell, vehicle_rent,bike_sell, bike_rent, garage_rent,components_sell  = (1, 2, 3, 4, 5,6)
    
    @classmethod
    def get_review_category_choices(cls):
        choices = (
            (cls.vehicle_sell, _("Vehicle Sell")),
            (cls.vehicle_rent, _("Vehicle Rent")),
            (cls.bike_sell, _("Bike Sell")),
            (cls.bike_rent, _("Bike Rent")),
            (cls.garage_rent, _("Garage Rent")),
            (cls.components_sell, _("Components Sell")),
        )
        return choices


class ComponentConstants:
    CAR, BIKE = (1, 2)
    NEW, USED = (1, 2)
    HOME_DELIVERY, TAKE_AWAY = (1, 2)
    FROM_DATE, FROM_REGISTRATION_DATE, FROM_TAKEOVER, NO_GUARANTEE = (1, 2, 3, 4)
    PENDING, REJECTED, APPROVED = (2, 0, 1)

    @classmethod
    def get_component_condition_choices(cls):
        choices = (
            (cls.NEW, _("New")),
            (cls.USED, _("Used"))
        )
        return choices

    @classmethod
    def get_delivery_choices(cls):
        choices = (
            (cls.HOME_DELIVERY, _("Home Delivery")),
            (cls.TAKE_AWAY, _("Take Away"))
        )
        return choices

    @classmethod
    def get_vehicle_type_choices(cls):
        choices = (
            (cls.CAR, _("Car")),
            (cls.BIKE, _("Bike"))
        )
        return choices

    @classmethod
    def get_warranty_type(cls):
        choices = (
            (cls.FROM_DATE, _("From date")),
            (cls.FROM_REGISTRATION_DATE, _("From registration date")),
            (cls.FROM_TAKEOVER, _("From takeover")),
            (cls.NO_GUARANTEE, _("From guarantee")),
        )
        return choices
    
    @classmethod
    def get_component_status_choices(cls):
        choices = (
            (cls.PENDING, _("Pending")),
            (cls.REJECTED, _("Rejected")),
            (cls.APPROVED, _("Approved"))
        )
        return choices        

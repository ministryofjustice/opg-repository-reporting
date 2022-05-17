from . import services as service_module
import inspect


class ServiceClasses:
    """Static class to find and return instances to handle aws services"""
    __found = None
    __classes = None

    @staticmethod
    def classes() -> list:
        """Return all classes from the service_module"""
        if ServiceClasses.__classes is None:
            ServiceClasses.__classes = inspect.getmembers(service_module, inspect.isclass)
        return ServiceClasses.__classes


    @staticmethod
    def supported() -> dict:
        """Generate the list of classes"""
        if ServiceClasses.__found is None:
            ServiceClasses.__found = {}
            for name, obj in list(ServiceClasses.classes()):
                ServiceClasses.__found.setdefault(name, obj)

        return ServiceClasses.__found

    @staticmethod
    def get(service_name:str) -> service_module.ServiceBase|None:
        """
        Use inspection to find the class matching the service name. 
        If found, return an instance of the class, otherwise return None
        """
        class_name = 'Service' + service_name.replace('-', ' ').title().replace(' ', '')
        service_names = ServiceClasses.supported()
        if class_name in service_names.keys():
            return service_names.get(class_name)()

        return None

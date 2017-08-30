import inspect
import importlib

# from widgets import WidgetAPI

def find_widget(package, widget_name):
    try:
        module = importlib.import_module('{0}.{1}'.format(package, widget_name))
        for x in dir(module):
            if x in ['DataStore', 'Retriever']:
                obj = getattr(module, x)
            else:
                continue

            # if inspect.isclass(obj) and issubclass(obj, WidgetAPI) and obj is not WidgetAPI:
                # return obj
            if inspect.isclass(obj):
                # print(obj)
                return obj
    except ImportError:
        return None
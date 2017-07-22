import cmd, sys
import numpy as np
import threading
import os
from pluginbase import PluginBase
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
from functools import partial

class App(threading.Thread):
    def __init__(self):
        threading.Thread.__init__(self)
        self.start()

    def callback(self):
        self.root.quit()

    def run(self):
        import matplotlib.pyplot as plt
        import numpy as np

        t = np.arange(0.0, 2.0, 0.01)
        s = 1 + np.sin(2 * np.pi * t)
        plt.plot(t, s)

        plt.xlabel('time (s)')
        plt.ylabel('value (V)')
        plt.title('A financial chart')
        plt.grid(True)
        # plt.savefig("test.png")
        plt.show()


def threaded_function():
    import matplotlib.pyplot as test

    test.figure()
    t = np.arange(0.0, 2.0, 0.01)
    s = 1 + np.sin(2 * np.pi * t)
    test.plot(t, s)

    test.xlabel('time (s)')
    test.ylabel('value (V)')
    test.title('A financial chart')
    test.grid(True)
    # plt.savefig("test.png")
    # draw()

    test.show(block=False)


def threaded_function_test():
    # Plot circle or radius 3
    import matplotlib.pyplot as test2
    test2.figure()
    an = np.linspace(0, 2 * np.pi, 100)

    test2.subplot(221)
    test2.plot(3 * np.cos(an), 3 * np.sin(an))
    test2.title('not equal, looks like ellipse', fontsize=10)

    test2.subplot(222)
    test2.plot(3 * np.cos(an), 3 * np.sin(an))
    test2.axis('equal')
    test2.title('equal, looks like circle', fontsize=10)

    test2.subplot(223)
    test2.plot(3 * np.cos(an), 3 * np.sin(an))
    test2.axis('equal')
    test2.axis([-3, 3, -3, 3])
    test2.title('looks like circle, even after changing limits', fontsize=10)

    test2.subplot(224)
    test2.plot(3 * np.cos(an), 3 * np.sin(an))
    test2.axis('equal')
    test2.axis([-3, 3, -3, 3])
    test2.plot([0, 4], [0, 4])
    test2.title('still equal after adding line', fontsize=10)

    test2.show(block=False)


from datetime import date
from marshmallow import Schema, fields, pprint

class ArgumentsSchema(Schema):
    date_from = fields.DateTime(required=True, format='%Y-%m-%d') 
    date_to = fields.DateTime(required=True, format='%Y-%m-%d')
    dependent_variable = fields.Str(required=True)
    independent_variables = fields.List(fields.String())
    
class RequestSchema(Schema):
    function = fields.Str(required=True)
    arguments = fields.Nested(ArgumentsSchema())

def main():
    here = os.path.abspath(os.path.dirname(__file__))
    get_path = partial(os.path.join, here)

    plugin_base = PluginBase(package='plugins',
                             searchpath=[get_path('./plugins')])

    source = plugin_base.make_plugin_source(
        searchpath=[get_path('./tmp/skata')],
        identifier='skata')

    available_plugins = [plugin for plugin in source.list_plugins() if plugin != 'abstractplugin']
    # for plugin in available_plugins:
    #     object = source.load_plugin(plugin)
    #     obj = object.Plugin()
    #     print([i for i in dir(obj) if not i.startswith('__')])


    history = InMemoryHistory()

    try:
        while True:
            input_string = prompt("> ", history=history)

            if input_string in ['exit', 'quit']:
                raise KeyboardInterrupt

            tokens = input_string.split(" ")
            filename = input_string.replace(" ", "_")
            plugin_name = tokens.pop(0)

            # here I need to do a bunch of validations on input string.
            # maybe each class needs to declare its own validation

            if plugin_name in available_plugins:
                object = source.load_plugin(plugin_name)
                obj = object.Plugin(filename, tokens)
                print(obj.run())
    except KeyboardInterrupt:
        print('GoodBye!')

if __name__ == '__main__':
    main()

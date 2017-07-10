import cmd, sys
import numpy as np
import threading
from pluginbase import PluginBase
from prompt_toolkit import prompt
from prompt_toolkit.history import InMemoryHistory
import os
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


def main():
    here = os.path.abspath(os.path.dirname(__file__))
    get_path = partial(os.path.join, here)

    plugin_base = PluginBase(package='plugins',
                             searchpath=[get_path('./plugins')])

    source = plugin_base.make_plugin_source(
        searchpath=[get_path('./tmp/skata')],
        identifier='skata')

    available_plugins = [plugin for plugin in source.list_plugins() 
                         if plugin != 'abstractplugin']
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
            plugin_name = tokens.pop(0)

            # here I need to do a bunch of validations on input string.
            # maybe each class needs to declare its own validation

            if plugin_name in available_plugins:
                object = source.load_plugin(plugin_name)
                obj = object.Plugin(tokens)
                print(obj.run())
    except KeyboardInterrupt:
        print('GoodBye!')

if __name__ == '__main__':
    main()

# class Shell(cmd.Cmd):
#     # For easier usage calculate the path relative to here.
#     here = os.path.abspath(os.path.dirname(__file__))
#     get_path = partial(os.path.join, here)
#
#     plugin_base = PluginBase(package='plugins',
#                              searchpath=[get_path('./plugins')])
#
#     source = plugin_base.make_plugin_source(
#         searchpath=[get_path('./tmp/skata')],
#         identifier='skata')
#
#     available_plugins = [plugin for plugin in source.list_plugins() if plugin != 'abstractplugin']
#     for plugin in available_plugins:
#         object = source.load_plugin(plugin)
#         obj = object.Plugin()
#         print([i for i in dir(obj) if not i.startswith('__')])
#
#
#     intro = 'Finance shell. Type help or ? to list commands.\n'
#     prompt = '(warren) '
#     file = None
#
#     # ----- basic turtle commands -----
#     def do_arima(self, arg):
#         'Execute arima model on time series'
#         pass
#
#     def do_finperf(self, arg):
#         'Execute financial performance of symbol'
#         pass
#
#     def do_undocumented_command_a(self, arg):
#         # thread.start_new_thread(threaded_function, ('test',) )
#         # th = threading.Thread(target=threaded_function)
#         # th.setDaemon(1)
#         # th.start()
#         threaded_function()
#
#     def do_undocumented_command_b(self, arg):
#         # thread.start_new_thread(threaded_function, ('test',) )
#         # th = threading.Thread(target=threaded_function)
#         # th.setDaemon(1)
#         # th.start()
#         threaded_function_test()
#
#     def do_bye(self, arg):
#         'Stop recording, close the turtle window, and exit:  BYE'
#         print('Thank you for using lehmanbrothers')
#         self.close()
#         # bye()
#         return True
#
#     def do_exit(self, arg):
#         'Stop recording, close the turtle window, and exit:  EXIT'
#         print('Thank you for using lehmanbrothers')
#         self.close()
#         # bye()
#         return True
#
#     def precmd(self, line):
#         line = line.lower().split(' ')
#         line = '_'.join(line)
#         if self.file and 'playback' not in line:
#             print(line, self.file)
#         return line
#
#     def close(self):
#         if self.file:
#             self.file.close()
#             self.file = None
#
#
# def parse(arg):
#     'Convert a series of zero or more numbers to an argument tuple'
#     return tuple(map(int, arg.split()))
#
#
# if __name__ == '__main__':
#     Shell().cmdloop()

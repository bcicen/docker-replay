import sys
from docker import Client, errors

class RunCommand(object):
    def __init__(self, container, image):
        self.image = image
        self.container = container

    @property
    def args(self):
        return (' ').join(self.container['Args'])

    @property
    def cmd(self):
        return self.container['Path']

    @property
    def entrypoint_opt(self):
        entrypoint = self.container['Config']['Entrypoint']
        if entrypoint:
            return '--entrypoint="%s"' % ' '.join(entrypoint)

    @property
    def name_opt(self):
        return '--name="%s"' % self.container['Name'].strip('/')

    @property
    def user_opt(self):
        if self.container['Config']['User']:
            return '--user="%s"' % self.container['Config']['User']

    @property
    def volume_opt(self):
        vopts = [] 
        for mount in self.container['Mounts']:
            opt = '--volume=%s:%s' % (mount['Source'], mount['Destination'])
            if mount['Mode']:
                opt += ':%s' % mount['Mode']
            vopts.append(opt)
        return ' '.join(vopts)

    def build_opts(self):
        opts = []
        all_opts = [ o for o in dir(self) if o.endswith('_opt') ]
        for opt in all_opts:
            if self.__getattribute__(opt):
                opts.append(self.__getattribute__(opt))
        return ' '.join(opts)

    def __str__(self):
        return 'docker run %s' % self.build_opts()

def main():
    q = sys.argv[1]
    client = Client()
    try:
        container = client.inspect_container(q)
        image = client.inspect_image(container['Image'])
    except errors.NotFound:
        print('no such container: %s' % q)
        sys.exit(1)
    
    print(RunCommand(container, image))

if __name__ == '__main__':
    main()

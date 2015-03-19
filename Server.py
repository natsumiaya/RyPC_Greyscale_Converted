import cv2
import rpyc
from rpyc.utils.server import ThreadedServer


class MyService(rpyc.Service):
    def exposed_open(self,filePath, mode = 'wb'):
        return open(filePath,mode)
    def exposed_dothemagic(self, filename):
            if filename.endswith('.png') or filename.endswith('.jpg'):
                print "Receiving.."
                img = cv2.imread(filename)
                print "Converting..."
                img2 = cv2.cvtColor(img, cv2.COLOR_RGB2GRAY)
                cv2.imwrite(filename, img2)
                print "Sending..."
                f = open(filename, 'rb')
                contents = f.read()
                return contents


if __name__ == "__main__":
    server = ThreadedServer(MyService, port=18812, protocol_config={"allow_public_attrs": True})
    server.start()

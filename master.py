import logging, sys
logging.basicConfig(stream=sys.stderr, level=logging.DEBUG)

from masterDataControl import getMasterDataControl
masterDataControl = getMasterDataControl()

if __name__ == '__main__':
    logging.debug('Master Node RUKA')
    masterDataControl.start()

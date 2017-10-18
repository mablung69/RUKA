from masterDataControl import getMasterDataControl

masterDataControl = getMasterDataControl()

if __name__ == '__main__':
    print("Master Node RUKA")
    masterDataControl.start()

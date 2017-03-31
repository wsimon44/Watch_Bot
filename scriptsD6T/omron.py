import pigpio, time, smbus

class OmronD6T(object):
    def init(self, rasPiChannel = 1, omronAddress = 0x0a, omronSize = 16):
        self.MAX_RETRIES = 5
        self.roomTemp = 0 #Init temp
        self.rasPiChannel = rasPiChannel	#Numero de bus dans la raspberry
        self.omronAddress = omronAddress #Adresse du capteur dans la Rasp
        self.arraySize = omronSize #Taille des donnees du capteur
        self.BUFFER_LENGTH=(self.arraySize * 2) + 3       # Taille du buffer
        self.piGPIO = pigpio.pi()
        self.piGPIOver = self.piGPIO.get_pigpio_version()
        self.i2cBus = smbus.SMBus(1)
        time.sleep(0.1)

            # initialize the device based on Omron's appnote 1
        self.retries = 0
        self.result = 0
        for i in range(0,self.MAX_RETRIES):
            time.sleep(0.05)                               # Wait a short time
            self.handle = self.piGPIO.i2c_open(self.rasPiChannel, self.omronAddress) # open Omron D6T device at address 0x0a on bus 1
            print self.handle
            if self.handle > 0:
                self.result = self.i2cBus.write_byte(self.omronAddress,0x4c)
            break
        else:
            print ''
            print '***** Omron init error ***** handle='+str(self.handle)+' retries='+str(self.retries)
            self.retries += 1


	# function to read the omron temperature array
    def read(self):
        self.temperature_data_raw=[0]*self.BUFFER_LENGTH
        self.temperature=[0.0]*self.arraySize         # holds the recently measured temperature
        self.values=[0]*self.BUFFER_LENGTH

        # read the temperature data stream - if errors, retry
        retries = 0
        for i in range(0,self.MAX_RETRIES):
            time.sleep(0.05)                               # Wait a short time
            (self.bytes_read, self.temperature_data_raw) = self.piGPIO.i2c_read_device(self.handle, self.BUFFER_LENGTH)

            # Handle i2c error transmissions
            if self.bytes_read != self.BUFFER_LENGTH:
                print '***** Omron Byte Count error ***** - bytes read: '+str(self.bytes_read)
                self.retries += 1                # start counting the number of times to retry the transmission


            else:
                t = (self.temperature_data_raw[1] << 8) | self.temperature_data_raw[0]
                self.tPATc = float(t) / 10

                # Convert Raw Values to Temperature ('F)
                a = 0

                for i in range(2, len(self.temperature_data_raw) - 2, 2):
                    self.temperature[a] = float(
                        (self.temperature_data_raw[i + 1] << 8) | self.temperature_data_raw[i]) / 10
                    a += 1

                for i in range(0, self.bytes_read):
                    self.values[i] = self.temperature_data_raw[i]

        return self.temperature

import obd
from obd import OBDStatus
import csv
from datetime import datetime

#obd.logger.setLevel(obd.logging.DEBUG)

#functions
def connectOBD():
        connection = obd.OBD("socket://127.0.0.1:35000",baudrate=38400,fast=True)
        if connection.status() == OBDStatus.CAR_CONNECTED:
                return connection
        else:
                print('Error connecting... retrying')
                connectOBD()
                
def getSupportedCommands(connection):
        commands = []
        for command in connection.supported_commands:
                response = connection.query(command)
                if hasattr(response.value, "magnitude"):
                        commands.append(command)
                #if hasattr(response, "value"):
                        #commands.append(command.name)
                #print(command.name)
                #if response is None:
                        #print(response)
                #elif hasattr(response, "value"):
                        #print(response.value)
                #else:
                        #print(response)
        return commands

def sendCommand(connection, command):
        response = connection.query(command)
        if(response.value is not None):
                print(command.name, ': ',  response.value)
                return response
                
def saveLogs(command, result):
        if(result is not None and command is not None):
                with open('logs.csv', 'a', newline='') as csvfile:
                        startwriter = csv.writer(csvfile, delimiter=',')
                        startwriter.writerow([datetime.now(), command.name, result.value.magnitude, result.unit])

#start
def startup():
        connection = None
        while(connection is None):
                connection = connectOBD()
        
        supported_commands = getSupportedCommands(connection)

        while(connection is not None and connection.status() == OBDStatus.CAR_CONNECTED):
                for command in supported_commands:
                        result = sendCommand(connection, command)
                        saveLogs(command, result)
        else:
                startup()
                
startup()

#connection.close()

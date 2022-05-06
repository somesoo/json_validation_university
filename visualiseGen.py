# pattern
# #include "ParametersDict.h"
#
# QMap<quint8, QString> ParametersDict::_boardsDict = {
#         {0x01, "Ground Station"},
#         {0x02, "Pi Box"},
#         {0x03, "MPPT 1"}
# };
#
# QMap<quint16, QString> ParametersDict::_paramsDict = {
#         {0x0001, "Heartbeat"},
#         {0x0002, "MCU Temp"},
#         {0x0010, "MPPT Voltage 1"},
#         {0x0011, "MPPT Voltage 2"}
# };
QMAP_QUINT8_QSTRING_PARAMETERSDICT_BOARD = "QMap<quint8, QString> ParametersDict::_boardsDict = {\n  "
QMAP_QUINT16_QSTRING_PARAMETERSDICT_PARAMETERS = "QMap<quint16, QString> ParametersDict::_paramsDict = {\n  "
INCLUDE = "#include \"parametersDict.h\"\n\n"


class VGenerate:
    def __init__(self, name):
        self.name = name

    @staticmethod
    def id_range_loop(json_object, i, rng):
        max_id = int(json_object[rng][i]['MaxID'], 16)
        curr_id = int(json_object[rng][i]['MinID'], 16)
        addresses = []
        while max_id >= curr_id:
            addresses.append(hex(curr_id))
            curr_id = curr_id + 1
        x = 0
        dict_items = []
        for j in range(len(addresses)):
            x += 1
            body = "{" + f'{addresses[j]}, \"{json_object[rng][i]["Name"].replace("<x>", str(x))}\"' + "}"
            dict_items.append(body)
        return dict_items

    def write_to_file(self, json_object):
        with open(self.name, "w") as file:
            file.write(INCLUDE)
            file.write(QMAP_QUINT8_QSTRING_PARAMETERSDICT_BOARD)
            # dict loop
            size = len(json_object["Boards"])
            for i in range(size):
                if 'ID' not in json_object['Boards'][i]:
                    generator = self.id_range_loop(json_object, i, "Boards")
                    gen_size = len(generator)
                    for j in generator:
                        if j == gen_size-1 and i == size-1:
                            file.write(j + "\n  ")
                        else:
                            file.write(j + ",\n  ")
                else:
                    file.write("{" + json_object['Boards'][i]["ID"] + ", \"")
                    file.write(json_object["Boards"][i]['Name'] + "\"}")
                    if i != (size-1):
                        file.write(",\n  ")
                    else:
                        file.write("\n  ")
            file.write("};\n")
            file.write(QMAP_QUINT16_QSTRING_PARAMETERSDICT_PARAMETERS)
            # dict loop
            size = len(json_object["Parameters"])
            for i in range(size):
                if 'ID' not in json_object['Parameters'][i]:
                    generator = self.id_range_loop(
                        json_object, i, "Parameters")
                    gen_size = len(generator)
                    for j in range(len(generator)):
                        if j == gen_size-1 and i == size-1:
                            file.write(generator[j] + "\n  ")
                        else:
                            file.write(generator[j] + ",\n  ")
                else:
                    file.write("{" + json_object['Parameters'][i]["ID"] + ", \"")
                    file.write(json_object["Parameters"][i]['Name'] + '\"}')
                    if i != size-1:
                        file.write(",\n  ")
                    else:
                        file.write("\n  ")
            file.write("};\n")

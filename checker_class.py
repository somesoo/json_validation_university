import jsonschema


class Checker:
    json_object = {}
    json_schema = {}

    def __init__(self, python_json_ob, python_json_schema, json_file_arg):
        self.json_object = python_json_ob
        self.json_schema = python_json_schema
        self.json_path = json_file_arg

    @staticmethod
    def check_placeholder(m_json):
        for i in range(len(m_json['Parameters'])):
            if 'ID' not in m_json['Parameters'][i]:
                if str(m_json['Parameters'][i]['Name']).find("<x>") != -1:
                    continue
                else:
                    print("error, placeholder")

    @staticmethod
    def not_double_name(m_json):
        name_board = []
        name_parameters = []
        for i in range(len(m_json["Boards"])):
            name_board.append(m_json["Boards"][i]["Name"])
        for i in range(len(m_json["Parameters"])):
            name_parameters.append(m_json["Parameters"][i]["Name"])
        name_board.sort()
        name_parameters.sort()
        for i in range(len(name_board)):
            if i < len(name_board) - 1:
                if name_board[i] == name_board[i + 1]:
                    print("boards name error")
        for i in range(len(name_parameters)):
            if i < len(name_parameters) - 1:
                if name_parameters[i] == name_parameters[i + 1]:
                    print("parameters name error")

    # check weather MinID is smaller than MaxID
    @staticmethod
    def compare_min_and_max(first, last):
        if int(first, 16) >> int(last, 16):
            print("Wrong MinID and MaxID input")

    @staticmethod
    def compare_loop(my_json):
        for j in range(len(my_json)):
            if 'ID' not in my_json['Parameters'][j]:
                Checker.compare_min_and_max(my_json['Parameters'][j]['MinID'], my_json['Parameters'][j]["MaxID"])

    @staticmethod
    def id_range_loop(json_object, i, rng):
        max_id = int(json_object[rng][i]['MaxID'], 16)
        curr_id = int(json_object[rng][i]['MinID'], 16)
        addresses = []
        while max_id >= curr_id:
            addresses.append(hex(curr_id))
            curr_id = curr_id + 1
        for j in range(len(addresses)):
            yield addresses[j]

    @staticmethod
    def check_for_address_collision(self, json_object):
        table_of_addresses_boards = []
        table_of_addresses_parameters = []
        for i in range(len(json_object["Boards"])):
            if 'ID' not in json_object['Boards'][i]:
                generator = self.id_range_loop(json_object, i, "Boards")
                for j in generator:
                    table_of_addresses_boards.append(j)
            else:
                table_of_addresses_boards.append(hex(int(json_object["Boards"][i]['ID'], 16)))
        for i in range(len(json_object["Parameters"])):
            if 'ID' not in json_object['Parameters'][i]:
                generator = self.id_range_loop(json_object, i, "Parameters")
                for j in generator:
                    table_of_addresses_parameters.append(j)
            else:
                table_of_addresses_parameters.append(hex(int(json_object["Parameters"][i]['ID'], 16)))
        if len(table_of_addresses_boards) == len(set(table_of_addresses_boards)):
            if len(table_of_addresses_parameters) == len(set(table_of_addresses_parameters)):
                return 1
            else:
                return 0
        else:
            return 0

    # errors
    def validate(self, json_object, json_schema):
        try:
            jsonschema.validate(instance=json_object, schema=json_schema)
            return 1
        except jsonschema.exceptions.ValidationError as ex:
            print(ex.instance)
            lookup = str(ex.instance)
            if lookup[0] == '{':
                lookup = lookup[1:lookup.find(',')]
                lookup = lookup.replace('\'', '\"')
            with open(self.json_path) as myFile:
                for (num, line) in enumerate(myFile, 1):
                    if lookup in line:
                        print('found at line:', num)
            return 0

    def run_checks(self, ob):
        if Checker.validate(self, self.json_object, self.json_schema):
            Checker.check_placeholder(ob)
            Checker.not_double_name(ob)
            Checker.compare_loop(ob)
            if Checker.check_for_address_collision(self, self.json_object):
                return 1
            else:
                return 0
        else:
            return 0

import re
import xml.etree.ElementTree as ET

tree = ET.parse('ConfigDumpInfo.xml')
root = tree.getroot()

dict_configs = {}

for neighbor in root.findall(".//*[@name]"):
    dict_configs[neighbor.attrib['id']] = neighbor.attrib['name']

PATTERN = '(?:,[\\n\\r]*|\\n|^)(\"(?:(?:\"\")*[^\"]*)*\"|[^\",\\n]*|(?:\\n|$))'

POINT_COUNT_CONFIGURATION = 2
SHIFT_CONFIGURATION_VERSION = 3
SHIFT_CONFIGURATION_PRODUCER = 4
SHIFT_CONFIGURATION_NAME = 5
SHIFT_CONFIGURATION_COUNT_OBJECT = 6
SHIFT_OBJECT_COUNT = 7
COUNT_ELEMENT_OBJECT = 4
CONFIGURATION_SUPPORT = 1
START_READ_POSITION = 3
SHIFT_SIZE = 2

dict_configuration = {}


def load_file():
    with open('ParentConfigurations.bin', 'rt', encoding='utf-8') as f:
        file_contents = f.read()
        data_strings = re.findall(PATTERN, file_contents)
        count_configuration = int(data_strings[POINT_COUNT_CONFIGURATION])

        start_point = START_READ_POSITION
        number_configuration = 1
        while number_configuration <= count_configuration:
            configuration_guid = data_strings[start_point]
            configuration_version = data_strings[start_point + SHIFT_CONFIGURATION_VERSION]
            configuration_producer = data_strings[start_point + SHIFT_CONFIGURATION_PRODUCER]
            configuration_name = data_strings[start_point + SHIFT_CONFIGURATION_NAME]
            count_objects_configuration = int(data_strings[start_point + SHIFT_CONFIGURATION_COUNT_OBJECT])
            configuration_support = int(data_strings[CONFIGURATION_SUPPORT])
            support_configuration = {"name": configuration_name, "provider": configuration_producer,
                                     "version": configuration_version, "support": configuration_support,
                                     "locked_list": [], "editable_list": [], "removed_list": []}
            dict_configuration[configuration_guid] = support_configuration

            start_object_point = start_point + SHIFT_OBJECT_COUNT
            number_object = 0
            while number_object < count_objects_configuration:
                currentObjectPoint = start_object_point + number_object * COUNT_ELEMENT_OBJECT;
                support = int(data_strings[currentObjectPoint])
                edit = int(data_strings[currentObjectPoint + 1])
                guid_object = data_strings[currentObjectPoint + SHIFT_SIZE]
                support_object = {"guid": guid_object, "support": support, "edit": edit, "name": ""}
                # 0 - не редактируется, 1 - с сохранением поддержки, 2 - снято
                if support == 0:
                    dict_configuration[configuration_guid]["locked_list"].append(support_object)
                elif support == 1:
                    dict_configuration[configuration_guid]["editable_list"].append(support_object)
                else:
                    support_object["name"] = dict_configs.get(guid_object, "")
                    dict_configuration[configuration_guid]["removed_list"].append(support_object)
                number_object += 1
            start_point = start_object_point + SHIFT_SIZE + count_objects_configuration * COUNT_ELEMENT_OBJECT

            number_configuration += 1


if __name__ == '__main__':
    load_file()

    for el in dict_configuration['2b62e156-bbc6-479f-a198-34dc5d797c6c']['removed_list']:
        print(el["name"])

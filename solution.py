import binascii, json


class Solution:
    """contains 4 answers"""

    def __load_data_file(self):
        with open(self.data_file_path, "r") as file:
            return file.readlines()

    def __load_protocol_json(self):
        with open(self.protocol_json_path, "r") as file:
            return json.load(file)

    def __init__(self, data_file_path: str, protocol_json_path: str):

        self.data_file_path = data_file_path
        self.protocol_json_path = protocol_json_path
        self.__expected_freq = {36: 164, 18: 84, 9: 48, 1: 1}
        self.__data = self.__load_data_file()
        self.__json_data = self.__load_protocol_json()

    def __hex_to_text(self, hex_data: str):
        hex_data = hex_data.replace(" ", "").replace("\t", "").strip()
        asci_message = binascii.unhexlify(hex_data)
        return "".join(chr(i) for i in asci_message)

    def get_version_name(self):

        first_line = self.__data[0].replace(" ", "")
        v_name = first_line.split(",")[-1]
        self.version = self.__hex_to_text(v_name)
        # used version
        return self.version

    def __get_protocols_frequencies(self, version: str):
        self.not_relevant_prots = set()
        self.prots_frequency = {
            k: 0 for k in self.__json_data["protocols_by_version"][version]["protocols"]
        }
        for line in self.__data:

            line = line.replace(" ", "").split(",")
            prot = str(int(line[2], 16))
            if self.prots_frequency.get(prot, None) is not None:
                self.prots_frequency[prot] = self.prots_frequency.get(prot, 0) + 1
            else:
                self.not_relevant_prots.add(prot)
                # Protocols that are not in the version
        return self.not_relevant_prots

    def compare_frequencies(self):

        self.__get_protocols_frequencies(self.version)
        self .not_used_protocols = set()
        self.wrong_freqs = []
        prots_fps = self.__json_data["protocols"]
        for k in self.prots_frequency.keys():
            if (
                self.__expected_freq[prots_fps[hex(int(k))]["fps"]]
                != self.prots_frequency[k]
            ):
               #wrong frequencies
                self.wrong_freqs.append(k)
            if self.prots_frequency[k] == 0 :
                 #Not used protocols
                self.not_used_protocols.add(hex(int(k)))

        return self.wrong_freqs.add(hex(int(k)))
    

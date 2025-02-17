import os


class GcodeModifier:
        def __init__(self, files_path, file_name, generated_file_name):
                self.files_path = files_path
                self.file_name = file_name
                self.generated_file_name = generated_file_name
                self.lines = self.get_file()

        def get_file(self):
                file_path = os.path.join(self.files_path, self.file_name)
                with open(file_path, "r+", encoding="utf-8") as file:
                        self.lines = file.readlines()
                return self.lines


        def insert_start_of_text(self, start_of_text, starting_line_pattern=";Machining time about", starting_gcode_pattern="G90"):
                insert_index = None
                for i, line in enumerate(self.lines):
                        if line.strip().startswith(starting_line_pattern):
                                insert_index = i + 1  
                                break
                if insert_index is not None:
                        for i in range(insert_index, len(self.lines)):
                                if self.lines[i].strip() == "G90":
                                        insert_index = i 
                                        break
                #if insert_index is not None:
                #        lines[:insert_index] + start_of_text + lines[insert_index:]

                self.lines[insert_index - 1 : insert_index - 1 + len(start_of_text)] = "".join(start_of_text)

                return self.lines


        def add_wait_times(self, raise_length=10, every_num=10):
                start_num = 0
                num_of_stops = 0
                for i, line in enumerate(self.lines):
                        if line.strip().startswith(";No. "):
                                start_num += 1
                        if (start_num != 0) and (start_num % every_num == 0):
                                if line.strip().startswith(("G00 Z2.0000 F480", "G00 Z1.0000 F480")):
                                        num_of_stops += 1
                                        self.lines[i : i + 1] = "".join([f"G0 Z{raise_length} F500 ; Auto generated {raise_length} raise\n",
                                                                    "M00 ; Auto generated Pause and wait\n"])

                print("Engrave steps: {}".format(start_num))
                print("Number of stops: {}".format(num_of_stops))

                return self.lines


        def write_files(self):
                file_path = os.path.join(self.files_path, self.generated_file_name)
                with open(file_path, "w") as file:
                        file.writelines(self.lines)
                                
                


if __name__ == "__main__":

        # Modify the raise in the 4th element of the list
        start_of_text = [
        "\nG92 X0 Y0 Z0 ; Set Current position to 0, all axes \n"
        "G00 Z5.0000 F500 ; Raise Z 5mm at 8.3mm/s to clear clamps and screws \n"
        "G28 Z ; Home in order, with Z touchplate \n"
        "G92 Z1.63 ; Account for probe thickness (set your thickness) \n"
        "G00 Z5.000 F500 ; Raise Z probe off of surface \n"
        "M00 ; Pause for LCD button press so you can remove the touchplate \n\n"
        ]

        files_path = None # Add your file path
        
        modifier = GcodeModifier(files_path=files_path, file_name="DU_test3.gcode", generated_file_name="DU_auto_generated_v2.gcode")
        modifier.insert_start_of_text(start_of_text)
        modifier.add_wait_times(raise_length=8, every_num=14)
        modifier.write_files()


import lin_class
import lin_gen_class
import lin_II_class



class class_tui_generator():
    def __init__(self) -> None:
        self.ini_template = [
            f"             _________       ", 
            f"        ____/         |_____ ", 
            f"       1___________________/ ", 
            f"          |               |  ", 
            "          |               |_ ", 
            "          |________________| ", 
            "    _____/                 | ", 
            "   |________________________|", 
            "| | | \|"
        ]



        pass # TODO: define tui segments

    def draw_from_class(self, clz: type):
        method_list = [func for func in dir(clz) if callable(getattr(clz, func)) and not func.startswith("__")]
        print(method_list)

    def print_segment(self, seg_short):
        for line in self.ini_template:
            print(line)


if __name__ == "__main__":
    ctg = class_tui_generator()
    # ctg.draw_from_class(lin_II_class.LinearClassifierTypeII)
    ctg.print_segment("d")

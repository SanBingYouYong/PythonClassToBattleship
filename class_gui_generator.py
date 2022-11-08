import cv2 as cv
from enum import Enum
import numpy as np



class Components(Enum):
    Head = "Ship Class Head Segment" # init function
    Arms = "Ship Turret Segments" # helper/sub methods/methods that does some job
    Bridge = "Ship Command Centres" # methods that combines sub methods together to do high level work
    Engine = "Ship Engine Segments" # methods involving major loops


class class_gui_generator():
    def __init__(self) -> None:
        self.img_head = cv.imread("./templates/base-head_noalpha.png")
        self.img_base = cv.imread("./templates/baseblock_noalpha.png")
        self.img_tail = cv.imread("./templates/base-tail_noalpha.png")
        self.img_bridge = cv.imread("./templates/bridge_noalpha.png")
        self.img_turret = cv.imread("./templates/turret_noalpha.png")
        self.img_engine = cv.imread("./templates/engine_noalpha.png")

        self.draw_outcome = None

    def manual_assign(self, methods: dict):
        # determine white background length using the sum of list lengths
        # height using the longest list length
        total_length = 0
        max_length = 0
        for (k, v) in methods.items():
            cl = len(v)
            total_length += cl
            if cl > max_length:
                max_length = cl
        shape = [100 * (3 + max_length), 100 * (total_length + 2), 3]
        background_whites = np.zeros(shape)
        background_whites.fill(255)
        canvas = background_whites.copy()
        # iterate and place image
        index_vertical_reversed = 100 * (2 + max_length)
        index_horizontal = 100
        for component in methods.keys():
            canvas[index_vertical_reversed - 100: index_vertical_reversed, index_horizontal: index_horizontal + 100, :] = self.img_base
            for name in methods[component]:
                index_vertical_reversed -= 25
                canvas[index_vertical_reversed - 100: index_vertical_reversed, index_horizontal: index_horizontal + 100, :] = self.img_turret
            # break
            cv.imshow("canvas", canvas)
            cv.waitKey(0)
            cv.destroyAllWindows()
            index_horizontal += 100
            index_vertical_reversed = 100 * (2 + max_length)
        cv.imshow("canvas", canvas)
        cv.waitKey(0)
        cv.destroyAllWindows()
    
    def manual_assign_manual_draw(self, methods: dict):
        # determine white background length using the sum of list lengths
        # height using the longest list length
        total_length = 0
        max_length = 0
        for (k, v) in methods.items():
            cl = len(v)
            total_length += cl
            if cl > max_length:
                max_length = cl
        shape = [100 * (3 + max_length), 100 * (total_length + 4), 3]
        background_whites = np.zeros(shape)
        background_whites.fill(255)
        canvas = background_whites.copy()
        ini_vertical_reversed = 100 * (2 + max_length)
        ini_horizontal = 100
        # Head: 
        canvas[ini_vertical_reversed - 100: ini_vertical_reversed, ini_horizontal: ini_horizontal + 100, :] = self.img_head
        canvas[ini_vertical_reversed - 100: ini_vertical_reversed, ini_horizontal + 100: ini_horizontal + 200, :] = self.img_base
        cv.putText(canvas, methods[Components.Head][0], [100, 100], cv.FONT_HERSHEY_COMPLEX, 1, (0, 0, 0))
        # Arms: Turrets without the last one pointing backward
        turret_verti_r = ini_vertical_reversed - 26
        turret_hori = ini_horizontal + 200
        turret_count = len(methods[Components.Arms]) # 3: 2 + 1
        turret_index = 1
        for name in methods[Components.Arms]:
            # TODO: fix indexing; turret is covering/overwriting bases for now
            canvas[turret_verti_r - 74: turret_verti_r + 26, turret_hori: turret_hori + 100, :] = self.img_base
            cv.putText(canvas, name, [turret_hori + 5, turret_verti_r + 100], cv.FONT_HERSHEY_COMPLEX, .3, (0, 0, 0))
            text_point = [turret_hori + 5, turret_verti_r + 75]
            for i in range(turret_index):
                canvas[ini_vertical_reversed - 125 - 25 * i: ini_vertical_reversed - 25 - 25 * max(0, i), turret_hori: turret_hori + 100, :] = self.img_base
                # uncomment following for index debugging: 
                # cv.imshow("canvas", canvas)
                # cv.waitKey(0)
                # cv.destroyAllWindows()
            canvas[turret_verti_r - 100 - 25 * max(0, (turret_index - 1)): turret_verti_r - 25 * max(0, (turret_index - 1)), turret_hori: turret_hori + 100, :] = self.img_turret
            cv.line(canvas, text_point, [text_point[0], text_point[1] - (turret_index + 2) * 25 + 5], (0, 0, 0))
            turret_hori += 100
            turret_index += 1
            if turret_index == turret_count: 
                break
        # Bridge: 
        canvas[turret_verti_r - 74: turret_verti_r + 26, turret_hori: turret_hori + 100, :] = self.img_base
        cv.putText(canvas, methods[Components.Bridge][0], [turret_hori + 5, turret_verti_r + 100], cv.FONT_HERSHEY_COMPLEX, .3, (0, 0, 0))
        for i in range(turret_index):
            canvas[ini_vertical_reversed - 100 - 25 * i: ini_vertical_reversed - 25 * max(0, i), turret_hori: turret_hori + 100, :] = self.img_base
        canvas[turret_verti_r - 100 - 25 * max(0, (turret_index - 1)): turret_verti_r - 25 * max(0, (turret_index - 1)), turret_hori: turret_hori + 100, :] = self.img_bridge
        cv.line(canvas, [turret_hori + 5, turret_verti_r + 75], [turret_hori + 5, turret_verti_r + 75 - (turret_index + 2) * 25 + 5], (0, 0, 0))
        # TODO: add support for multiple bridges and engines. 
        # Engine: 
        for i in range(turret_index - 1):
            canvas[ini_vertical_reversed - 100 - 25 * i: ini_vertical_reversed - 25 * max(0, i), turret_hori + 100: turret_hori + 200, :] = self.img_base
        canvas[turret_verti_r - 100 - 25 * max(0, (turret_index - 2)): turret_verti_r - 25 * max(0, (turret_index - 2)), turret_hori + 100: turret_hori + 200, :] = self.img_engine
        cv.putText(canvas, methods[Components.Engine][0], [turret_hori + 105, turret_verti_r + 100], cv.FONT_HERSHEY_COMPLEX, .3, (0, 0, 0))
        cv.line(canvas, [turret_hori + 105, turret_verti_r + 75], [turret_hori + 105, turret_verti_r + 75 - (turret_index + 1) * 25 + 5], (0, 0, 0))
        # Backward Arms: last turret: 
        for i in range(turret_index - 1):
            canvas[ini_vertical_reversed - 100 - 25 * i: ini_vertical_reversed - 25 * max(0, i), turret_hori + 200: turret_hori + 300, :] = self.img_base
        canvas[turret_verti_r - 100 - 25 * max(0, (turret_index - 3)): turret_verti_r - 25 * max(0, (turret_index - 3)), turret_hori + 200: turret_hori + 300, :] = cv.flip(self.img_turret, 1)
        cv.putText(canvas, methods[Components.Arms][-1], [turret_hori + 205, turret_verti_r + 100], cv.FONT_HERSHEY_COMPLEX, .3, (0, 0, 0))
        cv.line(canvas, [turret_hori + 205, turret_verti_r + 75], [turret_hori + 205, turret_verti_r + 75 - (turret_index) * 25 + 5], (0, 0, 0))
        # Tail: 
        # for i in range(turret_index - 3):
        #     canvas[ini_vertical_reversed - 100 - 25 * i: ini_vertical_reversed - 25 * max(0, i), turret_hori + 300: turret_hori + 400, :] = self.img_base
        # canvas[turret_verti_r - 100 - 25 * max(0, (turret_index - 4)): turret_verti_r - 25 * max(0, (turret_index - 4)), turret_hori + 300: turret_hori + 400, :] = self.img_tail
        canvas[ini_vertical_reversed - 100: ini_vertical_reversed, turret_hori + 300: turret_hori + 400, :] = self.img_tail
        self.draw_outcome = canvas
        cv.imwrite("./outputs/" + methods[Components.Head][0] + ".png", canvas)
        cv.imshow("canvas", canvas)
        cv.waitKey(0)
        cv.destroyAllWindows()


if __name__ == "__main__":
    cgg = class_gui_generator()
    # testing_dict = {
    #     Components.Head: ["Lin - II Class"],
    #     Components.Arms: ["log_loss", "log_loss_gradient", "gradient_descent"],
    #     Components.Bridge: ["step"],
    #     Components.Engine: ["steps"]
    # }
    # testing_dict = {
    #     Components.Head: ["Lin Gen Class"],
    #     Components.Arms: ["compute_mu", "compute_var"],
    #     Components.Bridge: ["fit_line"],
    #     Components.Engine: ["estimate_mu_var"]
    # }
    testing_dict = {
        Components.Head: ["Super Long Class"],
        Components.Arms: ["Turret 1", "Turret 2", "Turret 3", "Turret 4", "Turret 5", "Turret 6", "Turret 7"],
        Components.Bridge: ["Small Bridge", "Small Bridge 2"],
        Components.Engine: ["Engine 1", "Engine 2"]
    }
    cgg.manual_assign_manual_draw(testing_dict)
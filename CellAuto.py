class CellAuto:
    boundary_conds = ["Born-von_Karman",
                      "absorption_mechanism"]
    configs = []

    def __init__(self, rule_to_set_from, boundary_cond_to_choose):
        self.rule = rule_to_set_from
        self.boundary_cond_choice = boundary_cond_to_choose

    def adjust_config_weights(self):
        weights = '{0:08b}'.format(self.rule)
        self.configs = {"000": weights[7], "001": weights[6],
                        "010": weights[5], "011": weights[4],
                        "100": weights[3], "101": weights[2],
                        "110": weights[1], "111": weights[0]}

    def update_cells(self, cells):
        if not isinstance(cells, str):
            print(f"string expected, {type(cells)} passed")
            return
        if len(cells) == 0:
            print("No cells to update.")
            return

        self.adjust_config_weights()
        updated_cells = ""
        first = ""
        last = ""
        # "Born-von_Karman":
        if self.boundary_conds[self.boundary_cond_choice] == "Born-von_Karman":
            first = str(self.configs[cells[len(cells) - 1] + cells[0:2]])
            last = str(self.configs[cells[len(cells) - 2:len(cells)] + cells[0]])
        # case "absorption_mechanism":
        elif self.boundary_conds[self.boundary_cond_choice] == "absorption_mechanism":
            first = cells[0]
            last = cells[len(cells) - 1]

        updated_cells += first
        if len(cells) != 2:

            for i in range(len(cells) - 2):
                updated_cells += str((self.configs[cells[0 + i:3 + i]]))
        updated_cells += last
        return updated_cells

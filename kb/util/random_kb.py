import csv
import random
import string


def random_string(length, chars):
    return ''.join(random.choices(chars, k=length))


class FeatGenerator:
    def __init__(self, path_file, rows=5, id_max_len=50,
                 id_chars=f"{string.ascii_letters}{string.digits}/",
                 feat_len=10):
        self.path_file = path_file
        self.rows = rows
        self.id_len = id_max_len
        self.chars = id_chars.replace("|", "")
        self.n = feat_len

    def _id_generator(self):
        return random_string(random.randint(self.id_len // 3, self.id_len), self.chars)

    def _feat_generator(self):
        return [random.uniform(0, 20) for _ in range(self.n)]

    def generate_dict(self):
        """
        The functions generates a random dict like this:
            {inst: features, ...}
        :return:
        """
        ids = [self._id_generator() for _ in range(self.rows)]
        features = [self._feat_generator() for _ in range(self.rows)]
        return {inst_id: feats for inst_id, feats in zip(ids, features)}

    def generate_file(self, feat_dict=None):
        if feat_dict is None:
            feat_dict = self.generate_dict()
        with open(f'{self.path_file}.feat', 'w') as f:
            csv.writer(f, delimiter='|', lineterminator='\n').writerows(
                [inst_id, feats] for inst_id, feats in feat_dict.items())
        return feat_dict


class InfoGenerator:
    def __init__(self, path_file, insts, solvers=None, timeout=1800):
        if solvers is None:
            solvers = ["gecode", "chuffed", "coin_bc"]
        self.path_file = path_file
        self.insts = insts
        self.solvers = solvers
        self.timeout = timeout

    @staticmethod
    def _gen_goal() -> str:
        return random.choice(["sat", "min", "max"])

    @staticmethod
    def _gen_info(goal) -> str:
        if goal == "sat":
            return random.choice(["sat", "uns", "unk"])
        else:
            return random.choice(["sat", "uns", "unk", "opt"])

    @staticmethod
    def _gen_time(info, goal, timeout) -> int:
        if info == "unk" or (goal != "sat" and info == "sat"):
            return timeout
        else:
            return random.randint(1, timeout * 2 // 3)

    @staticmethod
    def _gen_val(info, goal):
        if goal == "sat" or info == "unk" or info == "uns":
            return "nan"
        else:
            return random.randint(1, 5000)

    @staticmethod
    def _gen_values(val, solving_time) -> dict:
        if val == "nan":
            return {}
        else:
            k = random.randint(1, solving_time)
            return {t_i: (random.randint(1, 5000) if t_i < k else val) for t_i in range(1, k + 1)}

    def generate_list(self):
        """
        The function generates a random list of lists like this:
            [[inst, solver, goal, info, time, val, values]...]
        :return:
        """
        info_list = []
        solvers = self.solvers + [random_string(10, string.ascii_lowercase) for _ in
                                  range(random.randint(0, 5))]
        for inst in self.insts:
            for solver in solvers:
                goal = self._gen_goal()
                info = self._gen_info(goal)
                time = self._gen_time(info, goal, self.timeout)
                val = self._gen_val(info, goal)
                values = self._gen_values(val, time)

                info_list.append([inst, solver, goal, info, time, val, values])

        return info_list

    def generate_file(self, info_list=None):
        if info_list is None:
            info_list = self.generate_list()
        with open(f'{self.path_file}.info', 'w') as f:
            csv.writer(f, delimiter='|', lineterminator='\n').writerows(info_list)
        return info_list


if __name__ == '__main__':
    from subprocess import run
    import os
    import sys

    # using full path starting from this file instead from where is called
    kbutil_path = os.path.join(*os.path.split(sys.argv[0])[:-1])
    random_csv_path = os.path.join(kbutil_path, "random_csv")
    if not os.path.exists(random_csv_path):
        os.mkdir(random_csv_path)
    directory_csv = file_csv = random_string(5, string.ascii_letters + string.digits)
    os.mkdir(os.path.join(random_csv_path, directory_csv))
    full_path = os.path.join(random_csv_path, directory_csv, file_csv)

    # feat and info generators
    feat = FeatGenerator(full_path)
    feat_dict = feat.generate_file()

    info = InfoGenerator(full_path, feat_dict.keys())
    info_list = info.generate_file()

    # run csv2kb.py given the newly created feat and info files
    run(["python3", os.path.join(kbutil_path, "csv2kb.py"), f"kb_{file_csv}", f"{full_path}.feat", f"{full_path}.info"])
